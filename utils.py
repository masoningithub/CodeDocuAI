import os
import tempfile
import docx2txt
import fitz  # PyMuPDF
from openai import OpenAI
from gtts import gTTS
from typing import Union, Optional
import logging
import streamlit as st
from sdd_templates import SDD_TEMPLATES, get_template_sections, generate_sdd_outline
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
MAX_TEXT_LENGTH = 8000  # Increased for API calls to handle larger content
TTS_MAX_LENGTH = 500     # For text-to-speech
SUPPORTED_FILE_TYPES = ['.txt', '.js', '.py', '.pdf', '.docx', '.md', '.java', '.c', '.cpp', '.h']

# API Configuration
API_CONFIGS = {
    "OpenAI": {
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4",
    },
    "Deepseek": {
        "base_url": "https://api.deepseek.com",
        "model": "deepseek-chat",
    },
    "Aliyun": {
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "deepseek-r1",
    },
    "volcengine": {
        "base_url": "https://ark.cn-beijing.volces.com/api/v3",
        "model": "ep- ",
    },
    "siliconflow": {
        "base_url": "https://api.siliconflow.cn/v1",
        "model": "deepseek-ai/DeepSeek-V3",
    },
    "Other": {
        "base_url": "https://api.otherprovider.com/",
        "model": "Your-Model-Here",
    }
}

def clean_markdown_wrappers(mindmap_content: str) -> str:
    """
    Remove markdown code block wrappers from mindmap content if present.
    
    Args:
        mindmap_content: Raw mindmap content that might be wrapped in ```markdown
        
    Returns:
        Cleaned mindmap content without wrapper
    """
    if not mindmap_content:
        return mindmap_content
    
    content = mindmap_content.strip()
    lines = content.split('\n')
    
    # Check if first line starts with ```markdown
    if lines and lines[0].strip().startswith('```markdown'):
        # Remove first line
        return '\n'.join(lines[1:])

    return content

def clean_llm_response(response_text: str) -> str:
    """
    Clean LLM response by removing introductory text but preserving legitimate code blocks.
    
    Args:
        response_text: Raw response from LLM
        
    Returns:
        Cleaned markdown content
    """
    if not response_text:
        return ""
    
    # Common introductory phrases to remove
    intro_patterns = [
        r"^Here's?\s+(?:the\s+)?(?:comprehensive\s+)?(?:software\s+design\s+document|sdd|mindmap|summary).*?:\s*",
        r"^I'll\s+(?:create|generate|provide).*?:\s*",
        r"^Based\s+on\s+the\s+provided\s+code.*?:\s*",
        r"^Below\s+is\s+(?:the\s+)?.*?:\s*",
        r"^The\s+following\s+is.*?:\s*",
    ]
    
    cleaned_text = response_text.strip()
    
    # Remove introductory patterns
    for pattern in intro_patterns:
        cleaned_text = re.sub(pattern, "", cleaned_text, flags=re.IGNORECASE | re.MULTILINE)
    
    # Remove leading/trailing whitespace and empty lines at start
    cleaned_text = cleaned_text.strip()
    while cleaned_text.startswith('\n'):
        cleaned_text = cleaned_text[1:]
    
    # ONLY remove code block wrappers if the ENTIRE response is wrapped in a single code block
    # AND it starts at the very beginning (indicating it's a wrapper, not content)
    if cleaned_text.startswith('```markdown') and cleaned_text.endswith('```'):
        # Check if this is a single wrapper by finding the first closing ``` after ```markdown
        first_close_pos = cleaned_text.find('```', 11)  # Start searching after '```markdown'
        last_close_pos = cleaned_text.rfind('```')
        
        # If the first closing ``` is also the last one, it's a single wrapper
        if first_close_pos == last_close_pos and first_close_pos != -1:
            # Extract content between ```markdown and the final ```
            match = re.search(r'^```markdown\s*\n?(.*?)\n?```$', cleaned_text, re.DOTALL)
            if match:
                cleaned_text = match.group(1).strip()
    
    # DO NOT remove other code blocks (like ```mermaid, ```python, etc.) as they are legitimate content
    
    return cleaned_text

