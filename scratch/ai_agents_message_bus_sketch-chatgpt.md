# AI Agent Message Bus Options & Architecture Sketch

## Comparison (Aug 2025)

| Option | Description | Key Features | Open-Source | Maturity (Aug 2025) | Backers/Community | Suitability for Agent Communication & Task Hand-Off | Pros | Cons |
|---|---|---|---|---|---|---|---|---|
| **A2A Protocol (Agent-to-Agent)** | An open protocol for inter-agent interoperability and delegation. | Defines agent identity, hand-offs/delegation, signatures; community GitHub; early implementations. | Yes (spec + refs). | **Early/experimental** | Google/DeepMind blog announcement, community contributors | Great *future* fit for standardized A2A hand-offs across stacks; today, best paired with a concrete bus/runtime. | Open, vendor-neutral; purpose-built for agent hand-offs | Young ecosystem; fewer production examples/tools right now |
| **OpenAI Agents SDK** | Lightweight multi-agent framework (Python & JS/TS). | Built-in **handoffs**, guardrails, sessions, tracing; integrates MCP; supports non-OpenAI models via LiteLLM/adapters. | Yes (MIT). | **Growing/active** | OpenAI + broad dev community | Strong for agent routing/handoffs & dev ergonomics; can sit atop any bus. | Batteries-included handoff + tracing; MCP support; works with other providers (LiteLLM) | Some features optimized for OpenAI; non-OpenAI parity can lag |
| **LangGraph (LangChain)** | Stateful agent orchestration (Python/JS). | Supervisor patterns, conditional routing, **HITL interrupts**, streaming; OTel/LangSmith/Langfuse tracing. | Yes (MIT). | **Mature/popular** | LangChain Inc. + big OSS community | Excellent for multi-agent routing, HITL, retries (via state/checkpoints). | First-class **HITL** via `interrupt`; easy tracing; Python & JS | You still need a transport/persistence layer for cross-process agents |
| **Microsoft AutoGen** | Multi-agent conversation & tool-use framework. | Coordinators, group chats, function tools; integrates with various LLMs. | Yes | **Mature OSS** | Microsoft + OSS community | Solid for intra-process agent teams; add a bus for distributed. | Simple mental model; many samples | Less focus on tracing/HITL out-of-the-box than LangGraph; add your own bus/observability |
| **Model Context Protocol (MCP)** | Open standard to expose tools/data to agents (not a bus). | Standardized tool servers/clients; broad ecosystem; supported in OpenAI Agents. | Yes | **Rapidly growing** | Anthropic + multi-vendor/community adoption | Great complement for agent interop and controlled tool access; use *with* an orchestration layer/bus. | Vendor-neutral; huge server ecosystem; security improving with OAuth flows | Not a message bus; you still need routing/queueing for agents |
| **NATS (JetStream)** | High-performance message bus (Req/Rep, Pub/Sub, Streams). | In-memory + **JetStream** persistence, **replay**, **streaming**, simple ops, request-reply; works great at small scale. | Yes | **Very mature** | Synadia + strong OSS users | Excellent backbone for A2A messaging, fan-out, retries. | Single binary; easy to self-host; **streaming** + replay; low-latency | No built-in human approval UI; implement HITL at app layer |
| **RabbitMQ (incl. Streams)** | Proven broker (AMQP) with queues + **Stream Queues**. | Routing with exchanges, DLX retries, **Streams** (replay, high-throughput), consumer groups. | Yes | **Very mature** | Broad OSS/CloudAMQP community | Great when you need routing patterns & persistent streams. | Rich routing, DLX retries, **replay** with Streams | Heavier to run than NATS; Streams adds ops complexity |
| **Redis Streams** | Lightweight streaming queue. | Consumer groups, persistence, at-least-once; doubles as cache/db. | Yes | **Mature** | Redis community | Good for small agent teams on a single box; easy to host. | Simple setup; consumer recovery semantics; real-time | Multi-group/partitioning can get tricky; cross-region exactly-once is hard |
| **Temporal** | Durable workflow engine (stateful orchestration). | **Durable execution**, retries/timeouts, visibility, human tasks. | Yes (server OSS) | **Mature** | Temporal Inc. + large community | Great for durability and complex retries/human tasks; overkill for 6 agents unless strict SLAs. | Exactly-once workflow semantics | Heavier ops; steeper learning curve |

---

## Recommended Stack

**Final pick: “LangGraph + NATS JetStream + MCP”, with A2A later**

- **LangGraph** for orchestration, routing, tracing, and HITL.
- **NATS JetStream** for transport, persistence, streaming, and retries.
- **MCP** for standardised tool access across agents, avoiding vendor lock-in.
- **A2A** to be adopted when the spec and tooling mature.

---

## Reference Architecture Sketch

```
/ai-agents-system
├── agents/
│   ├── agent_a/          # Python FastAPI service
│   ├── agent_b/
│   └── ...
├── orchestrator/
│   ├── langgraph_app.py  # LangGraph supervisor
│   ├── workflows/        # Graph definitions
│   └── hitl_ui/          # HITL dashboard (React)
├── mcp/
│   ├── servers/          # Tool/data servers
│   └── clients/          # MCP client configs
├── infra/
│   ├── nats/
│   │   └── nats.conf
│   ├── docker-compose.yml
│   └── telemetry/
│       └── otel_collector_config.yaml
└── README.md
```

**Flow:**  
1. **Agents** connect to **NATS** for messaging.  
2. **LangGraph supervisor** orchestrates multi-agent flows using NATS subjects for routing.  
3. **MCP servers/clients** expose tools securely.  
4. **HITL React UI** allows pausing/resuming workflows via LangGraph’s `interrupt()`.  
5. **Telemetry** flows to OpenTelemetry collector for distributed tracing.

---

## Why This Works for Your Constraints

- **Open-source**: All core components are MIT/BSD/Apache licensed.  
- **Cloud-hostable**: Fits free-tier VPS or micro container hosting.  
- **Python & React**: Orchestrator and agents in Python; UI in React.  
- **Scalable enough**: Easily handles your 6-agent scope, expandable later.  
- **No vendor lock-in**: Protocols and OSS tools keep you free to swap LLM providers.
