# Phase 1: Core Foundation Implementation Plan (Week 1)

This plan outlines the tasks to implement the core foundation of the Vibe-Coding Framework, focusing on simplicity, free tools, and a shared Markdown file for communication. It aligns with the Architect Role's responsibilities for system design, tool selection, and technical specifications, tailored for a solo developer or small team.

## 🎯 Objectives
- **Smart CLI Setup Tool**: Create a one-command project initialization script.
- **Mode Selection**: Enable configuration for solo or small team modes.
- **Basic Dependency Resolver**: Implement simple dependency tracking to prevent circular dependencies.
- **Simple Error Handling**: Add basic retry and fallback mechanisms.
- **Constraints**: Use free tools (e.g., Node.js, GitHub, VS Code) and a shared Markdown file for agent communication instead of a message bus.

## 📋 Task List

### 1. Smart CLI Setup Tool
- **Task**: Create a Node.js-based CLI script for project initialization.
  - **Description**: Develop a script using `commander.js` (free, open-source) to prompt for project type, team size, and stack, then generate a project structure.
  - **Tools**: Node.js (v20, free), `commander.js` (via npm), VS Code (free).
  - **Output**: A `create-vibe-project` script that sets up a project folder with a `package.json`, basic config files, and a shared Markdown file (`project-state.md`).
  - **Architect Role**: Define CLI input options (e.g., project type: web-app/api, team size: solo/small) and output structure (e.g., folders for src, tests).
  - **Steps**:
    1. Install Node.js and `commander.js` locally.
    2. Write a script to prompt for inputs and create a project folder with:
       - `package.json` for Node.js projects.
       - `project-state.md` for task tracking and communication.
       - Basic `.gitignore` for Git.
    3. Test CLI with a sample project (e.g., `npx create-vibe-project my-app`).
  - **Estimated Time**: 8 hours.
  - **Deliverable**: A working CLI script in a GitHub repository.

### 2. Mode Selection
- **Task**: Implement a configuration file for solo and small team modes.
  - **Description**: Create a `vibe-config.yaml` file with predefined agent roles based on team size, as outlined in the framework's Mode 1 (Solo) and Mode 2 (Small Team).
  - **Tools**: YAML (parsed with `js-yaml`, free), GitHub for config storage.
  - **Output**: A `vibe-config.yaml` file with agent roles (e.g., solo: all-in-one agent, small team: product_owner, developer_lead).
  - **Architect Role**: Define YAML structure for modes, ensuring compatibility with solo (minimal complexity) and small team (split roles).
  - **Steps**:
    1. Design YAML schema for modes (e.g., `agents: { solo: { roles: [analyst, architect, developer] } }`).
    2. Write a script to validate and load the config using `js-yaml`.
    3. Store the config in the project’s GitHub repository.
    4. Test config loading for solo and small team setups.
  - **Estimated Time**: 6 hours.
  - **Deliverable**: A validated `vibe-config.yaml` file in the project repository.

### 3. Basic Dependency Resolver
- **Task**: Implement a simple dependency tracker using a shared Markdown file.
  - **Description**: Create a `DependencyResolver` class to track tasks and dependencies in `project-state.md`, detecting circular dependencies manually.
  - **Tools**: Node.js, `markdown-it` (free, for parsing Markdown), GitHub for shared file storage.
  - **Output**: A `DependencyResolver` class that reads/writes task statuses and dependencies in `project-state.md`.
  - **Architect Role**: Define the dependency graph structure (e.g., task, dependencies, status) and specify Markdown table format for task tracking.
  - **Steps**:
    1. Design a Markdown table format for tasks (e.g., | Task | Dependencies | Status |).
    2. Write a `DependencyResolver` class to:
       - Parse `project-state.md` for tasks and dependencies.
       - Detect circular dependencies (e.g., Task A depends on B, B on A).
       - Update task statuses (pending, ready, complete).
    3. Test with sample tasks (e.g., "design API" depends on "write requirements").
    4. Store `project-state.md` in the GitHub repository for team access.
  - **Estimated Time**: 10 hours.
  - **Deliverable**: A `DependencyResolver` class and sample `project-state.md` in the repository.