def get_current_api_config():
    """
    Get current API configuration from environment variables or session state.
    This function properly reads the user-selected configuration.
    """
    # First try to get from environment variables (set by set_api_config)
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    model = os.getenv("OPENAI_MODEL")
    provider = os.getenv("API_PROVIDER")
    
    # If not found in env vars, try to get from session state
    if not api_key and hasattr(st, 'session_state'):
        if st.session_state.get('api_key_set', False):
            # Get from session state if available
            provider = st.session_state.get('api_provider', 'Deepseek')
            base_url = st.session_state.get('custom_base_url')
            model = st.session_state.get('custom_model')
            api_key = st.session_state.get('openai_api_key')  # This might not be stored in session state for security
    
    # Fallback to default configuration if nothing is set
    if not all([api_key, base_url, model]):
        default_provider = 'Deepseek'
        default_config = API_CONFIGS.get(default_provider, API_CONFIGS['Deepseek'])
        base_url = base_url or default_config['base_url']
        model = model or default_config['model']
        provider = provider or default_provider
    
    return {
        'api_key': api_key,
        'base_url': base_url,
        'model': model,
        'provider': provider
    }

# Initialize OpenAI client with dynamic API key handling
def get_openai_client():
    """Get OpenAI client with current API key and configuration from user selection."""
    config = get_current_api_config()
    
    if not config['api_key']:
        raise ValueError("OpenAI API key not configured. Please set your API key in the interface.")
    
    logger.info(f"Using API provider: {config['provider']}, base_url: {config['base_url']}, model: {config['model']}")
    
    return OpenAI(
        api_key=config['api_key'],
        base_url=config['base_url']
    )

def extract_code_from_file(uploaded_file) -> str:
    """
    Extracts text content from uploaded file with robust error handling.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        
    Returns:
        str: Content of the file
        
    Raises:
        ValueError: If file cannot be read or is empty
        UnicodeDecodeError: If file encoding is not supported
    """
    try:
        # Validate file extension
        _, ext = os.path.splitext(uploaded_file.name.lower())
        if ext not in SUPPORTED_FILE_TYPES:
            raise ValueError(f"Unsupported file type: {ext}. Supported types: {', '.join(SUPPORTED_FILE_TYPES)}")

        # Read content with encoding fallback
        uploaded_file.seek(0)
        content = None
        
        for encoding in ['utf-8', 'latin-1']:
            try:
                uploaded_file.seek(0)
                content = uploaded_file.read().decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            raise UnicodeDecodeError("Failed to decode file with standard encodings")
            
        if not content.strip():
            raise ValueError("Uploaded file is empty")
            
        return content
        
    except Exception as e:
        logger.error(f"Error extracting text from file: {str(e)}")
        raise ValueError(f"Error processing file: {str(e)}")

def extract_text_from_file(uploaded_file) -> str:
    """
    Extract text from PDF or DOCX files with proper resource cleanup.
    """
    try:
        _, ext = os.path.splitext(uploaded_file.name.lower())
        uploaded_file.seek(0)
        
        if ext == '.pdf':
            with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
                return " ".join(page.get_text() for page in doc)
                
        elif ext == '.docx':
            with tempfile.NamedTemporaryFile(suffix=".docx") as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file.flush()
                return docx2txt.process(temp_file.name)
                
        return ""
        
    except Exception as e:
        logger.error(f"Error extracting text from {uploaded_file.name}: {str(e)}")
        raise ValueError(f"Could not extract text from file: {str(e)}")

def _call_llm(prompt: str, task_description: str, temperature: float = 0.5) -> str:
    """Helper function for LLM API calls with error handling and response cleaning."""
    try:
        client = get_openai_client()
        config = get_current_api_config()
        model_name = config['model']
        
        logger.info(f"Making API call to {config['provider']} with model {model_name}")
        
        # Don't truncate the prompt - send full content
        full_prompt = f"{task_description}: {prompt}"
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[{
                "role": "user",
                "content": full_prompt
            }],
            stream=False,
            temperature=temperature 
            # max_tokens=2000,  # Reduced per part to ensure completion
        )
        
        raw_response = response.choices[0].message.content.strip()
        # Clean the response to remove introductory text
        cleaned_response = clean_llm_response(raw_response)
        
        logger.info(f"LLM response length: {len(cleaned_response)} characters")
        return cleaned_response
    except Exception as e:
        logger.error(f"LLM API error: {str(e)}")
        raise ValueError(f"Failed to generate {task_description}: {str(e)}")

