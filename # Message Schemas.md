# Message Schemas — Vibe-Coding Orchestrator

## Core Message Format (JSON)

```json
{
  "id": "uuid-v4",
  "actor": "Analyst|Architect|Developer|Tester|ProductOwner",
  "task_type": "feature|bug|question|test",
  "summary": "Brief description",
  "details": "Markdown-formatted detailed description",
  "status": "todo|in_progress|blocked|done|awaiting_PO",
  "attachments": ["url-to-diff", "url-to-test-report"],
  "escalation_required": true,
  "priority": "low|medium|high",
  "timestamp": "ISO8601 datetime"
}
