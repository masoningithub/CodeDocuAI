# sdd_templates.py
"""
Enhanced SDD (Software Design Document) templates with multiple layers and subsections.
"""

SDD_TEMPLATES = {
    "standard": {
        "name": "Standard Automation SDD",
        "description": "Automation used template",
        "sections": [
            "1. Overview",
            "1.1 Purpose",
            "1.2 References",

            "2. Solution Overview",
            "2.1 Solution Feature",
            "2.1.1 Automation Type",
            "2.1.2 Technologies Involved",
            "2.2 Workflow",
            "2.2.1 Restriction",
            "2.2.2 Solution Diagram",
            "2.2.3 To-Be workflow",
            "2.2.4 Input and Output",
            "2.2.5 Data Items in Configuration File",

            "3. Design",
            "3.1 Module Design",
            "3.2 Module Detail",
            "3.3 Data Structure Design",

            "4. Exception Handling Design",
            "4.1 Exception Categories",
            "4.2 System Exception",
            "4.3 Business Exception",
            "4.4 Exception Handling Process",

            "5. Security Design",
            "5.1 System/Application Credentials",
            "5.2 Data Transmission"
        ]
    },
    
    "microservices": {
        "name": "Microservices SDD",
        "description": "Template for microservices architecture documentation",
        "sections": [
            "1. Executive Summary",
            "1.1 Business Context",
            "1.2 Solution Overview",
            "1.3 Key Benefits",
            
            "2. Microservices Architecture",
            "2.1 Service Decomposition",
            "2.1.1 Domain Boundaries",
            "2.1.2 Service Identification",
            "2.1.3 Service Dependencies",
            "2.2 Communication Patterns",
            "2.2.1 Synchronous Communication",
            "2.2.2 Asynchronous Messaging",
            "2.2.3 Event-Driven Architecture",
            "2.3 Data Management",
            "2.3.1 Database per Service",
            "2.3.2 Data Consistency Patterns",
            "2.3.3 Transaction Management",
            
            "3. Individual Service Design",
            "3.1 Service Specifications",
            "3.1.1 Service A Design",
            "3.1.2 Service B Design",
            "3.1.3 Service C Design",
            "3.2 API Contracts",
            "3.2.1 RESTful APIs",
            "3.2.2 GraphQL Interfaces",
            "3.2.3 Event Schemas",
            
            "4. Cross-Cutting Concerns",
            "4.1 Service Discovery",
            "4.2 Load Balancing",
            "4.3 Circuit Breakers",
            "4.4 Distributed Tracing",
            "4.5 Centralized Logging",
            
            "5. DevOps and Deployment",
            "5.1 CI/CD Pipeline",
            "5.1.1 Build Automation",
            "5.1.2 Testing Strategy",
            "5.1.3 Deployment Automation",
            "5.2 Container Strategy",
            "5.2.1 Docker Configuration",
            "5.2.2 Kubernetes Orchestration",
            "5.2.3 Service Mesh",
            
            "6. Monitoring and Observability",
            "6.1 Health Checks",
            "6.2 Metrics Collection",
            "6.3 Alerting Strategy",
            "6.4 Performance Monitoring"
        ]
    },
    
    "web_application": {
        "name": "Web Application SDD",
        "description": "Template for web application development",
        "sections": [
            "1. Application Overview",
            "1.1 Purpose and Goals",
            "1.2 Target Users",
            "1.3 Success Criteria",
            
            "2. User Experience Design",
            "2.1 User Interface Design",
            "2.1.1 Wireframes",
            "2.1.2 Visual Design",
            "2.1.3 Responsive Design",
            "2.2 User Journey",
            "2.2.1 User Flows",
            "2.2.2 Navigation Structure",
            "2.2.3 Accessibility Requirements",
            
            "3. Frontend Architecture",
            "3.1 Client-Side Framework",
            "3.1.1 Component Architecture",
            "3.1.2 State Management",
            "3.1.3 Routing Strategy",
            "3.2 Build and Bundle",
            "3.2.1 Asset Pipeline",
            "3.2.2 Code Splitting",
            "3.2.3 Performance Optimization",
            
            "4. Backend Architecture",
            "4.1 Server Architecture",
            "4.1.1 Application Server",
            "4.1.2 Web Server Configuration",
            "4.1.3 Load Balancing",
            "4.2 API Layer",
            "4.2.1 REST API Design",
            "4.2.2 Authentication/Authorization",
            "4.2.3 Rate Limiting",
            "4.3 Business Logic Layer",
            "4.3.1 Service Classes",
            "4.3.2 Data Validation",
            "4.3.3 Error Handling",
            
            "5. Data Layer",
            "5.1 Database Design",
            "5.1.1 Entity Relationship Model",
            "5.1.2 Normalization Strategy",
            "5.1.3 Indexing Plan",
            "5.2 Data Access Layer",
            "5.2.1 ORM Configuration",
            "5.2.2 Query Optimization",
            "5.2.3 Connection Management",
            
            "6. Security Implementation",
            "6.1 Web Security",
            "6.1.1 HTTPS Configuration",
            "6.1.2 CSRF Protection",
            "6.1.3 XSS Prevention",
            "6.2 Authentication",
            "6.2.1 User Registration",
            "6.2.2 Login Process",
            "6.2.3 Password Security",
            "6.3 Authorization",
            "6.3.1 Role-Based Access",
            "6.3.2 Permission System",
            "6.3.3 Session Management"
        ]
    },
    
    "api_service": {
        "name": "API Service SDD",
        "description": "Template for API service documentation",
        "sections": [
            "1. API Overview",
            "1.1 Service Purpose",
            "1.2 API Version",
            "1.3 Service Level Agreement",
            
            "2. API Design",
            "2.1 RESTful Principles",
            "2.1.1 Resource Identification",
            "2.1.2 HTTP Methods Usage",
            "2.1.3 Status Code Conventions",
            "2.2 Endpoint Specification",
            "2.2.1 Public Endpoints",
            "2.2.2 Protected Endpoints",
            "2.2.3 Admin Endpoints",
            "2.3 Request/Response Format",
            "2.3.1 JSON Schema",
            "2.3.2 Error Response Format",
            "2.3.3 Pagination Strategy",
            
            "3. Authentication & Authorization",
            "3.1 Authentication Methods",
            "3.1.1 API Key Authentication",
            "3.1.2 OAuth 2.0 Integration",
            "3.1.3 JWT Token Handling",
            "3.2 Authorization Framework",
            "3.2.1 Role-Based Access Control",
            "3.2.2 Scope Management",
            "3.2.3 Rate Limiting",
            
            "4. Data Processing",
            "4.1 Input Validation",
            "4.1.1 Schema Validation",
            "4.1.2 Business Rule Validation",
            "4.1.3 Sanitization",
            "4.2 Data Transformation",
            "4.2.1 Input Processing",
            "4.2.2 Output Formatting",
            "4.2.3 Data Enrichment",
            
            "5. Error Handling",
            "5.1 Error Classification",
            "5.2 Error Response Structure",
            "5.3 Logging Strategy",
            
            "6. Performance & Scalability",
            "6.1 Caching Strategy",
            "6.2 Database Optimization",
            "6.3 Horizontal Scaling",
            
            "7. API Documentation",
            "7.1 OpenAPI Specification",
            "7.2 Interactive Documentation",
            "7.3 SDK Generation"
        ]
    }
}