def summarize_text(text: str) -> str:
    """Generate a concise summary of the provided text."""
    return _call_llm(text, "Summarize the following technical document")

def get_SDD_perSection(text: str, template_name: str = 'standard') -> str:
    """
    Generate Software Design Document from code/text using specified template.
    Uses multi-part generation to avoid token limits and ensure complete documents.
    
    Args:
        text: Source code or text to analyze
        template_name: SDD template to use ('standard', 'microservices', 'web_application', 'api_service')
    
    Returns:
        str: Generated SDD following the specified template structure
    """
    try:
        # Get the template sections
        sections = get_template_sections(template_name)
        template_info = SDD_TEMPLATES.get(template_name, SDD_TEMPLATES['standard'])
        
        # Split sections into logical groups to avoid token limits
        section_groups = []
        if template_name == 'standard':
            section_groups = [
                # Group 1: Overview sections
                ["1. Overview", "1.1 Purpose", "1.2 References"],
                # Group 2: Solution Overview 
                ["2. Solution Overview", "2.1 Solution Feature", "2.1.1 Automation Type", "2.1.2 Technologies Involved"],
                # Group 3: Workflow sections
                ["2.2 Workflow", "2.2.1 Restriction", "2.2.2 Solution Diagram", "2.2.3 To-Be workflow", "2.2.4 Input and Output", "2.2.5 Data Items in Configuration File"],
                # Group 4: Design sections
                ["3. Design", "3.1 Module Design", "3.2 Module Detail", "3.3 Data Structure Design"],
                # Group 5: Exception and Security
                ["4. Exception Handling Design", "4.1 Exception Categories", "4.2 System Exception", "4.3 Business Exception", "4.4 Exception Handling Process", "5. Security Design", "5.1 System/Application Credentials", "5.2 Data Transmission"]
            ]
        else:
            # For other templates, split into smaller groups
            section_groups = [sections[i:i+5] for i in range(0, len(sections), 5)]
        
        logger.info(f"Generating SDD in {len(section_groups)} parts to ensure completeness")
        
        # Generate each section group
        sdd_parts = []
        for i, section_group in enumerate(section_groups):
            try:
                logger.info(f"Generating SDD part {i+1}/{len(section_groups)}: {section_group[:2]}...")
                
                section_list = "\n".join([f"- {section}" for section in section_group])
                
                part_prompt = f"""
                Analyze the following code and generate a comprehensive Software Design Document (SDD) section
                following the {template_info['name']} template structure.
                
                FOCUS ONLY ON THESE SECTIONS:
                {section_list}
                
                Context: {template_info['description']}
                
                Instructions:
                1. Generate ONLY the sections listed above - do not include other sections
                2. Use exact headings that match the section names provided
                3. Provide detailed, comprehensive content for each section
                4. Include technical details, architecture decisions, and implementation specifics
                5. Use proper markdown formatting with headers, lists, and code blocks
                6. If a section is not applicable, briefly explain why and provide alternatives
                7. IMPORTANT: Return ONLY the markdown content without any introductory text
                8. IMPORTANT: Complete ALL sections in the list - do not stop early
                9. Each section should have substantial content (minimum 3-4 sentences per section)
                10. For "Solution Diagram" section, describe the diagram in text format since we cannot generate images
                
                Code to analyze:
                {text[:6000]}
                
                Generate the specified sections with detailed content:
                """
                
                part_result = _call_llm(part_prompt, f"Generate SDD part {i+1}", temperature=0.3)
                if part_result and part_result.strip():
                    sdd_parts.append(part_result.strip())
                    
            except Exception as e:
                logger.error(f"Error generating SDD part {i+1}: {str(e)}")
                # Continue with other parts even if one fails
                continue
        
        if not sdd_parts:
            # Fallback to single generation if multi-part fails
            logger.warning("Multi-part generation failed, falling back to single generation")
            return get_SDD_single(text, template_name)
        
        # Combine all parts
        complete_sdd = "\n\n".join(sdd_parts)
        
        # Add document header if not present
        if not complete_sdd.startswith('#'):
            header = f"# {template_info['name']}\n\n*Generated by CodeDocuAI*\n\n"
            complete_sdd = header + complete_sdd
            
        logger.info(f"Successfully generated complete SDD with {len(sdd_parts)} parts")
        return complete_sdd
        
    except Exception as e:
        logger.error(f"Error in multi-part SDD generation: {str(e)}")
        # Final fallback
        return get_SDD_single(text, template_name)


