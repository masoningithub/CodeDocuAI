import streamlit as st
from utils import (
    summarize_text, get_SDD, extract_code_from_file, get_mindmap, 
    get_available_sdd_templates, preview_sdd_template, test_api_connection,
    get_api_configs, set_api_config,clean_markdown_wrappers
)
from markmap_component import render_markmap, create_markmap_download_link
import os
from typing import List, Dict

# Enhanced page configuration with icon
st.set_page_config(
    page_title="CodeDocuAI - Smart Documentation", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main app styling */
    .main > div {
        padding: 2rem 1rem;
    }
    
    /* Enhanced messages */
    .element-container .stSuccess {
        background: linear-gradient(90deg, #d4edda 0%, #c3e6cb 100%);
        border: 1px solid #c3e6cb;
        border-radius: 12px;
        border-left: 4px solid #28a745;
    }
    
    .element-container .stInfo {
        background: linear-gradient(90deg, #cce7ff 0%, #99d6ff 100%);
        border: 1px solid #99d6ff;
        border-radius: 12px;
        border-left: 4px solid #007bff;
    }
    
    .element-container .stWarning {
        background: linear-gradient(90deg, #fff3cd 0%, #ffecb3 100%);
        border: 1px solid #ffecb3;
        border-radius: 12px;
        border-left: 4px solid #ffc107;
    }
    
    .element-container .stError {
        background: linear-gradient(90deg, #f8d7da 0%, #f1c2c7 100%);
        border: 1px solid #f1c2c7;
        border-radius: 12px;
        border-left: 4px solid #dc3545;
    }
    
    /* Enhanced buttons */
    .stButton > button {
        border-radius: 12px;
        border: none;
        transition: all 0.3s ease;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    .stButton > button[kind="secondary"] {
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
    }
    
    /* File uploader enhancement */
    .stFileUploader > div {
        border-radius: 12px;
        border: 2px dashed #ccc;
        transition: all 0.3s ease;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    .stFileUploader > div:hover {
        border-color: #667eea;
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    }
    
    /* Enhanced inputs */
    .stSelectbox > div > div, .stTextInput > div > div {
        border-radius: 8px;
        border: 2px solid #e1e8ed;
        transition: border-color 0.3s ease;
    }
    
    .stSelectbox > div > div:focus-within, .stTextInput > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Progress bar enhancement */
    .stProgress > div > div {
        border-radius: 10px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Tab enhancement */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px 12px 0 0;
        padding: 0.75rem 1.5rem;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border: 2px solid #dee2e6;
        border-bottom: none;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: #667eea;
    }
    
    /* Expander enhancement */
    .streamlit-expanderHeader {
        border-radius: 8px;
        background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
        border: 1px solid #dee2e6;
    }
    
    /* Text area enhancement */
    .stTextArea textarea {
        border-radius: 8px;
        border: 2px solid #e1e8ed;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Metric enhancement */
    .metric-container {
        background: white;
        border: 1px solid #e1e8ed;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        transition: transform 0.2s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* Hide Streamlit footer */
    .viewerBadge_container__1QSob {
        display: none;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main > div {
            padding: 1rem 0.5rem;
        }
        
        .stColumns {
            flex-direction: column;
        }
        
        .stColumns > div {
            width: 100% !important;
            margin-bottom: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Enhanced header with gradient background
st.markdown("""
<div style="
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    padding: 1rem 2rem; 
    border-radius: 15px; 
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
">
    <div style="text-align: center;">
        <h1 style="
            color: white; 
            margin: 0; 
            font-size: 3rem; 
            font-weight: 700;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        ">
            🤖 CodeDocuAI
        </h1>
        <p style="
            color: rgba(255,255,255,0.9); 
            margin: 1rem 0 0 0; 
            font-size: 1.25rem;
            font-weight: 300;
        ">
            Transform your code into documentation with AI
        </p>
        <div style="
            margin-top: 1.5rem;
            padding: 0.5rem 1rem;
            background: rgba(255,255,255,0.1);
            border-radius: 25px;
            display: inline-block;
            backdrop-filter: blur(10px);
        ">
            <span style="color: white; font-size: 0.9rem;">
                ✨ Powered by Advanced AI • 🚀 Multiple Templates • 🧠 Interactive Mindmaps
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'selected_template' not in st.session_state:
    st.session_state.selected_template = 'standard'
if 'results' not in st.session_state:
    st.session_state.results = []
if 'api_key_set' not in st.session_state:
    st.session_state.api_key_set = False
if 'api_provider' not in st.session_state:
    st.session_state.api_provider = 'Deepseek'
if 'custom_base_url' not in st.session_state:
    st.session_state.custom_base_url = ''
if 'custom_model' not in st.session_state:
    st.session_state.custom_model = ''

# Enhanced API status display function
def show_api_status():
    if st.session_state.get('api_key_set', False) or os.getenv("OPENAI_API_KEY"):
        provider = os.getenv("API_PROVIDER", "Unknown")
        model = os.getenv("OPENAI_MODEL", "Unknown")
        
        status_html = f"""
        <div style="
            background: linear-gradient(90deg, #00c9ff 0%, #92fe9d 100%);
            padding: 0.75rem;
            border-radius: 12px;
            margin: 1rem 0;
            color: white;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,201,255,0.3);
        ">
            <strong>✅ API Connected</strong><br>
            <small>Provider: {provider} | Model: {model}</small>
        </div>
        """
        st.markdown(status_html, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="
            background: linear-gradient(90deg, #ff9a9e 0%, #fecfef 100%);
            padding: 1rem;
            border-radius: 12px;
            margin: 1rem 0;
            color: white;
            text-align: center;
            box-shadow: 0 4px 15px rgba(255,154,158,0.3);
        ">
            <strong>⚠️ API Configuration Required</strong><br>
            <small>Please configure your API settings below</small>
        </div>
        """, unsafe_allow_html=True)

# Status card creation function
def create_status_card(title, value, icon, color):
    return f"""
    <div style="
        background: {color}; 
        padding: 0.75rem; 
        border-radius: 15px; 
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        margin: 0.5rem 0;
        transition: transform 0.3s ease;
        border: 1px solid rgba(255,255,255,0.1);
    " onmouseover="this.style.transform='translateY(-5px)'" 
       onmouseout="this.style.transform='translateY(0)'">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{icon}</div>
        <h4 style="margin: 0.5rem 0; color: white; font-weight: 600;">{title}</h4>
        <p style="margin: 0; color: rgba(255,255,255,0.9); font-size: 1.1rem; font-weight: bold;">{value}</p>
    </div>
    """

# Show API status
show_api_status()

# API Key Configuration
st.markdown("### 🔑 API Configuration")

# Get available API configs
api_configs = get_api_configs()

with st.expander("Configure your API Settings", expanded=not st.session_state.get('api_key_set', False)):
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # API Provider selection
        selected_provider = st.selectbox(
            "Select API Provider",
            options=list(api_configs.keys()),
            index=list(api_configs.keys()).index(st.session_state.api_provider),
            key="provider_select"
        )
        
        # Update session state
        if selected_provider != st.session_state.api_provider:
            st.session_state.api_provider = selected_provider
            # Auto-fill base URL and model from config
            config = api_configs[selected_provider]
            st.session_state.custom_base_url = config['base_url']
            st.session_state.custom_model = config['model']
            st.rerun()
        
        # API Key input
        api_key = st.text_input(
            "API Key",
            type="password",
            placeholder="Enter your API key here...",
            help="Your API key will be used for this session only and not stored permanently.",
            key="openai_api_key"
        )
    
    with col2:
        # Base URL and Model configuration
        base_url = st.text_input(
            "Base URL",
            value=st.session_state.custom_base_url or api_configs[selected_provider]['base_url'],
            help="API endpoint URL",
            key="base_url_input"
        )
        
        model_name = st.text_input(
            "Model Name",
            value=st.session_state.custom_model or api_configs[selected_provider]['model'],
            help="Model identifier for the API",
            key="model_input"
        )
    
    # Configuration buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("💾 Save Configuration", type="primary", key="save_config"):
            if api_key and base_url and model_name:
                set_api_config(selected_provider, base_url, model_name, api_key)
                st.session_state.api_key_set = True
                st.session_state.custom_base_url = base_url
                st.session_state.custom_model = model_name
                st.success("✅ API Configuration saved!")
                st.rerun()
            else:
                st.error("❌ Please fill in all configuration fields")
    
    with col2:
        if st.button("🔄 Reset to Default", type="secondary", key="reset_config"):
            config = api_configs[selected_provider]
            st.session_state.custom_base_url = config['base_url']
            st.session_state.custom_model = config['model']
            st.rerun()
    
    with col3:
        if st.button("🧪 Test Connection", type="secondary", key="test_api"):
            if st.session_state.get('api_key_set', False) or os.getenv("OPENAI_API_KEY"):
                test_api_connection()
            else:
                st.error("Please save configuration first!")

st.markdown("---")

# Enhanced sidebar
with st.sidebar:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
    ">
        <h2 style="color: white; margin: 0;">⚙️ Configuration</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Get available templates
    available_templates = get_available_sdd_templates()
    
    # Template selection
    selected_template = st.selectbox(
        "Select SDD Template",
        options=list(available_templates.keys()),
        format_func=lambda x: f"{x.replace('_', ' ').title()} - {available_templates[x][:50]}...",
        index=list(available_templates.keys()).index(st.session_state.selected_template),
        key="template_selector"
    )
    
    # Update session state
    st.session_state.selected_template = selected_template
    
    # Template preview
    if st.button("📋 Preview Template Structure", key="preview_template"):
        template_preview = preview_sdd_template(selected_template)
        st.text_area("Template Structure Preview", template_preview, height=300, key="template_preview_area")
    
    st.markdown("---")
    
    # Enhanced template descriptions
    st.markdown("### 📚 Template Descriptions")
    for name, desc in available_templates.items():
        with st.expander(f"📄 {name.replace('_', ' ').title()}"):
            st.write(desc)
    
    st.markdown("---")
    
    # Enhanced current configuration display
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #dee2e6;
    ">
        <h4 style="margin: 0 0 1rem 0; color: #495057;">📊 Current Status</h4>
    """, unsafe_allow_html=True)
    
    st.write(f"**Template**: {selected_template.replace('_', ' ').title()}")
    st.write(f"**Files Loaded**: {len(st.session_state.uploaded_files)}")
    
    if st.session_state.analysis_complete:
        st.success("✅ Analysis Complete")
        st.write(f"**Results**: {len(st.session_state.results)} files processed")
    elif st.session_state.uploaded_files:
        st.info("⏳ Ready to Analyze")
    else:
        st.info("📁 No Files Loaded")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Enhanced file uploader
    st.markdown("### 📁 Upload Your Code Files")
    uploaded_files = st.file_uploader(
        "Choose one or more code files to analyze",
        type=['txt', 'js', 'py', 'md', 'java', 'c', 'cpp', 'h'],
        accept_multiple_files=True,
        help="Supported formats: .txt, .js, .py, .md, .java, .c, .cpp, .h",
        key="file_uploader"
    )

with col2:
    if uploaded_files:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #00c9ff 0%, #92fe9d 100%);
            padding: 0.75rem;
            border-radius: 12px;
            color: white;
            text-align: center;
            margin-top: 2rem;
        ">
            <h4 style="margin: 0;">📁 Files Ready</h4>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.75rem; font-weight: bold;">
                {len(uploaded_files)} file(s) selected
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # List files
        st.markdown("**Selected Files:**")
        for file in uploaded_files:
            st.write(f"• {file.name}")

# Add uploaded files to session state
if uploaded_files:
    st.session_state.uploaded_files = uploaded_files

# Simple status line
if st.session_state.uploaded_files:
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.info(f"📁 **Files:** {len(st.session_state.uploaded_files)}")
    with col2:
        template_name = selected_template.replace('_', ' ').title()
        st.info(f"📋 **Template:** {template_name}")
    with col3:
        generate_options = st.multiselect(
            "🎯 Generate:",
            ["SDD", "Mindmap", "Summary"],
            default=["SDD", "Mindmap", "Summary"],
            key="generate_options"
        )

# Enhanced animated progress function
def show_animated_progress(current, total, filename):
    progress_html = f"""
    <div style="margin: 1.5rem 0; padding: 1rem; background: white; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.75rem;">
            <span style="font-weight: 600; color: #495057;">🔄 Processing: {filename}</span>
            <span style="color: #6c757d; font-weight: 500;">{current}/{total}</span>
        </div>
        <div style="background: #e9ecef; border-radius: 10px; overflow: hidden; height: 8px;">
            <div style="
                width: {(current/total)*100}%; 
                height: 100%; 
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                transition: width 0.5s ease;
                border-radius: 10px;
            "></div>
        </div>
    </div>
    """
    return progress_html

# Enhanced analyze button and processing
analyze_button = False
generate_options = ["SDD", "Mindmap", "Summary"]  # Default value

if st.session_state.uploaded_files:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_button = st.button(
            "🚀 Analyze Files", 
            type="primary", 
            key="analyze_button",
            use_container_width=True
        )

if analyze_button and st.session_state.uploaded_files:
    # Check if API key is configured
    if not (st.session_state.get('api_key_set', False) or os.getenv("OPENAI_API_KEY")):
        st.error("❌ Please configure your API settings first!")
        st.stop()
    
    st.session_state.analysis_complete = False
    
    # Hide header and API sections, show progress at top
    st.markdown("""
    <style>
        .main > div > div:nth-child(1),
        .main > div > div:nth-child(2),
        .main > div > div:nth-child(3) {
            display: none !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Progress at page top
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0 2rem 0;
        text-align: center;
        color: white;
        position: sticky;
        top: 0;
        z-index: 100;
    ">
        <h2 style="margin: 0;">🔄 Analysis in Progress</h2>
        <p style="margin: 0.5rem 0 0 0;">Please wait while we process your files...</p>
    </div>
    """, unsafe_allow_html=True)
    
    progress_container = st.empty()
    
    try:
        results = []
        total_files = len(st.session_state.uploaded_files)
        
        for i, uploaded_file in enumerate(st.session_state.uploaded_files):
            # Update progress
            progress_container.markdown(
                show_animated_progress(i+1, total_files, uploaded_file.name), 
                unsafe_allow_html=True
            )
            
            try:
                # Read file content
                text = extract_code_from_file(uploaded_file)
                
                if not text.strip():
                    st.warning(f"File {uploaded_file.name} is empty! Skipping...")
                    continue
                
                # Store results for each file
                file_result = {
                    'filename': uploaded_file.name,
                    'content': text,
                    'sdd': None,
                    'mindmap': None,
                    'summary': None,
                    'template_used': selected_template
                }
                
                # Process file content based on selected options
                if "SDD" in generate_options:
                    with st.spinner(f"Generating SDD for {uploaded_file.name} using {selected_template} template..."):
                        raw_SDD = get_SDD(text, selected_template)
                        file_result['sdd'] = clean_markdown_wrappers(raw_SDD)
                
                if "Mindmap" in generate_options:
                    with st.spinner(f"Generating mindmap for {uploaded_file.name}..."):
                        file_result['mindmap'] = get_mindmap(text)
                
                if "Summary" in generate_options:
                    with st.spinner(f"Summarizing {uploaded_file.name}..."):
                        # Use SDD for summary if available, otherwise use original content
                        summary_source = file_result['sdd'] if file_result['sdd'] else text
                        file_result['summary'] = summarize_text(summary_source)
                
                results.append(file_result)
                
            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {str(e)}")
                continue
        
        # Store results in session state for export
        st.session_state.results = results
        st.session_state.analysis_complete = True
        
        progress_container.empty()
        
        if results:
            # Enhanced success message
            st.markdown(f"""
            <div style="
                background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
                padding: 1rem;
                border-radius: 15px;
                text-align: center;
                margin: 2rem 0;
                box-shadow: 0 8px 25px rgba(17,153,142,0.3);
                color: white;
            ">
                <h2 style="margin: 0;">🎉 Analysis Complete!</h2>
                <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem;">
                    Successfully processed {len(results)} files. Your documentation is ready!
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Auto-scroll to results
            st.markdown("""
            <script>
                setTimeout(function() {
                    const resultsSection = document.querySelector('h2[style*="📊 Analysis Results"]').parentElement;
                    if (resultsSection) {
                        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                }, 1000);
            </script>
            """, unsafe_allow_html=True)
        else:
            st.warning("No results generated. Please check your files and API configuration.")
    
    except Exception as e:
        st.error(f"Error during analysis: {str(e)}")
        progress_container.empty()

# Enhanced results display
if st.session_state.analysis_complete and st.session_state.results:
    st.markdown("---")
    
    # Results header
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0.75rem;
        border-radius: 15px;
        margin: 2rem 0;
        text-align: center;
        color: white;
    ">
        <h2 style="margin: 0;">📊 Analysis Results</h2>
        <p style="margin: 0.5rem 0 0 0;">
            Explore your generated documentation below
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for each processed file
    tabs = st.tabs([f"📄 {res['filename']}" for res in st.session_state.results])
    
    for tab, result in zip(tabs, st.session_state.results):
        with tab:
            # Enhanced file info header
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                padding: 1.5rem;
                border-radius: 12px;
                margin-bottom: 1.5rem;
                border-left: 4px solid #667eea;
            ">
                <h3 style="margin: 0; color: #495057;">📄 {result['filename']}</h3>
                <p style="margin: 0.5rem 0 0 0; color: #6c757d;">
                    Template: {result['template_used'].replace('_', ' ').title()}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Create sub-tabs for different outputs
            sub_tabs = []
            if result['content']:
                sub_tabs.append("📃 Source Code")
            if result['sdd']:
                sub_tabs.append("📋 SDD")
            if result['mindmap']:
                sub_tabs.append("🧠 Mindmap")
            if result['summary']:
                sub_tabs.append("📝 Summary")
            
            if sub_tabs:
                content_tabs = st.tabs(sub_tabs)
                tab_index = 0
                
                # Source Code Tab
                if result['content']:
                    with content_tabs[tab_index]:
                        st.text_area(
                            f"Source Code - {result['filename']}",
                            result['content'],
                            height=250,
                            key=f"content_{result['filename']}_{id(result)}",
                            help="Original file content"
                        )
                        
                        # Enhanced file statistics
                        lines = len(result['content'].split('\n'))
                        chars = len(result['content'])
                        words = len(result['content'].split())
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown(f"""
                            <div class="metric-container">
                                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📏</div>
                                <h3 style="margin: 0; color: #495057;">{lines}</h3>
                                <p style="margin: 0; color: #6c757d;">Lines</p>
                            </div>
                            """, unsafe_allow_html=True)
                        with col2:
                            st.markdown(f"""
                            <div class="metric-container">
                                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📝</div>
                                <h3 style="margin: 0; color: #495057;">{words}</h3>
                                <p style="margin: 0; color: #6c757d;">Words</p>
                            </div>
                            """, unsafe_allow_html=True)
                        with col3:
                            st.markdown(f"""
                            <div class="metric-container">
                                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔤</div>
                                <h3 style="margin: 0; color: #495057;">{chars}</h3>
                                <p style="margin: 0; color: #6c757d;">Characters</p>
                            </div>
                            """, unsafe_allow_html=True)
                    tab_index += 1
                
                # SDD Tab
                if result['sdd']:
                    with content_tabs[tab_index]:
                        # Create two columns for markdown display and controls
                        col1, col2 = st.columns([4, 1])
                        
                        with col1:
                            st.markdown("### 📋 Software Design Document")
                            
                            # View mode selection
                            view_mode = st.radio(
                                "Display Mode:",
                                ["Rendered", "Raw"],
                                key=f"sdd_view_mode_{result['filename']}_{id(result)}",
                                horizontal=True
                            )
                            
                            if view_mode == "Rendered":
                                # Display SDD as rendered markdown
                                st.markdown(result['sdd'])
                            else:
                                # Display raw markdown
                                st.text_area(
                                    "Raw SDD Content",
                                    result['sdd'],
                                    height=400,
                                    key=f"raw_sdd_content_{result['filename']}_{id(result)}",
                                    help="Raw markdown content - you can copy this text"
                                )
                        
                        with col2:
                            st.markdown("<br><br>", unsafe_allow_html=True)
                            # Enhanced download button
                            st.download_button(
                                label="📥 Download SDD",
                                data=result['sdd'],
                                file_name=f"{result['filename']}_SDD.md",
                                mime="text/markdown",
                                key=f"download_sdd_{result['filename']}_{id(result)}",
                                help="Download as Markdown file",
                                use_container_width=True
                            )
                            
                            # Enhanced metrics
                            sdd_words = len(result['sdd'].split())
                            sdd_chars = len(result['sdd'])
                            
                            st.markdown(f"""
                            <div style="
                                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                padding: 1rem;
                                border-radius: 12px;
                                color: white;
                                text-align: center;
                                margin: 1rem 0;
                            ">
                                <h4 style="margin: 0;">📊 SDD Stats</h4>
                                <p style="margin: 0.5rem 0 0 0;">
                                    {sdd_words} words • {sdd_chars} characters
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                    tab_index += 1
                
                # Enhanced Mindmap Tab with MarkMap
                if result['mindmap']:
                    with content_tabs[tab_index]:
                        st.markdown("### 🧠 Interactive Mindmap")
                        
                        # View mode selection for mindmap
                        mindmap_view_mode = st.radio(
                            "Display Mode:",
                            ["Interactive MarkMap", "Rendered", "Raw"],
                            key=f"mindmap_view_mode_{result['filename']}_{id(result)}",
                            horizontal=True
                        )
                        
                        if mindmap_view_mode == "Interactive MarkMap":
                            # Display interactive MarkMap
                            col1, col2 = st.columns([5, 1])
                            
                            with col1:
                                try:
                                    render_markmap(
                                        result['mindmap'],
                                        width=800,
                                        height=500,
                                        unique_id=f"markmap_{result['filename'].replace('.', '_')}_{id(result)}"
                                    )
                                except Exception as e:
                                    st.error(f"Error rendering MarkMap: {str(e)}")
                                    # Fallback to markdown
                                    st.markdown("**Fallback to Markdown View:**")
                                    st.markdown(result['mindmap'])
                            
                            with col2:
                                st.markdown("<br><br><br>", unsafe_allow_html=True)
                                
                                # Enhanced download buttons
                                st.download_button(
                                    label="📥 Download MD",
                                    data=result['mindmap'],
                                    file_name=f"{result['filename']}_mindmap.md",
                                    mime="text/markdown",
                                    key=f"download_mindmap_md_{result['filename']}_{id(result)}",
                                    help="Download mindmap as Markdown",
                                    use_container_width=True
                                )
                                
                                st.download_button(
                                    label="🌐 Download HTML",
                                    data=create_markmap_download_link(result['mindmap'], result['filename']),
                                    file_name=f"{result['filename']}_mindmap.html",
                                    mime="text/html",
                                    key=f"download_mindmap_html_{result['filename']}_{id(result)}",
                                    help="Download interactive mindmap as HTML",
                                    use_container_width=True
                                )
                                
                                # Enhanced mindmap metrics
                                mindmap_lines = len(result['mindmap'].split('\n'))
                                mindmap_words = len(result['mindmap'].split())
                                
                                st.markdown(f"""
                                <div style="
                                    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                                    padding: 1rem;
                                    border-radius: 12px;
                                    color: white;
                                    text-align: center;
                                    margin: 1rem 0;
                                ">
                                    <h4 style="margin: 0;">🧠 Mindmap Stats</h4>
                                    <p style="margin: 0.5rem 0 0 0;">
                                        {mindmap_lines} lines • {mindmap_words} words
                                    </p>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        elif mindmap_view_mode == "Rendered":
                            # Display markdown as rendered text
                            col1, col2 = st.columns([4, 1])
                            
                            with col1:
                                st.markdown(result['mindmap'])
                            
                            with col2:
                                st.markdown("<br><br>", unsafe_allow_html=True)
                                # Download buttons
                                st.download_button(
                                    label="📥 Download MD",
                                    data=result['mindmap'],
                                    file_name=f"{result['filename']}_mindmap.md",
                                    mime="text/markdown",
                                    key=f"download_mindmap_rendered_{result['filename']}_{id(result)}",
                                    help="Download mindmap as Markdown",
                                    use_container_width=True
                                )
                                
                                st.download_button(
                                    label="🌐 Download HTML",
                                    data=create_markmap_download_link(result['mindmap'], result['filename']),
                                    file_name=f"{result['filename']}_mindmap.html",
                                    mime="text/html",
                                    key=f"download_mindmap_html_rendered_{result['filename']}_{id(result)}",
                                    help="Download interactive mindmap as HTML",
                                    use_container_width=True
                                )
                                
                                # Mindmap metrics
                                mindmap_lines = len(result['mindmap'].split('\n'))
                                mindmap_words = len(result['mindmap'].split())
                                
                                st.markdown(f"""
                                <div style="
                                    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                                    padding: 1rem;
                                    border-radius: 12px;
                                    color: white;
                                    text-align: center;
                                    margin: 1rem 0;
                                ">
                                    <h4 style="margin: 0;">🧠 Mindmap Stats</h4>
                                    <p style="margin: 0.5rem 0 0 0;">
                                        {mindmap_lines} lines • {mindmap_words} words
                                    </p>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        else:  # Raw view
                            # Display raw markdown text
                            col1, col2 = st.columns([4, 1])
                            
                            with col1:
                                st.text_area(
                                    "Raw Mindmap Content",
                                    result['mindmap'],
                                    height=400,
                                    key=f"raw_mindmap_content_{result['filename']}_{id(result)}",
                                    help="Raw markdown content - you can copy this text"
                                )
                            
                            with col2:
                                st.markdown("<br><br>", unsafe_allow_html=True)
                                # Download buttons
                                st.download_button(
                                    label="📥 Download MD",
                                    data=result['mindmap'],
                                    file_name=f"{result['filename']}_mindmap.md",
                                    mime="text/markdown",
                                    key=f"download_mindmap_raw_{result['filename']}_{id(result)}",
                                    help="Download mindmap as Markdown",
                                    use_container_width=True
                                )
                                
                                st.download_button(
                                    label="🌐 Download HTML",
                                    data=create_markmap_download_link(result['mindmap'], result['filename']),
                                    file_name=f"{result['filename']}_mindmap.html",
                                    mime="text/html",
                                    key=f"download_mindmap_html_raw_{result['filename']}_{id(result)}",
                                    help="Download interactive mindmap as HTML",
                                    use_container_width=True
                                )
                                
                                # Mindmap metrics
                                mindmap_lines = len(result['mindmap'].split('\n'))
                                mindmap_words = len(result['mindmap'].split())
                                
                                st.markdown(f"""
                                <div style="
                                    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                                    padding: 1rem;
                                    border-radius: 12px;
                                    color: white;
                                    text-align: center;
                                    margin: 1rem 0;
                                ">
                                    <h4 style="margin: 0;">🧠 Mindmap Stats</h4>
                                    <p style="margin: 0.5rem 0 0 0;">
                                        {mindmap_lines} lines • {mindmap_words} words
                                    </p>
                                </div>
                                """, unsafe_allow_html=True)
                    tab_index += 1
                
                # Summary Tab
                if result['summary']:
                    with content_tabs[tab_index]:
                        # Create two columns for markdown display and metrics
                        col1, col2 = st.columns([4, 1])
                        
                        with col1:
                            st.markdown("### 📝 Summary")
                            
                            # View mode selection
                            view_mode = st.radio(
                                "Display Mode:",
                                ["Rendered", "Raw"],
                                key=f"summary_view_mode_{result['filename']}_{id(result)}",
                                horizontal=True
                            )
                            
                            if view_mode == "Rendered":
                                # Display summary as rendered markdown
                                st.markdown(result['summary'])
                            else:
                                # Display raw markdown
                                st.text_area(
                                    "Raw Summary Content",
                                    result['summary'],
                                    height=250,
                                    key=f"raw_summary_content_{result['filename']}_{id(result)}",
                                    help="Raw markdown content - you can copy this text"
                                )
                        
                        with col2:
                            # Enhanced summary metrics
                            summary_words = len(result['summary'].split())
                            original_words = len(result['content'].split())
                            compression_ratio = round((1 - summary_words/original_words) * 100, 1) if original_words > 0 else 0
                            
                            st.markdown(f"""
                            <div style="
                                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                                padding: 1rem;
                                border-radius: 12px;
                                color: white;
                                text-align: center;
                                margin: 1rem 0;
                            ">
                                <h4 style="margin: 0;">📊 Summary Stats</h4>
                                <p style="margin: 0.5rem 0 0 0;">
                                    {summary_words} words<br>
                                    {compression_ratio}% compression
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Download button
                            st.download_button(
                                label="📥 Download Summary",
                                data=result['summary'],
                                file_name=f"{result['filename']}_summary.md",
                                mime="text/markdown",
                                key=f"download_summary_{result['filename']}_{id(result)}",
                                help="Download as Markdown file",
                                use_container_width=True
                            )

# Enhanced action buttons
if st.session_state.analysis_complete and st.session_state.results:
    st.markdown("---")
    
    # Action buttons header
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 2rem 0;
        text-align: center;
        border: 1px solid #dee2e6;
    ">
        <h3 style="margin: 0; color: #495057;">🎯 Quick Actions</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🔄 Analyze New Files", type="secondary", key="new_analysis", use_container_width=True):
            # Clear uploaded files but keep results until new analysis
            st.session_state.uploaded_files = []
            st.rerun()
    
    with col2:
        if st.button("📊 Re-analyze Different Template", type="secondary", key="reanalyze", use_container_width=True):
            # Keep uploaded files but trigger re-analysis
            st.session_state.analysis_complete = False
            st.rerun()
    
    with col3:
        # Enhanced export all results
        if st.button("📦 Export All Results", type="secondary", key="export_all", use_container_width=True):
            try:
                import zipfile
                import io
                
                # Create a zip file in memory
                zip_buffer = io.BytesIO()
                
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for result in st.session_state.results:
                        base_name = os.path.splitext(result['filename'])[0]
                        
                        if result.get('sdd'):
                            zip_file.writestr(f"{base_name}_SDD.md", result['sdd'])
                        if result.get('mindmap'):
                            zip_file.writestr(f"{base_name}_mindmap.md", result['mindmap'])
                            # Add interactive HTML mindmap
                            html_content = create_markmap_download_link(result['mindmap'], base_name)
                            zip_file.writestr(f"{base_name}_mindmap.html", html_content)
                        if result.get('summary'):
                            zip_file.writestr(f"{base_name}_summary.md", result['summary'])
                
                zip_buffer.seek(0)
                
                st.download_button(
                    label="📥 Download Complete Package",
                    data=zip_buffer.getvalue(),
                    file_name="CodeDocuAI_Analysis_Results.zip",
                    mime="application/zip",
                    key="download_zip_final",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"Error creating export: {str(e)}")

# Enhanced footer with information
if not st.session_state.uploaded_files and not st.session_state.analysis_complete:
    st.markdown("---")
    
    # Getting started section
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        color: white;
    ">
        <h2 style="margin: 0 0 1rem 0; text-align: center;">🚀 Getting Started</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem;">
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px;">
                <h4 style="margin: 0 0 0.5rem 0;">1. 🔑 Configure API</h4>
                <p style="margin: 0; font-size: 0.9rem;">Select your API provider and enter credentials</p>
            </div>
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px;">
                <h4 style="margin: 0 0 0.5rem 0;">2. 📋 Select Template</h4>
                <p style="margin: 0; font-size: 0.9rem;">Choose an SDD template for your project type</p>
            </div>
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px;">
                <h4 style="margin: 0 0 0.5rem 0;">3. 📁 Upload Files</h4>
                <p style="margin: 0; font-size: 0.9rem;">Select one or more code files to analyze</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Features showcase
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
        ">
            <h3 style="color: #495057; margin: 0 0 1rem 0;">🌐 API Providers</h3>
            <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                <li><strong>OpenAI</strong>: GPT-4, GPT-3.5-turbo</li>
                <li><strong>DeepSeek</strong>: deepseek-chat model</li>
                <li><strong>Aliyun</strong>: Alibaba Cloud DashScope</li>
                <li><strong>Volcengine</strong>: ByteDance AI</li>
                <li><strong>SiliconFlow</strong>: Latest DeepSeek models</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
        ">
            <h3 style="color: #495057; margin: 0 0 1rem 0;">📋 Templates</h3>
            <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                <li><strong>Standard</strong>: Comprehensive automation template</li>
                <li><strong>Microservices</strong>: For distributed architectures</li>
                <li><strong>Web Application</strong>: For web development</li>
                <li><strong>API Service</strong>: For API documentation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Professional footer
st.markdown("""
<div style="
    margin-top: 3rem;
    padding: 2rem;
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    border-radius: 15px;
    text-align: center;
    border-top: 4px solid #667eea;
    box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
">
    <h4 style="margin: 0 0 1rem 0; color: #495057;">🤖 CodeDocuAI</h4>
    <p style="margin: 0; color: #6c757d; font-size: 14px;">
        Made with ❤️ using <strong>Streamlit and Claude.ai</strong> | 
        Transform your code into documentation
    </p>
    <p style="margin: 0.5rem 0 0 0; color: #adb5bd; font-size: 12px;">
        Powered by Multiple AI Providers • Interactive Mindmaps • Professional Templates
    </p>
</div>
""", unsafe_allow_html=True)