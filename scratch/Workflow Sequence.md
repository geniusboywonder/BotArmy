Workflow Sequence
Human Orchestrator defines the initial project goals and requirements.

Requirements Agent generates user stories and acceptance criteria, sending them to the orchestrator for adjudication.

Upon approval, the Design Agent creates a technical design and architecture, which is again sent to the orchestrator for adjudication.

The TDD Agent writes a test suite based on the approved design, which is then passed to the Coding Agent.

The Coding Agent writes code to pass the tests. This process is iterative, with the Coding and TDD agents working together until all tests pass.

The DevOps Agent picks up the approved code and tests, running them through the CI/CD pipeline for building and deployment.

The orchestrator monitors the entire process, stepping in to make decisions or clarify requirements at any point where the agents are blocked or present multiple options.