def get_template_sections(template_name: str) -> list:
    """
    Get the sections for a specific SDD template.
    
    Args:
        template_name: Name of the template ('standard', 'microservices', etc.)
        
    Returns:
        List of section names with hierarchical numbering
    """
    if template_name not in SDD_TEMPLATES:
        return SDD_TEMPLATES['standard']['sections']
    
    return SDD_TEMPLATES[template_name]['sections']

def get_available_templates() -> dict:
    """
    Get all available template names and descriptions.
    
    Returns:
        Dictionary with template names as keys and descriptions as values
    """
    return {
        name: template['description'] 
        for name, template in SDD_TEMPLATES.items()
    }

def generate_sdd_outline(template_name: str = 'standard') -> str:
    """
    Generate a formatted outline for the specified SDD template.
    
    Args:
        template_name: Name of the template to use
        
    Returns:
        Formatted string outline of the SDD structure
    """
    if template_name not in SDD_TEMPLATES:
        template_name = 'standard'
    
    template = SDD_TEMPLATES[template_name]
    sections = template['sections']
    
    outline = f"# {template['name']}\n"
    outline += f"## {template['description']}\n\n"
    outline += "### Document Structure:\n\n"
    
    for section in sections:
        level = section.count('.') + 1
        indent = "  " * (level - 1)
        outline += f"{indent}- {section}\n"
    
    return outline