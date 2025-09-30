# Create a flowchart showing SFT Number Generator deployment process
diagram_code = """
flowchart TD
    A[SFT Generator Project] --> B{Choose Deployment}
    
    %% Streamlit Cloud Path (Recommended)
    B -->|Recommended| C[Create GitHub Repo]
    C --> D[Push Code to GitHub]
    D --> E[Connect to Streamlit Cloud]
    E --> F[Deploy to share.streamlit.io]
    F --> G[Live Python Web App]
    
    %% GitHub Pages Path (Alternative)
    B -->|Alternative| H[Create HTML Version]
    H --> I[Push to GitHub]
    I --> J[Enable GitHub Pages]
    J --> K[Static HTML Website]
    
    %% Styling for different paths
    classDef streamlit fill:#B3E5EC,stroke:#1FB8CD,stroke-width:2px
    classDef github fill:#FFCDD2,stroke:#DB4545,stroke-width:2px
    classDef decision fill:#A5D6A7,stroke:#2E8B57,stroke-width:2px
    classDef start fill:#FFEB8A,stroke:#D2BA4C,stroke-width:2px
    
    class A start
    class B decision
    class C,D,E,F,G streamlit
    class H,I,J,K github
"""

# Create the mermaid diagram and save as both PNG and SVG
png_path, svg_path = create_mermaid_diagram(diagram_code, 'deployment_flowchart.png', 'deployment_flowchart.svg')

print(f"Flowchart saved as: {png_path} and {svg_path}")