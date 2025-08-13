Add another page for Artifacts where the output from the SDLC can be stored. 
Perhaps a tab for each part of the SDLC? with a list of Artifacts and a link to download them. THe code artifacts may become quite large, so perhaps a folder tree would work better for them? 

The folder structure is not going to be shown to the user and just used for storage. 
The table containing the name and hyperlink "flattens" the folders to present all the files for that phase in a simple table. 
It is just the Development phase where the folder structure is a better way to browse the files and structure.
 

SDLC Phases as Tabs
Requirements Gathering
Role: Business Analyst
Artifacts: Requirements Document, Use Cases
Design
Role: System Architect
Artifacts: Architecture Diagrams, Design Models
Development
Role: Developer
Artifacts: Source Code, Code Documentation
Testing
Role: QA Engineer
Artifacts: Test Plans, Test Cases, Test Scripts
Deployment
Role: DevOps Engineer
Artifacts: Deployment Scripts, Configuration Files
Maintenance
Role: DevOps Engineer
Artifacts: Monitoring Reports, Logs

Artifact Types
Requirements Gathering: Markdown files (md), Word documents
Design: Images (e.g., PNG, JPEG), PDF files, Markdown files
Development: Code files (e.g., Java, Python), Markdown files for documentation
Testing: Markdown files for test plans, scripts (e.g., shell scripts), Excel files for test cases
Deployment: Scripts (e.g., shell scripts, YAML files), configuration files (e.g., JSON, XML)
Maintenance: Logs (text files), Markdown files for reports

Folder Structure
The folder structure should reflect the project structure, with a potential dynamic hierarchy defined by the Architect for code artifacts. Here’s a suggested structure:
/project-root
    /requirements
        /gathering
            - requirements.md
            - use_cases.md
    /design
        /architecture
            - architecture_diagram.png
            - design_model.md
    /development
        /source_code
            - main.java
            - utils.py
        /documentation
            - code_documentation.md
    /testing
        /test_plans
            - test_plan.md
        /test_cases
            - test_cases.xlsx
        /test_scripts
            - test_script.sh
    /deployment
        - deployment_script.sh
        - config.json
    /maintenance
        - monitoring_report.md
        - logs.txt

Download Links
The download links should point to files hosted on a server. A suggested URL structure could be:
https://yourserver.com/artifacts/{phase}/{artifact_name}

For example:
https://yourserver.com/artifacts/requirements/gathering/requirements.md

Document Table Example
You can create a table to display the documents with hyperlinks for downloading:

Document Name	Download Link
Requirements Document	Download
Use Cases	Download
Architecture Diagram	Download
Source Code	Download
Test Plan	Download
Deployment Script	Download

Preview Window
For file types that support preview (like Markdown, images, and PDFs), you can implement a modal or a dedicated preview section on your web interface to display the content without downloading.

Implementation Notes
Each tab will display the relevant documents in a table format, except for the Development tab, which will show a folder structure for better navigation.
The download links will point to the server where the files are stored.
The UI can include a modal or preview window for supported file types to allow users to view content without downloading.