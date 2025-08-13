Collaboration Protocol for BotArmy
Purpose:
Define how the Product Owner Agent, Requirements Specification Agent, Design & Architecture Agent, Frontend Developer Agent, Backend Developer Agent, Testing & QA Agent, and Deployment Agent collaborate, exchange data, and resolve conflicts.

1. Agent Roles & Responsibilities
Agent	Primary Responsibilities	Receives Input From	Provides Output To
Product Owner Agent	Interpret human vision, define product scope, resolve unresolved conflicts.	Human Product Owner, any agent with unresolved issues.	Requirements Specification Agent
Requirements Specification Agent	Transform scope into detailed functional & non-functional specs. Clarify requirements.	Product Owner Agent	Design & Architecture Agent
Design & Architecture Agent	Create technical architecture, database design, UI/UX wireframes. Validate feasibility.	Requirements Specification Agent	Frontend & Backend Developer Agents
Frontend Developer Agent	Build responsive, accessible UI and integrate frontend logic.	Design & Architecture Agent	Testing & QA Agent
Backend Developer Agent	Build APIs, databases, server logic, integrations.	Design & Architecture Agent	Testing & QA Agent
Testing & QA Agent	Validate product meets requirements, find/report defects.	Frontend & Backend Developer Agents	Deployment Agent
Deployment Agent	Configure hosting, deploy, and verify live accessibility.	Testing & QA Agent	Product Owner Agent (final delivery)

2. Collaboration Flow
Step-by-step workflow:

Vision & Scope

Human Product Owner → Product Owner Agent

Defines high-level vision, target users, primary features, and success metrics.

Detailed Requirements

Product Owner Agent → Requirements Specification Agent

Expands into functional & non-functional specs, constraints, and acceptance criteria.

Conflict rule: If requirement ambiguity remains after two clarification loops, escalate to Human Product Owner.

Design Phase

Requirements Specification Agent → Design & Architecture Agent

Produces:

Technical architecture

UI wireframes

Database schema

Checks with Dev agents for feasibility before finalizing.

Development Phase

Design & Architecture Agent → Frontend & Backend Developer Agents (parallel)

Frontend Developer Agent: Builds UI, routing, state management, API calls.

Backend Developer Agent: Builds API endpoints, data persistence, authentication.

Integration Loop: Dev agents sync on API contracts; if mismatched, try 2 iterations to resolve before escalation.

Testing Phase

Frontend + Backend output → Testing & QA Agent

Runs unit, integration, UI, performance, and security tests.

Defect loop: QA → Dev agents for fixes → back to QA for re-test. Limit: 3 loops before escalation.

Deployment Phase

Testing & QA Agent → Deployment Agent

Deployment Agent sets up hosting, config, CI/CD, monitors performance.

Post-deployment smoke tests by QA Agent before handover.

Final Delivery

Deployment Agent → Product Owner Agent → Human Product Owner.

Human reviews live product and final documentation.

3. Communication Protocol
All inter-agent communication follows structured JSON handoffs:

{
  "from_agent": "RequirementsSpecificationAgent",
  "to_agent": "DesignArchitectureAgent",
  "handoff_type": "requirements_package",
  "version": "1.2",
  "content": {
    "functional_requirements": ["User login with email/password", "Responsive dashboard"],
    "non_functional_requirements": ["Page load under 2s", "99.9% uptime"],
    "constraints": ["Must use React + Node.js", "Deploy to AWS"],
    "open_questions": ["Confirm color palette for branding?"]
  },
  "status": "awaiting_acknowledgement",
  "timestamp": "2025-08-10T14:35:00Z"
}

4. Conflict Resolution Rules
First attempt: Agents negotiate directly (max 3 message exchanges).

Second attempt: If no agreement, both agents propose compromise options in structured format.

Final escalation: Send issue to Product Owner Agent with a side-by-side pros/cons list.

Human override: If Product Owner Agent cannot resolve in 2 attempts, escalate to Human Product Owner.

5. Logging & Transparency
All agent interactions are logged in chronological JSONL format for auditability.

Logs contain:

Agent names

Actions taken

Decision points

Escalation events

Human Product Owner dashboard can filter logs by phase, agent, or issue type.

6. Handoff Contracts
Each handoff must include:

Version number (so changes can be tracked)

Status (draft, ready_for_review, approved, rejected_with_comments)

Dependencies (which other outputs must exist before proceeding)

Checklist of acceptance criteria

7. Example Interaction Loop
Scenario: API endpoint name mismatch

Backend Developer → Frontend Developer: “API returns /user_data but you’re calling /users.”

Frontend Developer: Adjusts call or requests backend rename.

Backend Developer: Updates and confirms fix.

QA validates before proceeding.

If still failing → escalate to Product Owner Agent.