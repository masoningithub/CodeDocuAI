# markmap_component.py - Fixed version
"""
MarkMap integration component for rendering interactive mindmaps in Streamlit.
"""

import streamlit as st
import streamlit.components.v1 as components
import json
import hashlib

def generate_markmap_html_with_id(markdown_content: str, width: int = 800, height: int = 600, unique_id: str = "markmap") -> str:
    """
    Generate HTML content with MarkMap visualization using unique IDs.
    
    Args:
        markdown_content: Markdown content to render as mindmap
        width: Width of the mindmap container
        height: Height of the mindmap container
        unique_id: Unique identifier for HTML elements
    
    Returns:
        HTML string with embedded MarkMap
    """
    
    # Escape the markdown content for JavaScript
    escaped_content = json.dumps(markdown_content)
    
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MarkMap Visualization</title>
        
        <!-- MarkMap CSS -->
        <style>
            body {{
                margin: 0;
                padding: 10px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background-color: #ffffff;
                overflow: hidden;
            }}
            
            #{unique_id} {{
                width: {width}px;
                height: {height - 20}px;
                min-height: 400px;
                border: 1px solid #e1e5e9;
                border-radius: 8px;
                background-color: #ffffff;
                display: block;
                cursor: grab;
            }}
            
            #{unique_id}:active {{
                cursor: grabbing;
            }}
            
            .markmap-toolbar-{unique_id} {{
                position: absolute;
                top: 20px;
                right: 20px;
                z-index: 1000;
                display: flex;
                flex-direction: column;
                gap: 5px;
                background: rgba(255, 255, 255, 0.9);
                padding: 8px;
                border-radius: 8px;
                backdrop-filter: blur(10px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            }}
            
            .markmap-btn-{unique_id} {{
                padding: 8px 12px;
                background: #ffffff;
                border: 1px solid #e1e5e9;
                border-radius: 6px;
                cursor: pointer;
                font-size: 12px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                transition: all 0.2s ease;
                white-space: nowrap;
            }}
            
            .markmap-btn-{unique_id}:hover {{
                background: #f8f9fa;
                box-shadow: 0 4px 8px rgba(0,0,0,0.15);
                transform: translateY(-1px);
            }}
            
            .loading-{unique_id} {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: {height - 20}px;
                font-size: 16px;
                color: #666;
                background: #f8f9fa;
                border-radius: 8px;
            }}
            
            .error-{unique_id} {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: {height - 20}px;
                font-size: 14px;
                color: #dc3545;
                background: #f8f9fa;
                border-radius: 8px;
                text-align: center;
                padding: 20px;
            }}
        </style>
    </head>
    <body>
        <div id="loading-{unique_id}" class="loading-{unique_id}">
            <div>🧠 Loading interactive mindmap...</div>
        </div>
        <svg id="{unique_id}" style="display: none;"></svg>
        
        <div class="markmap-toolbar-{unique_id}">
            <button class="markmap-btn-{unique_id}" onclick="fitMap_{unique_id}()" title="Fit to screen">🔍 Fit</button>
            <button class="markmap-btn-{unique_id}" onclick="resetZoom_{unique_id}()" title="Reset zoom">↻ Reset</button>
            <button class="markmap-btn-{unique_id}" onclick="centerMap_{unique_id}()" title="Center map">🎯 Center</button>
            <button class="markmap-btn-{unique_id}" onclick="expandAll_{unique_id}()" title="Expand all nodes">📖 Expand</button>
            <button class="markmap-btn-{unique_id}" onclick="collapseAll_{unique_id}()" title="Collapse all nodes">📕 Collapse</button>
            <button class="markmap-btn-{unique_id}" onclick="downloadSVG_{unique_id}()" title="Download as SVG">💾 SVG</button>
        </div>

        <!-- MarkMap Libraries - Updated versions -->
        <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
        <script src="https://cdn.jsdelivr.net/npm/markmap-view@0.16.0"></script>
        <script src="https://cdn.jsdelivr.net/npm/markmap-lib@0.16.0"></script>

        <script>
            let mm_{unique_id};
            let svg_{unique_id};
            let initialData_{unique_id};
            
            async function renderMarkmap_{unique_id}() {{
                try {{
                    console.log('Starting markmap rendering for {unique_id}');
                    const markdown = {escaped_content};
                    
                    // Verify MarkMap libraries are loaded
                    if (!window.markmap) {{
                        throw new Error('MarkMap libraries not loaded');
                    }}
                    
                    // Transform markdown to markmap data
                    const {{ Transformer }} = window.markmap;
                    const transformer = new Transformer();
                    const {{ root, features }} = transformer.transform(markdown);
                    
                    // Store initial data
                    initialData_{unique_id} = root;
                    
                    // Create markmap instance
                    svg_{unique_id} = d3.select('#{unique_id}');
                    const {{ Markmap, loadCSS, loadJS }} = window.markmap;
                    
                    // Load required assets
                    if (features.styles) {{
                        await loadCSS(features.styles);
                    }}
                    if (features.scripts) {{
                        await loadJS(features.scripts);
                    }}
                    
                    // Create and render markmap with enhanced options
                    mm_{unique_id} = Markmap.create(svg_{unique_id}.node(), {{
                        duration: 300,
                        maxWidth: 250,
                        spacingVertical: 10,
                        spacingHorizontal: 120,
                        autoFit: true,
                        pan: true,
                        zoom: true,
                        colorFreezeLevel: 6,
                        paddingX: 8,
                        paddingY: 8,
                        // Enable interactive features
                        fitRatio: 0.9,
                        panEnabled: true,
                        zoomEnabled: true,
                        // Remove initial expand level limitation
                        initialExpandLevel: -1,  // -1 means no automatic expansion limit
                        // Set zoom constraints
                        zoom: {{
                            enabled: true,
                            scaleExtent: [0.1, 3],
                            wheelDelta: function(event) {{
                                return -event.deltaY * (event.deltaMode === 1 ? 0.05 : event.deltaMode ? 1 : 0.002);
                            }}
                        }}
                    }});
                    
                    // Set data and enable interactions
                    mm_{unique_id}.setData(root);
                    
                    // Hide loading and show mindmap
                    document.getElementById('loading-{unique_id}').style.display = 'none';
                    document.getElementById('{unique_id}').style.display = 'block';
                    
                    // Initial fit with delay to ensure proper rendering
                    setTimeout(() => {{
                        if (mm_{unique_id}) {{
                            mm_{unique_id}.fit();
                        }}
                    }}, 500);
                    
                    // Add keyboard shortcuts
                    document.addEventListener('keydown', function(event) {{
                        if (event.target.closest('#{unique_id}')) {{
                            switch(event.key) {{
                                case 'f':
                                case 'F':
                                    event.preventDefault();
                                    fitMap_{unique_id}();
                                    break;
                                case 'r':
                                case 'R':
                                    event.preventDefault();
                                    resetZoom_{unique_id}();
                                    break;
                                case 'c':
                                case 'C':
                                    event.preventDefault();
                                    centerMap_{unique_id}();
                                    break;
                                case 'e':
                                case 'E':
                                    event.preventDefault();
                                    expandAll_{unique_id}();
                                    break;
                                case 'q':
                                case 'Q':
                                    event.preventDefault();
                                    collapseAll_{unique_id}();
                                    break;
                            }}
                        }}
                    }});
                    
                    console.log('MarkMap rendered successfully for {unique_id}');
                    
                }} catch (error) {{
                    console.error('Error rendering markmap:', error);
                    const loadingElement = document.getElementById('loading-{unique_id}');
                    if (loadingElement) {{
                        loadingElement.innerHTML = `
                            <div class="error-{unique_id}">
                                <div>
                                    ❌ Error loading mindmap:<br>
                                    <small>${{error.message}}</small><br><br>
                                    <em>Try refreshing the page or check browser console for details</em>
                                </div>
                            </div>
                        `;
                        loadingElement.className = 'error-{unique_id}';
                    }}
                }}
            }}
            
            function fitMap_{unique_id}() {{
                console.log('Fitting map for {unique_id}');
                if (mm_{unique_id}) {{
                    mm_{unique_id}.fit();
                }}
            }}
            
            function resetZoom_{unique_id}() {{
                console.log('Resetting zoom for {unique_id}');
                if (mm_{unique_id} && initialData_{unique_id}) {{
                    mm_{unique_id}.setData(initialData_{unique_id});
                    setTimeout(() => {{
                        mm_{unique_id}.fit();
                    }}, 100);
                }}
            }}
            
            function centerMap_{unique_id}() {{
                console.log('Centering map for {unique_id}');
                if (mm_{unique_id}) {{
                    const svg = svg_{unique_id}.node();
                    const bbox = svg.getBBox();
                    const viewBox = `${{bbox.x}} ${{bbox.y}} ${{bbox.width}} ${{bbox.height}}`;
                    svg_{unique_id}.attr('viewBox', viewBox);
                }}
            }}
            
            function expandAll_{unique_id}() {{
                console.log('Expanding all nodes for {unique_id}');
                if (mm_{unique_id} && initialData_{unique_id}) {{
                    // Function to recursively expand all nodes at all levels
                    function expandNode(node) {{
                        // Always ensure the node is expanded
                        if (node.payload) {{
                            delete node.payload.fold; // Remove any fold property
                        }} else {{
                            node.payload = {{}};
                        }}
                        
                        // Recursively expand all children
                        if (node.children && node.children.length > 0) {{
                            node.children.forEach(child => {{
                                expandNode(child);
                            }});
                        }}
                    }}
                    
                    // Create a deep copy of the initial data
                    const expandedData = JSON.parse(JSON.stringify(initialData_{unique_id}));
                    expandNode(expandedData);
                    
                    // Force re-render with completely expanded data
                    mm_{unique_id}.setData(expandedData);
                    
                    // Additional method: manually trigger expansion using MarkMap's internal methods
                    setTimeout(() => {{
                        try {{
                            // Try to access MarkMap's internal state and force expansion
                            const state = mm_{unique_id}.state;
                            if (state && state.data) {{
                                // Walk through all nodes and ensure they're expanded
                                function forceExpand(nodeData) {{
                                    if (nodeData.payload) {{
                                        nodeData.payload.fold = 0; // 0 = expanded
                                    }}
                                    if (nodeData.children) {{
                                        nodeData.children.forEach(forceExpand);
                                    }}
                                }}
                                forceExpand(state.data);
                                
                                // Trigger a re-render
                                mm_{unique_id}.setData(state.data);
                            }}
                        }} catch (e) {{
                            console.log('Fallback expansion method used');
                        }}
                        
                        // Fit to screen after expansion
                        setTimeout(() => {{
                            mm_{unique_id}.fit();
                        }}, 100);
                    }}, 100);
                }}
            }}
            
            function collapseAll_{unique_id}() {{
                console.log('Collapsing all nodes for {unique_id}');
                if (mm_{unique_id} && initialData_{unique_id}) {{
                    // Function to recursively collapse all nodes except root
                    function collapseNode(node, isRoot = false) {{
                        if (!isRoot) {{
                            // Collapse this node (except root)
                            node.payload = node.payload || {{}};
                            node.payload.fold = 1; // 1 means collapsed
                        }}
                        
                        // Process children
                        if (node.children && node.children.length > 0) {{
                            node.children.forEach(child => {{
                                collapseNode(child, false);
                            }});
                        }}
                    }}
                    
                    // Create a deep copy of the initial data
                    const collapsedData = JSON.parse(JSON.stringify(initialData_{unique_id}));
                    
                    // Keep root expanded but collapse all its children
                    if (collapsedData.children) {{
                        collapsedData.children.forEach(child => {{
                            collapseNode(child, false);
                        }});
                    }}
                    
                    // Update the markmap with collapsed data
                    mm_{unique_id}.setData(collapsedData);
                    
                    // Fit to screen after collapse
                    setTimeout(() => {{
                        mm_{unique_id}.fit();
                    }}, 100);
                }}
            }}
            
            function downloadSVG_{unique_id}() {{
                console.log('Downloading SVG for {unique_id}');
                if (svg_{unique_id}) {{
                    try {{
                        const svgNode = svg_{unique_id}.node();
                        const serializer = new XMLSerializer();
                        let svgData = serializer.serializeToString(svgNode);
                        
                        // Add XML declaration and styling
                        svgData = `<?xml version="1.0" encoding="UTF-8"?>\\n${{svgData}}`;
                        
                        const svgBlob = new Blob([svgData], {{type: "image/svg+xml;charset=utf-8"}});
                        const svgUrl = URL.createObjectURL(svgBlob);
                        const downloadLink = document.createElement("a");
                        downloadLink.href = svgUrl;
                        downloadLink.download = "mindmap_{unique_id}.svg";
                        document.body.appendChild(downloadLink);
                        downloadLink.click();
                        document.body.removeChild(downloadLink);
                        URL.revokeObjectURL(svgUrl);
                    }} catch (error) {{
                        console.error('Error downloading SVG:', error);
                        alert('Error downloading SVG: ' + error.message);
                    }}
                }}
            }}
            
            // Initialize when DOM is loaded
            if (document.readyState === 'loading') {{
                document.addEventListener('DOMContentLoaded', renderMarkmap_{unique_id});
            }} else {{
                renderMarkmap_{unique_id}();
            }}
            
            // Handle window resize
            window.addEventListener('resize', function() {{
                if (mm_{unique_id}) {{
                    setTimeout(() => {{
                        mm_{unique_id}.fit();
                    }}, 300);
                }}
            }});
        </script>
    </body>
    </html>
    """
    
    return html_template

def generate_markmap_html(markdown_content: str, width: int = 800, height: int = 600) -> str:
    """
    Generate HTML content with MarkMap visualization (backward compatibility).
    """
    return generate_markmap_html_with_id(markdown_content, width, height, "markmap")

def render_markmap(markdown_content: str, width: int = 800, height: int = 600, unique_id: str = None) -> None:
    """
    Render MarkMap component in Streamlit.
    
    Args:
        markdown_content: Markdown content to visualize
        width: Width of the component
        height: Height of the component
        unique_id: Unique identifier for the component (used in HTML, not as Streamlit key)
    """
    
    if not markdown_content or not markdown_content.strip():
        st.warning("⚠️ No mindmap content to display")
        return
    
    # Generate unique ID for HTML elements if not provided
    if unique_id is None:
        content_hash = hashlib.md5(markdown_content.encode()).hexdigest()[:8]
        unique_id = f"markmap_{content_hash}"
    
    # Generate HTML with unique IDs
    html_content = generate_markmap_html_with_id(markdown_content, width, height, unique_id)
    
    # Render component without key parameter
    components.html(
        html_content,
        width=width,
        height=height,
        scrolling=False  # Changed to False to prevent scroll issues
    )

def create_markmap_download_link(markdown_content: str, filename: str = "mindmap") -> str:
    """
    Create a standalone HTML file for MarkMap that can be downloaded.
    
    Args:
        markdown_content: Markdown content for the mindmap
        filename: Base filename for the download
    
    Returns:
        HTML content as string
    """
    
    # Escape the markdown content for JavaScript
    escaped_content = json.dumps(markdown_content)
    
    full_page_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Interactive Mindmap - {filename}</title>
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                height: 100vh;
                width: 100vw;
                overflow: hidden;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background-color: #ffffff;
            }}
            
            #markmap-standalone {{
                width: 100vw;
                height: 100vh;
                display: block;
                background-color: #ffffff;
                cursor: grab;
            }}
            
            #markmap-standalone:active {{
                cursor: grabbing;
            }}
            
            .markmap-toolbar-standalone {{
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 1000;
                display: flex;
                flex-direction: column;
                gap: 8px;
                background: rgba(255, 255, 255, 0.95);
                padding: 12px;
                border-radius: 12px;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            }}
            
            .markmap-btn-standalone {{
                padding: 10px 16px;
                background: #ffffff;
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                cursor: pointer;
                font-size: 14px;
                font-weight: 500;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                transition: all 0.3s ease;
                min-width: 120px;
                text-align: center;
                white-space: nowrap;
            }}
            
            .markmap-btn-standalone:hover {{
                background: #f8f9fa;
                border-color: #007bff;
                box-shadow: 0 6px 20px rgba(0,0,0,0.2);
                transform: translateY(-2px);
            }}
            
            .loading-standalone {{
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 18px;
                color: #666;
                z-index: 999;
                text-align: center;
            }}
            
            .title-overlay {{
                position: fixed;
                top: 20px;
                left: 20px;
                z-index: 1000;
                background: rgba(255, 255, 255, 0.95);
                padding: 12px 20px;
                border-radius: 12px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                backdrop-filter: blur(10px);
                font-size: 16px;
                font-weight: 600;
                color: #333;
            }}
            
            .help-overlay {{
                position: fixed;
                bottom: 20px;
                left: 20px;
                z-index: 1000;
                background: rgba(255, 255, 255, 0.9);
                padding: 8px 12px;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                font-size: 12px;
                color: #666;
                max-width: 300px;
            }}
        </style>
    </head>
    <body>
        <div id="loading-standalone" class="loading-standalone">
            <div>🧠 Loading interactive mindmap...</div>
            <div style="margin-top: 10px; font-size: 14px;">Please wait...</div>
        </div>
        <div class="title-overlay">📄 {filename} - Interactive Mindmap</div>
        <div class="help-overlay">
            <strong>Controls:</strong><br>
            • Drag to pan<br>
            • Scroll to zoom<br>
            • Click nodes to expand/collapse<br>
            • Press F to fit, R to reset, C to center<br>
            • Press E to expand all, Q to collapse all
        </div>
        <svg id="markmap-standalone" style="display: none;"></svg>
        
        <div class="markmap-toolbar-standalone">
            <button class="markmap-btn-standalone" onclick="fitMap_standalone()" title="Fit to screen (F)">🔍 Fit to Screen</button>
            <button class="markmap-btn-standalone" onclick="resetZoom_standalone()" title="Reset zoom (R)">↻ Reset View</button>
            <button class="markmap-btn-standalone" onclick="centerMap_standalone()" title="Center map (C)">🎯 Center Map</button>
            <button class="markmap-btn-standalone" onclick="expandAll_standalone()" title="Expand all nodes (E)">📖 Expand All</button>
            <button class="markmap-btn-standalone" onclick="collapseAll_standalone()" title="Collapse all nodes (Q)">📕 Collapse All</button>
            <button class="markmap-btn-standalone" onclick="downloadSVG_standalone()" title="Download as SVG">💾 Download SVG</button>
        </div>

        <!-- MarkMap Libraries - Updated versions -->
        <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
        <script src="https://cdn.jsdelivr.net/npm/markmap-view@0.16.0"></script>
        <script src="https://cdn.jsdelivr.net/npm/markmap-lib@0.16.0"></script>

        <script>
            let mm_standalone;
            let svg_standalone;
            let initialData_standalone;
            
            async function renderMarkmap_standalone() {{
                try {{
                    console.log('Starting standalone markmap rendering');
                    const markdown = {escaped_content};
                    
                    // Verify MarkMap libraries are loaded
                    if (!window.markmap) {{
                        throw new Error('MarkMap libraries not loaded');
                    }}
                    
                    // Transform markdown to markmap data
                    const {{ Transformer }} = window.markmap;
                    const transformer = new Transformer();
                    const {{ root, features }} = transformer.transform(markdown);
                    
                    // Store initial data
                    initialData_standalone = root;
                    
                    // Create markmap instance
                    svg_standalone = d3.select('#markmap-standalone');
                    const {{ Markmap, loadCSS, loadJS }} = window.markmap;
                    
                    // Load required assets
                    if (features.styles) {{
                        await loadCSS(features.styles);
                    }}
                    if (features.scripts) {{
                        await loadJS(features.scripts);
                    }}
                    
                    // Create and render markmap with better sizing
                    mm_standalone = Markmap.create(svg_standalone.node(), {{
                        duration: 500,
                        maxWidth: 280,
                        spacingVertical: 12,
                        spacingHorizontal: 150,
                        autoFit: true,
                        pan: true,
                        zoom: true,
                        colorFreezeLevel: 6,
                        paddingX: 40,
                        paddingY: 40,
                        initialExpandLevel: -1,  // -1 means no automatic expansion limit
                        // Enhanced zoom and pan settings
                        fitRatio: 0.85,
                        panEnabled: true,
                        zoomEnabled: true
                    }});
                    
                    mm_standalone.setData(root);
                    
                    // Hide loading and show mindmap
                    document.getElementById('loading-standalone').style.display = 'none';
                    document.getElementById('markmap-standalone').style.display = 'block';
                    
                    // Fit after a delay to ensure proper rendering
                    setTimeout(() => {{
                        if (mm_standalone) {{
                            mm_standalone.fit();
                        }}
                    }}, 800);
                    
                    // Add keyboard shortcuts
                    document.addEventListener('keydown', function(event) {{
                        switch(event.key.toLowerCase()) {{
                            case 'f':
                                event.preventDefault();
                                fitMap_standalone();
                                break;
                            case 'r':
                                event.preventDefault();
                                resetZoom_standalone();
                                break;
                            case 'c':
                                event.preventDefault();
                                centerMap_standalone();
                                break;
                            case 'e':
                                event.preventDefault();
                                expandAll_standalone();
                                break;
                            case 'q':
                                event.preventDefault();
                                collapseAll_standalone();
                                break;
                        }}
                    }});
                    
                    console.log('Standalone MarkMap rendered successfully');
                    
                }} catch (error) {{
                    console.error('Error rendering standalone markmap:', error);
                    const loadingElement = document.getElementById('loading-standalone');
                    if (loadingElement) {{
                        loadingElement.innerHTML = `
                            <div style="color: #dc3545; text-align: center;">
                                ❌ Error loading mindmap:<br>
                                <small>${{error.message}}</small><br><br>
                                <em>Try refreshing the page or check browser console for details</em>
                            </div>
                        `;
                    }}
                }}
            }}
            
            function fitMap_standalone() {{
                console.log('Fitting standalone map');
                if (mm_standalone) {{
                    mm_standalone.fit();
                }}
            }}
            
            function resetZoom_standalone() {{
                console.log('Resetting standalone zoom');
                if (mm_standalone && initialData_standalone) {{
                    mm_standalone.setData(initialData_standalone);
                    setTimeout(() => {{
                        mm_standalone.fit();
                    }}, 200);
                }}
            }}
            
            function centerMap_standalone() {{
                console.log('Centering standalone map');
                if (mm_standalone) {{
                    const svg = svg_standalone.node();
                    const bbox = svg.getBBox();
                    const viewBox = `${{bbox.x}} ${{bbox.y}} ${{bbox.width}} ${{bbox.height}}`;
                    svg_standalone.attr('viewBox', viewBox);
                }}
            }}
            
            function expandAll_standalone() {{
                console.log('Expanding all nodes in standalone');
                if (mm_standalone && initialData_standalone) {{
                    // Function to recursively expand all nodes at all levels
                    function expandNode(node) {{
                        // Always ensure the node is expanded
                        if (node.payload) {{
                            delete node.payload.fold; // Remove any fold property
                        }} else {{
                            node.payload = {{}};
                        }}
                        
                        // Recursively expand all children
                        if (node.children && node.children.length > 0) {{
                            node.children.forEach(child => {{
                                expandNode(child);
                            }});
                        }}
                    }}
                    
                    // Create a deep copy of the initial data
                    const expandedData = JSON.parse(JSON.stringify(initialData_standalone));
                    expandNode(expandedData);
                    
                    // Force re-render with completely expanded data
                    mm_standalone.setData(expandedData);
                    
                    // Additional method: manually trigger expansion using MarkMap's internal methods
                    setTimeout(() => {{
                        try {{
                            // Try to access MarkMap's internal state and force expansion
                            const state = mm_standalone.state;
                            if (state && state.data) {{
                                // Walk through all nodes and ensure they're expanded
                                function forceExpand(nodeData) {{
                                    if (nodeData.payload) {{
                                        nodeData.payload.fold = 0; // 0 = expanded
                                    }}
                                    if (nodeData.children) {{
                                        nodeData.children.forEach(forceExpand);
                                    }}
                                }}
                                forceExpand(state.data);
                                
                                // Trigger a re-render
                                mm_standalone.setData(state.data);
                            }}
                        }} catch (e) {{
                            console.log('Fallback expansion method used');
                        }}
                        
                        // Fit to screen after expansion
                        setTimeout(() => {{
                            mm_standalone.fit();
                        }}, 100);
                    }}, 100);
                }}
            }}
            
            function collapseAll_standalone() {{
                console.log('Collapsing all nodes in standalone');
                if (mm_standalone && initialData_standalone) {{
                    // Function to recursively collapse all nodes except root
                    function collapseNode(node, isRoot = false) {{
                        if (!isRoot) {{
                            // Collapse this node (except root)
                            node.payload = node.payload || {{}};
                            node.payload.fold = 1; // 1 means collapsed
                        }}
                        
                        // Process children
                        if (node.children && node.children.length > 0) {{
                            node.children.forEach(child => {{
                                collapseNode(child, false);
                            }});
                        }}
                    }}
                    
                    // Create a deep copy of the initial data
                    const collapsedData = JSON.parse(JSON.stringify(initialData_standalone));
                    
                    // Keep root expanded but collapse all its children
                    if (collapsedData.children) {{
                        collapsedData.children.forEach(child => {{
                            collapseNode(child, false);
                        }});
                    }}
                    
                    // Update the markmap with collapsed data
                    mm_standalone.setData(collapsedData);
                    
                    // Fit to screen after collapse
                    setTimeout(() => {{
                        mm_standalone.fit();
                    }}, 100);
                }}
            }}
            
            function downloadSVG_standalone() {{
                console.log('Downloading standalone SVG');
                if (svg_standalone) {{
                    try {{
                        const svgNode = svg_standalone.node();
                        const serializer = new XMLSerializer();
                        let svgData = serializer.serializeToString(svgNode);
                        
                        // Add XML declaration and styling
                        svgData = `<?xml version="1.0" encoding="UTF-8"?>\\n${{svgData}}`;
                        
                        const svgBlob = new Blob([svgData], {{type: "image/svg+xml;charset=utf-8"}});
                        const svgUrl = URL.createObjectURL(svgBlob);
                        const downloadLink = document.createElement("a");
                        downloadLink.href = svgUrl;
                        downloadLink.download = "mindmap_{filename}.svg";
                        document.body.appendChild(downloadLink);
                        downloadLink.click();
                        document.body.removeChild(downloadLink);
                        URL.revokeObjectURL(svgUrl);
                    }} catch (error) {{
                        console.error('Error downloading SVG:', error);
                        alert('Error downloading SVG: ' + error.message);
                    }}
                }}
            }}
            
            // Initialize when DOM is loaded and when window resizes
            if (document.readyState === 'loading') {{
                document.addEventListener('DOMContentLoaded', renderMarkmap_standalone);
            }} else {{
                renderMarkmap_standalone();
            }}
            
            window.addEventListener('resize', () => {{
                if (mm_standalone) {{
                    setTimeout(() => {{
                        mm_standalone.fit();
                    }}, 500);
                }}
            }});
        </script>
    </body>
    </html>
    """
    
    return full_page_html

# Test function for development
def test_markmap():
    """Test function to verify MarkMap integration."""
    sample_markdown = """
# Software Architecture

## Frontend
- React Components
  - Header Component
  - Navigation
  - Content Area
- State Management
  - Redux Store
  - Actions
  - Reducers

## Backend
- API Layer
  - REST Endpoints
  - Authentication
  - Rate Limiting
- Business Logic
  - User Management
  - Data Processing
- Database
  - PostgreSQL
  - Migrations
  - Indexing

## DevOps
- CI/CD Pipeline
- Docker Containers
- Kubernetes Deployment
"""
    
    st.title("MarkMap Test")
    render_markmap(sample_markdown, width=800, height=600)

if __name__ == "__main__":
    test_markmap()