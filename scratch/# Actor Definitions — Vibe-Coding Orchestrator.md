# Actor Definitions — Vibe-Coding Orchestrator

## 1. Product Owner (You)
- Final approver of all decisions and changes
- Reviews agent communications and clarifications via UI
- Answers questions surfaced by agents
- Confirms merges and deployments

## 2. Analyst
- Gathers and clarifies requirements from Product Owner
- Synthesizes inputs into structured format (Requirements.md)
- Generates questions and escalations to Product Owner
- Communicates requirements to Architect

## 3. Architect
- Designs system components and workflows based on Analyst input
- Defines message contracts and task breakdowns
- Assigns tasks to Developer agents
- Handles architectural clarifications and escalations

## 4. Developer
- Implements assigned features in isolated branches or containers
- Writes and runs unit tests
- Communicates progress and blockers to Tester and Architect

## 5. Tester
- Develops and executes automated test suites
- Reports test results and failures to Developer and Analyst
- Validates agent communication contract adherence

## 6. (Future) Code Reviewer
- Reviews pull requests for code quality and standards
- Approves or requests changes prior to merge

## 7. (Future) DevOps / Deployment
- Maintains CI/CD pipelines
- Manages infrastructure and deployment environments