def get_SDD(text: str, template_name: str = 'standard') -> str:
    """
    Generate Software Design Document from code/text using specified template.
    
    Args:
        text: Source code or text to analyze
        template_name: SDD template to use ('standard', 'microservices', 'web_application', 'api_service')
    
    Returns:
        str: Generated SDD following the specified template structure
    """
    try:
        # Get the template sections
        sections = get_template_sections(template_name)
        template_info = SDD_TEMPLATES.get(template_name, SDD_TEMPLATES['standard'])
        
        # Create detailed prompt with template structure
        template_structure = "\n".join([f"- {section}" for section in sections])
        
        enhanced_prompt = f"""
        Analyze the following code and generate a comprehensive Software Design Document (SDD) 
        following the {template_info['name']} template structure.
        
        Required sections to cover:
        {template_structure}
        
        Instructions:
        1. Provide detailed content for each relevant section based on the code analysis
        2. Use clear headings that match the template structure
        3. Include technical details, architecture decisions, and implementation specifics
        4. If a section is not applicable to the code, briefly explain why
        5. Ensure the document is professional and comprehensive
        6. Format the output in proper markdown with headers, lists, and code blocks
        
        Code to analyze:
        {text[:MAX_TEXT_LENGTH]}
        
        Generate a detailed SDD following the above structure:
        """
        
        return _call_llm(enhanced_prompt, "Generate comprehensive SDD", temperature=0.3)
        
    except Exception as e:
        logger.error(f"Error generating SDD: {str(e)}")
        # Fallback to basic SDD generation
        return _call_llm(text, "Review below code and generate an SDD document showing how the code works")

def get_SDD_single(text: str, template_name: str = 'standard') -> str:
    """
    Fallback single-generation method for SDD.
    """
    try:
        sections = get_template_sections(template_name)
        template_info = SDD_TEMPLATES.get(template_name, SDD_TEMPLATES['standard'])
        
        template_structure = "\n".join([f"- {section}" for section in sections])
        
        enhanced_prompt = f"""
        Analyze the following code and generate a Software Design Document (SDD) 
        following the {template_info['name']} template structure.
        
        Required sections to cover:
        {template_structure}
        
        Instructions:
        1. Provide content for each relevant section based on the code analysis
        2. Use clear headings that match the template structure exactly
        3. Include technical details and implementation specifics
        4. Format the output in proper markdown
        5. IMPORTANT: Return ONLY the markdown content without any introductory text
        6. If you cannot complete all sections due to length limits, prioritize the first sections
        
        Code to analyze:
        {text[:4000]}
        
        Generate an SDD following the structure:
        """
        
        return _call_llm(enhanced_prompt, "Generate SDD (single generation)", temperature=0.3)
        
    except Exception as e:
        logger.error(f"Error in single SDD generation: {str(e)}")
        return f"# Error Generating SDD\n\nAn error occurred while generating the SDD: {str(e)}"

