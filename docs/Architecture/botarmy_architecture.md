# BotArmy Technical Architecture Document

## 1. Architecture Overview

BotArmy is designed as a **Sequential Agent Orchestration System** with real-time human oversight, built for rapid POC deployment on free cloud platforms.

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    BotArmy System                           │
├─────────────────────────────────────────────────────────────┤
│  Human Interface Layer                                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │ Agent Consoles  │  │ Action Queue    │  │ Spec Viewer │ │
│  │ (Real-time)     │  │ (Human Tasks)   │  │ (Live Doc)  │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  Orchestration Layer                                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │ Agent Manager   │  │ Message Bus     │  │ Conflict    │ │
│  │ (Sequential)    │  │ (JSONL + WS)    │  │ Resolver    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  Agent Layer                                                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │ Analyst  │ │Architect │ │Developer │ │ Tester   │ ...  │
│  │ (Claude) │ │(Claude)  │ │(Claude)  │ │(OpenAI)  │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
├─────────────────────────────────────────────────────────────┤
│  Persistence Layer                                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │ Conversation    │  │ Project Spec    │  │ Generated   │ │
│  │ Logs (JSONL)    │  │ (JSON+History)  │  │ Artifacts   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 2. Technology Stack

### 2.1 Primary Platform: **GitHub Codespaces** (Recommended)

- **Rationale**: Free tier available, persistent storage, web-based, supports full-stack development
- **Alternative**: Replit (if GitHub Codespaces unavailable)
- **Fallback**: Google Colab (limited web capabilities)

### 2.2 Core Technologies

| Component | Technology | Justification |
|-----------|------------|---------------|
| **Frontend** | React + Vite | Fast development, component-based UI for agent consoles |
| **Backend** | FastAPI (Python) | Async support, auto-documentation, WebSocket support |
| **Real-time Communication** | WebSockets | Live agent conversation streaming |
| **Message Bus** | In-memory Queue + JSONL | Simple, observable, persistent logging |
| **LLM Integration** | LangChain + OpenAI/Anthropic | Unified interface, easy model swapping |
| **State Management** | Pydantic Models + JSON Files | Type safety, easy serialization |
| **Testing** | Pytest + React Testing Library | Basic coverage for POC |

### 2.3 File Structure

```
botarmy/
├── frontend/                   # React UI
│   ├── src/
│   │   ├── components/
│   │   │   ├── AgentConsole.jsx
│   │   │   ├── ActionQueue.jsx
│   │   │   └── SpecViewer.jsx
│   │   ├── hooks/
│   │   │   └── useWebSocket.js
│   │   └── App.jsx
├── backend/                    # FastAPI Server
│   ├── agents/
│   │   ├── base_agent.py
│   │   ├── analyst.py
│   │   ├── architect.py
│   │   └── developer.py
│   ├── orchestration/
│   │   ├── message_bus.py
│   │   ├── conflict_resolver.py
│   │   └── agent_manager.py
│   ├── models/
│   │   ├── messages.py
│   │   └── project_spec.py
│   └── main.py
├── data/                       # Persistent Storage
│   ├── conversations/
│   ├── specs/
│   └── artifacts/
└── tests/
```

## 3. Core Components Design

### 3.1 Message Bus Architecture

```python
# Message Schema
{
    "id": "msg_001",
    "timestamp": "2024-01-01T10:00:00Z",
    "from_agent": "analyst",
    "to_agent": "architect",
    "message_type": "handoff|conflict|agreement|escalation",
    "content": {
        "requirements": {...},
        "status": "complete|pending|conflict",
        "confidence": 0.8
    },
    "attempt_number": 1,
    "thread_id": "thread_001"
}
```

### 3.2 Conflict Resolution System

```python
class ConflictResolver:
    def __init__(self):
        self.max_attempts = 3
        self.timeout_seconds = 300
        
    def detect_conflict(self, conversation_thread):
        # Check for disagreement patterns
        # Detect loops in conversation
        # Monitor timeout conditions
        
    def escalate_to_human(self, conflict_context):
        # Pause dependent agents
        # Generate human-readable summary
        # Queue for human intervention
```

