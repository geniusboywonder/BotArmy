# Sub-Agent Activation Plan: Developer and Tester Roles Post-Phase 1

This plan outlines the tasks to activate the **Developer** and **Tester** sub-agents immediately after Phase 1 (Week 1) of the Vibe-Coding Framework, enabling them to develop and test code while contributing to the Phase 1 deliverables. It uses free tools, the shared `project-state.md` file for communication, and aligns with the Architect Role’s system design for solo/small team setups.

## 🎯 Objectives
- **Developer Activation**: Enable the Developer to write and commit code for the Phase 1 CLI tool and `DependencyResolver`, using the `vibe-config.yaml` and `project-state.md`.
- **Tester Activation**: Enable the Tester to create and run tests for the CLI tool and `DependencyResolver`, ensuring functionality and reliability.
- **Speed**: Activate both roles by **Day 6-7** of Week 1, leveraging Phase 1 infrastructure.
- **Constraints**: Use free tools (e.g., Node.js, Jest, GitHub, VS Code) and `project-state.md` for task coordination.

## 📋 Task List

### 1. Developer Role Activation
- **Objective**: Enable the Developer to write and commit code for the CLI tool and `DependencyResolver`.
- **Tools**: Node.js (v20, free), VS Code (free), GitHub (free), `npm` for package management.
- **Architect Role Input**: Provide technical specs for the CLI tool (e.g., `commander.js` commands) and `DependencyResolver` (e.g., Markdown parsing logic), stored in `project-state.md`.
- **Tasks**:
  1. **Setup Development Environment** (2 hours, Day 6):
     - Clone the Phase 1 GitHub repository.
     - Install Node.js and dependencies (`commander.js`, `js-yaml`, `markdown-it`) via `npm install`.
     - Configure VS Code with ESLint (free) for code linting.
     - Update `project-state.md` with status: "Developer environment ready."
  2. **Implement CLI Enhancements** (4 hours, Day 6):
     - Add a new CLI command (e.g., `npx vibe-project add-task`) to append tasks to `project-state.md`.
     - Follow Architect’s specs in `project-state.md` (e.g., command prompts for task name, dependencies).
     - Commit changes to GitHub and update `project-state.md` with status: "CLI task command implemented."
  3. **Enhance DependencyResolver** (4 hours, Day 7):
     - Add a method to list pending tasks in `DependencyResolver` using `markdown-it`.
     - Implement basic task validation (e.g., ensure task names are unique).
     - Commit changes and update `project-state.md` with status: "DependencyResolver enhanced."
- **Interdependencies**:
  - **With Architect**: Developer relies on CLI and `DependencyResolver` specs in `project-state.md`. If specs are unclear, Developer adds a clarification request to `project-state.md` (e.g., "Need CLI command output format").
  - **Blocker Resolution**: If blocked (e.g., unclear specs), Developer updates `project-state.md` with issue details and switches to an alternative task (e.g., write documentation).
- **Deliverables**: Updated CLI script with new command, enhanced `DependencyResolver`, and `project-state.md` updates in GitHub.

### 2. Tester Role Activation
- **Objective**: Enable the Tester to write and run tests for the CLI tool and `DependencyResolver` to ensure functionality.
- **Tools**: Jest (free, via npm), Node.js, GitHub, VS Code.
- **Architect Role Input**: Provide system design details in `project-state.md` (e.g., CLI expected inputs/outputs, `DependencyResolver` task states) for test case creation.
- **Tasks**:
  1. **Setup Testing Environment** (2 hours, Day 6):
     - Clone the Phase 1 GitHub repository.
     - Install Jest via `npm install --save-dev jest`.
     - Configure Jest in `package.json` with basic test scripts (e.g., `npm test`).
     - Update `project-state.md` with status: "Tester environment ready."
  2. **Write CLI Tests** (4 hours, Day 6):
     - Create Jest test suite for CLI tool (e.g., test `create-vibe-project` creates correct folder structure).
     - Use Architect’s specs in `project-state.md` to define test cases (e.g., verify `package.json` creation).
     - Commit tests to GitHub and update `project-state.md` with status: "CLI tests written."
  3. **Write DependencyResolver Tests** (4 hours, Day 7):
     - Create Jest test suite for `DependencyResolver` (e.g., test circular dependency detection, task status updates).
     - Use Architect’s specs for expected task states (e.g., pending, complete).
     - Commit tests and update `project-state.md` with status: "DependencyResolver tests written."
- **Interdependencies**:
  - **With Architect**: Tester relies on system design in `project-state.md` for test case alignment. If design is unclear, Tester adds a clarification request to `project-state.md`.
  - **With Developer**: Tester uses Developer’s code commits to write tests. If code is incomplete, Tester updates `project-state.md` with issue details and switches to writing test plans.
- **Deliverables**: Jest test suites for CLI and `DependencyResolver`, committed to GitHub, with test results in `project-state.md`.

## 🛠 System Integration
- **Architecture Update**:
  - Developer and Tester use the Phase 1 GitHub repository and `project-state.md` for task tracking and communication.
  - CLI tool gains a new command (`add-task`) to support Developer task input.
  - `DependencyResolver` supports task listing and validation for Developer and Tester coordination.
- **Data Flow**:
  - Developer commits code to GitHub, updating `project-state.md` with task statuses.
  - Tester pulls latest code, runs tests, and updates `project-state.md` with test results.
  - Architect reviews `project-state.md` for blockers and updates specs if needed.
- **Diagram Update**:
  ```plaintext
  [CLI Tool] --> [vibe-config.yaml] --> [DependencyResolver]
     |               |                      |
     v               v                      v
  [Project Files] [project-state.md] <--> [GitHub Repo]
     ^                                    ^    ^
     |                                    |    |
  [Developer] ------------------------> [Tester]
  ```
- **Error Handling**: Reuse Phase 1 retry logic (e.g., `async-retry` for CLI) and fallback tasks (e.g., Developer writes docs if blocked, Tester writes test plans).

## 📅 Timeline
- **Day 6**:
  - Developer: Set up environment, implement CLI command.
  - Tester: Set up Jest, write CLI tests.
- **Day 7**:
  - Developer: Enhance `DependencyResolver`, commit changes.
  - Tester: Write `DependencyResolver` tests, commit results.
- **Total Time**: 2 days (Day 6-7 of Week 1).

## ✅ Success Metrics
- **Developer Activation**: Developer commits CLI command and `DependencyResolver` enhancements by Day 7, with <10 minutes setup time.
- **Tester Activation**: Tester runs Jest tests for CLI and `DependencyResolver` by Day 7, with 90% test coverage.
- **Collaboration**: Developer and Tester update `project-state.md` for all tasks, with <1 hour resolution for blockers via Architect clarification.
- **Simplicity**: Both roles onboard and contribute within 2 hours of environment setup.

## 📝 Notes
- **Shared Markdown**: `project-state.md` serves as the communication hub, with Developer and Tester updating task statuses and blockers in Markdown tables.
- **Free Tools**: Node.js, Jest, GitHub, and VS Code ensure zero-cost activation.
- **Architect Role Alignment**: Provides specs and resolves blockers via `project-state.md`, per the Architect Role definition.
- **Next Steps**: Discuss test coverage goals, Developer task prioritization, and potential expansion to other roles (e.g., Analyst) in Week 2.