### 4. Simple Error Handling
- **Task**: Add basic retry and fallback mechanisms to the CLI and resolver.
  - **Description**: Implement a retry mechanism for CLI commands and a fallback task assignment in `DependencyResolver` when tasks are blocked.
  - **Tools**: Node.js, `async-retry` (free, for retries), GitHub for shared state.
  - **Output**: Retry logic in the CLI (e.g., retry file creation 3 times) and fallback task logic in `DependencyResolver` (e.g., assign alternative tasks if blocked).
  - **Architect Role**: Define error handling requirements (e.g., retry 3 times with 1-second delay, fallback to documentation tasks if blocked).
  - **Steps**:
    1. Add `async-retry` to the CLI for file operations (e.g., retry `mkdir` if it fails).
    2. Extend `DependencyResolver` to mark tasks as "blocked" in `project-state.md` and suggest alternative tasks (e.g., "write docs" if "code API" is blocked).
    3. Test retry (e.g., simulate file access failure) and fallback (e.g., simulate blocked task).
    4. Document error handling in `project-state.md`.
  - **Estimated Time**: 8 hours.
  - **Deliverable**: Updated CLI and `DependencyResolver` with error handling, reflected in `project-state.md`.

## 🛠 System Design
- **Architecture**: A Node.js-based CLI tool that generates a project structure and manages tasks via a shared `project-state.md` file stored in a GitHub repository.
- **Components**:
  - **CLI Tool**: `create-vibe-project` script for setup.
  - **Config**: `vibe-config.yaml` for mode selection.
  - **Dependency Resolver**: Node.js class for task tracking.
  - **Shared State**: `project-state.md` for task and error communication.
- **Tools**:
  - **Node.js**: Runtime for CLI and resolver.
  - **commander.js**: CLI input handling.
  - **js-yaml**: Parse mode config.
  - **markdown-it**: Parse shared Markdown file.
  - **GitHub**: Free repository for project files and collaboration.
  - **VS Code**: Free IDE for development.
- **Data Flow**:
  - CLI generates project files and `project-state.md`.
  - `DependencyResolver` reads/writes tasks to `project-state.md`.
  - Agents (solo or small team) update `project-state.md` via GitHub.
- **Scalability**: Minimal setup for solo/small teams, using GitHub for shared access.
- **Diagram**:
  ```plaintext
  [CLI Tool] --> [vibe-config.yaml] --> [DependencyResolver]
     |               |                      |
     v               v                      v
  [Project Files] [project-state.md] <--> [GitHub Repo]
  ```

## 📅 Timeline
- **Day 1**: Set up Node.js, install dependencies, and design CLI structure.
- **Day 2**: Implement and test CLI setup tool.
- **Day 3**: Create and test `vibe-config.yaml` for mode selection.
- **Day 4**: Develop and test `DependencyResolver` with Markdown parsing.
- **Day 5**: Add and test retry/fallback error handling, finalize documentation.

## ✅ Success Metrics
- **Setup Time**: CLI creates a project in <10 minutes.
- **Dependency Resolution**: 100% detection of circular dependencies in tests.
- **Error Handling**: Retry succeeds in 90% of simulated failures; fallback assigns alternative tasks correctly.
- **Simplicity**: Solo developer can configure and run the setup in <1 hour.

## 📝 Notes
- **Shared Markdown File**: `project-state.md` replaces the message bus for simplicity, storing tasks, dependencies, and statuses in a GitHub-hosted Markdown table.
- **Free Tools**: All tools (Node.js, GitHub, VS Code, npm packages) are free, ensuring accessibility.
- **Architect Role Alignment**: Tasks focus on system design, tool selection, and technical specs, avoiding coding or testing per the Architect Role definition.
- **Next Steps**: Discuss task prioritization, test scenarios, and potential GitHub repository setup for collaboration.