### 3.3 Agent Communication Protocol

**Sequential Workflow:**

1. **Analyst** → Requirements Document → **Architect**
2. **Architect** → Technical Specs → **Developer**  
3. **Developer** → Code Artifacts → **Tester**
4. **Tester** → Test Results → **Deployer**

**Conflict Resolution Protocol:**

1. Agent A sends message to Agent B
2. Agent B responds with agreement/disagreement
3. If disagreement, negotiate for up to 3 attempts
4. If unresolved, escalate to human with context
5. Human decision updates project spec and resumes workflow

## 4. Data Persistence Strategy

### 4.1 Storage Components

| Data Type | Format | Location | Update Pattern |
|-----------|--------|----------|----------------|
| **Conversations** | JSONL | `/data/conversations/{project_id}.jsonl` | Append-only |
| **Project Spec** | JSON | `/data/specs/{project_id}.json` | Versioned updates |
| **Agent State** | JSON | In-memory + periodic snapshots | Real-time |
| **Generated Code** | Files | `/data/artifacts/{project_id}/` | Version controlled |

### 4.2 Spec Versioning

```python
{
    "project_id": "proj_001",
    "version": 3,
    "updated_by": "architect",
    "updated_at": "2024-01-01T10:30:00Z",
    "changes": ["Added API endpoints", "Updated data schema"],
    "spec": {
        "requirements": {...},
        "architecture": {...},
        "implementation": {...}
    },
    "history": [
        {"version": 1, "updated_by": "analyst", "timestamp": "..."},
        {"version": 2, "updated_by": "architect", "timestamp": "..."}
    ]
}
```

## 5. User Interface Design

### 5.1 Main Dashboard Layout

```
┌─────────────────────────────────────────────────────────────┐
│ BotArmy POC - Project: {project_name}               [Settings]│
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│ │ Agent Consoles  │  │ Action Required │  │ Project Spec    │ │
│ │                 │  │                 │  │                 │ │
│ │ [Analyst]  🟢   │  │ 🔴 Human Input  │  │ Version: 3      │ │
│ │ [Architect] 🟡  │  │ Needed          │  │ Updated: 10:30  │ │
│ │ [Developer] ⚪  │  │                 │  │ By: architect   │ │
│ │ [Tester]   ⚪   │  │ Choose API      │  │                 │ │
│ │                 │  │ Framework:      │  │ [View Full Spec]│ │
│ │ [Live Logs]     │  │ • REST          │  │ [Download]      │ │
│ │                 │  │ • GraphQL       │  │                 │ │
│ │ ...agent msgs   │  │                 │  │ Status:         │ │
│ │                 │  │ [Decide]        │  │ Architecture    │ │
│ └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Real-time Features

- **WebSocket connections** for live agent conversation streaming
- **Auto-scroll** in conversation logs
- **Toast notifications** for human action requirements
- **Progress indicators** showing workflow stage

## 6. LLM Integration Strategy

### 6.1 Agent-LLM Mapping

```python
AGENT_LLM_CONFIG = {
    "analyst": {
        "provider": "anthropic",
        "model": "claude-3-sonnet",
        "temperature": 0.3,
        "max_tokens": 2000
    },
    "architect": {
        "provider": "anthropic", 
        "model": "claude-3-sonnet",
        "temperature": 0.2,
        "max_tokens": 3000
    },
    "developer": {
        "provider": "anthropic",
        "model": "claude-3-sonnet", 
        "temperature": 0.1,
        "max_tokens": 4000
    },
    "tester": {
        "provider": "openai",
        "model": "gpt-4o-mini",
        "temperature": 0.2,
        "max_tokens": 2000
    }
}
```

### 6.2 Free Tier Management

- **OpenAI**: GPT-4o-mini free tier
- **Anthropic**: Claude-3-haiku free tier (if available)
- **Fallback**: Groq Llama models for high-volume testing

## 7. Deployment Architecture

### 7.1 GitHub Codespaces Setup

```yaml
# .devcontainer/devcontainer.json
{
    "name": "BotArmy POC",
    "image": "mcr.microsoft.com/devcontainers/python:3.11",
    "features": {
        "ghcr.io/devcontainers/features/node:1": {"version": "18"}
    },
    "ports": [3000, 8000],
    "postCreateCommand": "cd backend && pip install -r requirements.txt && cd ../frontend && npm install"
}
```

### 7.2 Container Structure (Future Migration)

```dockerfile
# Dockerfile (for future use)
FROM python:3.11-slim
COPY backend/ /app/backend/
COPY frontend/dist/ /app/frontend/
WORKDIR /app
RUN pip install -r backend/requirements.txt
EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 8. Testing Strategy

