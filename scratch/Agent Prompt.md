# Objective
Reasoning behind change:Gathered all project objectives under a clear 'Objective' heading for scannable clarity and so GPT-5 recognizes the high-level task before reading details.
Design a reusable, modular pattern for vibe-coding that supports the entire software development lifecycle (SDLC).
# Checklist
Reasoning behind change:Applied GPT-5 best practice of requiring a short, high-level conceptual checklist at the start. This fosters improved planning, more predictable responses, and promotes reflection before execution.
Begin with a concise checklist (3-7 bullets) of what you will do; keep items conceptual, not implementation-level.
# Core Instructions
- Keep the solution simple, actionable, and well-structured.
Reasoning behind change:Rewrote all instruction statements for brevity and actionable clarity to reduce potential ambiguity and cognitive overload—key for high-performing multi-step GPT-5 tasks.
- Cover all major SDLC stages with defined sub-agent roles, ensuring modularity across the process.
- Ensure every component is based on free, up-to-date tools or frameworks.
- Structure should support easy replacement and upgrading of tools/modules based on ongoing feedback.
# Steps
Reasoning behind change:Split the process into clear, actionable, step-by-step instructions to improve the assistant's response structure and reliability.
1. Review the requirements; request clarification on any unclear points before proceeding.
Reasoning behind change:Added a direct instruction to ask clarifying questions before proceeding if requirements are unclear. This leverages GPT-5's clarification abilities and avoids rework.
2. Deliver a concise, high-level plan in Markdown, structured with clear headings and lists.
3. The plan will support generating actionable task lists for each sub-agent and guide further detail work.
# Plan Structure
Reasoning behind change:Clarified and ordered all output plan sections (overview, stages, sub-agent roles, tools/components, workflow, error handling) to ensure the assistant provides output in a logical, usable sequence.
Follow this schema for the Markdown output:
---
Reasoning behind change:Expanded the Markdown schema and sample output format with clear delimiters and explicit sections for the plan, aligning output tightly to user needs.
# Vibe-Coding Pattern: High-Level Plan
## Overview
- Briefly summarize the intent behind vibe-coding and its modular approach.
## Development Lifecycle Stages
- List and briefly explain each stage (e.g., Requirements, Design, TDD, Implementation, DevOps, etc.).
## Sub-Agent Roles
- For each lifecycle stage:
Reasoning behind change:Specified exactly which details to include about each sub-agent, such as role name, responsibilities, free tool options, and sample tasks. This concreteness prevents the assistant from omitting critical role-specific context and supports modularity.
- **Role Name**: (e.g., Test Agent, DevOps Agent)
- **Responsibilities**: 1-2 sentence summary
- **Suggested Free Tools/Frameworks**: Bullet list (include options where swaps are likely)
- **Sample Tasks**: Bullet list
## Tools & Modular Components
Reasoning behind change:Introduced a structured table for listing modular components and their alternatives, facilitating explicit documentation of available free tools and easy swapping.
- Provide a table:
| Component | Free Tools/Frameworks | Alternatives |
|------------------|------------------------|------------------------|
| IDE | VSCode | Eclipse, Atom |
| CI/CD | GitHub Actions | GitLab CI, Jenkins |
| ... | ... | ... |
## Workflow Sequence
- Numbered or bulleted list outlining stage order, showing points where component swaps or decisions might occur.
## Error Handling & Divergent Choices
Reasoning behind change:Added a brief, explicitly-required section for error handling and divergent choices, to address tool swaps and issues in a modular tooling approach.
- Concisely describe how tool swaps and error handling are managed.
---
# Output Format
Reasoning behind change:Added a formal Markdown-based output format example with clear required headings and structure to resolve ambiguity from the original prompt. This ensures the response is easy to read, consistent, and can be reused or referenced later.
- Output the high-level plan in Markdown only, following the schema above.
# Verbosity
Reasoning behind change:Added a 'Verbosity' section and explicit 'Completion Criteria' to define level of detail and task boundaries, helping GPT-5 avoid over-generation and keep outputs concise and focused.
- Aim for concise, clear lists and statements.
# Completion Criteria
- Do not proceed beyond delivering the initial high-level plan.
- Ask for clarifications first if requirements are unclear.
# Agentic Criteria
Reasoning behind change:Added 'Agentic Criteria' to provide GPT-5 explicit autonomy boundaries, so the model knows when to proceed or pause for clarification, reducing unproductive back-and-forth.
Attempt a first pass autonomously unless missing critical info; stop and request clarification if requirements are ambiguous or if key success criteria are unmet.