def get_mindmap(text: str) -> str:
    """Generate a mindmap in markdown format from the text."""
    enhanced_prompt = f"""
    Create a comprehensive mindmap to show the workflow of the code in markdown format for the following code.
    
    Instructions:
    1. Use bullet points and proper indentation to show the hierarchical execution flow
    2. Break down the code into discrete execution steps (Step 1, Step 2, etc.)
    3. For each step, clearly explain:
       - What operation is being performed
       - What data is being processed or transformed
       - What variables are being created or modified
       - What the output or result of that step is
    4. Show the logical flow as if you're tracing through the code execution
    5. Focus on the runtime behavior and data flow, not just static code structure
    6. Use markdown formatting with clear headings and subheadings
    7. Structure it like: Main Function → Step 1: [description] → Sub-step 1.1: [details], etc.
    8. IMPORTANT: Return ONLY the markdown content without any introductory text or explanations
    9. Make it comprehensive enough to understand the complete execution path
    10. Do not include any mermaid or other code blocks, just pure markdown with bullet points
    
    Code to analyze:
    {text}
    
    Generate a detailed mindmap:
    """
    
    result = _call_llm(enhanced_prompt, "Generate comprehensive mindmap in markdown format")
    # Clean markdown wrapper if present
    return result

def generate_flowchart(summary: str) -> str:
    """
    Generate Graphviz flowchart from summary text.
    Improved with better node naming and error handling.
    """
    try:
        steps = [line.strip() for line in summary.split('.') if line.strip()]
        if not steps:
            raise ValueError("Summary text is empty or invalid")
            
        flowchart = ['digraph G {', '  node [shape=rectangle];']
        
        for i in range(len(steps)-1):
            # Truncate long node labels
            from_node = steps[i][:50] + ('...' if len(steps[i]) > 50 else '')
            to_node = steps[i+1][:50] + ('...' if len(steps[i+1]) > 50 else '')
            flowchart.append(f'  "{from_node}" -> "{to_node}";')
            
        flowchart.append('}')
        return '\n'.join(flowchart)
        
    except Exception as e:
        logger.error(f"Flowchart generation error: {str(e)}")
        return "digraph G { Error -> \"Generating flowchart\"; }"

def generate_tts(text: str, output_path: Optional[str] = None) -> str:
    """
    Generate text-to-speech audio with improved error handling.
    Uses temporary directory if no output path specified.
    """
    try:
        if not output_path:
            output_dir = tempfile.mkdtemp()
            output_path = os.path.join(output_dir, "summary.mp3")
            
        tts = gTTS(text[:TTS_MAX_LENGTH], lang="en", slow=False)
        tts.save(output_path)
        return output_path
        
    except Exception as e:
        logger.error(f"TTS generation error: {str(e)}")
        raise ValueError(f"Failed to generate audio: {str(e)}")

def test_api_connection() -> bool:
    """Test if the API connection is working with current configuration."""
    try:
        client = get_openai_client()
        config = get_current_api_config()
        model_name = config['model']
        
        logger.info(f"Testing API connection for {config['provider']} with model {model_name}")
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[{
                "role": "user",
                "content": "Say 'Hello, API is working!'"
            }],
            stream=False,
            temperature=0.1
        )
        
        result = response.choices[0].message.content.strip()
        st.success(f"✅ API Test Successful ({config['provider']}): {result}")
        return True
        
    except Exception as e:
        config = get_current_api_config()
        st.error(f"❌ API Connection Failed ({config.get('provider', 'Unknown')}): {str(e)}")
        return False

def get_available_sdd_templates() -> dict:
    """Get all available SDD templates with their descriptions."""
    return {
        name: template['description'] 
        for name, template in SDD_TEMPLATES.items()
    }

def preview_sdd_template(template_name: str) -> str:
    """Generate a preview of the SDD template structure."""
    return generate_sdd_outline(template_name)

def get_api_configs() -> dict:
    """Get available API configurations."""
    return API_CONFIGS

def set_api_config(provider: str, base_url: str, model: str, api_key: str):
    """Set API configuration in environment variables."""
    os.environ["OPENAI_API_KEY"] = api_key
    os.environ["OPENAI_BASE_URL"] = base_url
    os.environ["OPENAI_MODEL"] = model
    os.environ["API_PROVIDER"] = provider
    logger.info(f"API configuration set for provider: {provider}")