### 8.1 Testing Components

| Component | Testing Approach | Tools |
|-----------|------------------|-------|
| **Agent Logic** | Unit tests for message handling | Pytest + Mock LLM responses |
| **Message Bus** | Integration tests for communication | Pytest with test agents |
| **UI Components** | Component testing | React Testing Library |
| **API Endpoints** | API testing | FastAPI TestClient |
| **E2E Workflow** | End-to-end agent handoffs | Pytest with orchestrated flow |

### 8.2 Mock LLM Testing

```python
# For testing without API costs
class MockLLMProvider:
    def __init__(self, predefined_responses):
        self.responses = predefined_responses
        
    def generate_response(self, agent_type, prompt):
        return self.responses.get(agent_type, "Mock response")
```

## 9. Technical Risks & Mitigation

### 9.1 Identified Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **LLM API Rate Limits** | High | Medium | Free tier rotation, request queuing |
| **Agent Infinite Loops** | High | Medium | Max attempt limits, timeout mechanisms |
| **Memory Usage (Large Logs)** | Medium | High | Log rotation, compression |
| **WebSocket Connection Loss** | Medium | Medium | Auto-reconnect, message persistence |
| **Platform Storage Limits** | Medium | Medium | File cleanup, external storage hooks |

### 9.2 Scalability Considerations

- **Message Volume**: JSONL files can handle ~10K messages before performance impact
- **Concurrent Projects**: Current design supports 1 project; multi-tenancy requires session isolation
- **Agent Parallelization**: Architecture ready for concurrent agent execution in future versions

## 10. Implementation Phases

### 10.1 Phase 1: Core Infrastructure (Week 1-2)

- [ ] Message bus and agent base classes
- [ ] Basic UI with agent consoles
- [ ] Single agent (Analyst) integration
- [ ] File-based persistence

### 10.2 Phase 2: Agent Orchestration (Week 3-4)

- [ ] All agent implementations
- [ ] Sequential workflow execution
- [ ] Conflict detection and escalation
- [ ] Real-time UI updates

### 10.3 Phase 3: POC Refinement (Week 5-6)

- [ ] End-to-end testing
- [ ] UI/UX improvements
- [ ] Performance optimization
- [ ] Documentation and deployment

## 11. Spec Updates Required

Based on the architecture design, the following additions to the Product Specification Document are recommended:

### 11.1 New Technical Requirements

```markdown
3.12 Conflict Resolution
- Maximum 3 negotiation attempts between agents before human escalation
- 5-minute timeout for agent responses with automatic escalation
- Loop detection in agent conversations with intervention

3.13 Real-time Communication
- WebSocket-based live agent conversation streaming
- Human action queue with priority-based notifications
- Auto-reconnection for connection failures

3.14 LLM Provider Management
- Support for multiple LLM providers (OpenAI, Anthropic)
- Agent-specific model configuration
- Free tier management and rate limiting
```

### 11.2 Updated Success Metrics

```markdown
- Agent conflict resolution rate < 20% human escalation
- Message processing latency < 2 seconds for real-time UI
- System uptime > 95% during POC testing period
```

This architecture provides a solid foundation for the BotArmy POC while maintaining flexibility for future enhancements and migration to production environments.
