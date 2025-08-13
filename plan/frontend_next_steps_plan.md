# BotArmy Frontend Implementation - Next Steps

## Phase 1: Project Setup (Days 1-2)

### 1.1 Create Frontend Directory Structure
```bash
mkdir -p frontend/{src,public}
cd frontend
npm create vite@latest . -- --template react-ts
```

### 1.2 Install Dependencies
```bash
npm install zustand axios @tanstack/react-query @tanstack/react-virtual
npm install -D tailwindcss postcss autoprefixer
npm install -D @testing-library/react @testing-library/jest-dom
npm install -D vitest jsdom msw
npx tailwindcss init -p
```

### 1.3 Configure Core Files
- `vite.config.ts` - Proxy setup for backend API
- `tailwind.config.js` - Design system colors and animations
- `tsconfig.json` - Path aliases and strict TypeScript

## Phase 2: Core Infrastructure (Days 3-4)

### 2.1 Type Definitions (`src/types/`)
```typescript
// src/types/agent.ts
export type AgentType = 'analyst' | 'architect' | 'developer' | 'tester';
export type AgentStatus = 'idle' | 'thinking' | 'waiting' | 'error';

// src/types/websocket.ts  
export interface WebSocketMessage {
  type: 'agent_message' | 'status_update' | 'action_required';
  data: MessageData;
}
```

### 2.2 State Management (`src/stores/`)
```typescript
// src/stores/agentStore.ts - Zustand store for agent state
// src/stores/conversationStore.ts - Message history management
// src/stores/actionQueueStore.ts - Human actions queue
```

### 2.3 WebSocket Integration (`src/hooks/`)
```typescript
// src/hooks/useWebSocket.ts - Real-time communication
// src/hooks/useConversations.ts - Message loading/caching
// src/hooks/useOptimisticUpdates.ts - UI responsiveness
```

## Phase 3: Core Components (Days 5-8)

### 3.1 Dashboard Layout (`src/components/Layout/`)
- **Dashboard.tsx** - Main container with tabbed interface
- **Header.tsx** - Connection status, spec viewer toggle
- **TabNavigation.tsx** - Agent console switcher

### 3.2 Agent Consoles (`src/components/AgentConsole/`)
- **BaseAgentConsole.tsx** - Reusable console template
- **ConversationView.tsx** - Message display with virtualization
- **MessageItem.tsx** - Individual message component
- **AgentStatusIndicator.tsx** - Real-time status display

### 3.3 Action Queue (`src/components/ActionQueue/`)
- **ActionQueue.tsx** - Sidebar with priority-based notifications
- **ActionItem.tsx** - Individual action cards
- **ActionModal.tsx** - Decision interface forms

### 3.4 Spec Viewer (`src/components/SpecViewer/`)
- **SpecViewer.tsx** - Project specification display
- **SpecHistory.tsx** - Version history with diffs
- **SpecDiff.tsx** - JSON Patch visualization

## Phase 4: Advanced Features (Days 9-12)

### 4.1 Performance Optimizations
- Message virtualization for large conversation histories
- IndexedDB caching for offline capability
- Optimistic UI updates with rollback
- Debounced real-time updates

### 4.2 Testing Infrastructure
- Unit tests for hooks and stores (75% coverage)
- Component tests with React Testing Library
- WebSocket integration tests with MSW
- E2E tests with Playwright

### 4.3 Error Handling & UX Polish
- Error boundaries for component isolation
- Loading states and skeleton screens
- Toast notifications for system events
- Responsive design with Tailwind CSS

## Required Backend Integration Points

### API Endpoints Needed:
- `GET /api/conversations/{agentId}` - Message history
- `PATCH /api/projects/{projectId}/spec` - Spec updates
- `POST /api/projects/{projectId}/actions` - Human decisions
- `WebSocket /ws/projects/{projectId}` - Real-time communication

### Mock Data for Development:
```typescript
// src/services/api.ts
const isDevelopment = process.env.NODE_ENV === 'development';

export const apiService = {
  async getConversations(agentId: string) {
    if (isDevelopment) {
      return mockConversationData[agentId] || [];
    }
    // Real API call
  }
};
```

## Success Criteria

### Technical Metrics:
- ✅ Initial page load < 3 seconds
- ✅ Message delivery < 1 second end-to-end  
- ✅ UI responsiveness < 100ms for interactions
- ✅ 75% test coverage for core components
- ✅ WebSocket connection uptime > 99%

### User Experience:
- ✅ Intuitive tabbed agent console interface
- ✅ Real-time status indicators with confidence scores
- ✅ Priority-based human action notifications
- ✅ Searchable conversation history
- ✅ Zero-configuration setup in development

## File Structure to Create:
```
frontend/
├── src/
│   ├── components/
│   │   ├── AgentConsole/
│   │   ├── ActionQueue/
│   │   ├── SpecViewer/
│   │   ├── Layout/
│   │   └── UI/
│   ├── hooks/
│   ├── stores/
│   ├── types/
│   ├── services/
│   ├── utils/
│   └── App.tsx
├── public/
├── package.json
├── vite.config.ts
├── tailwind.config.js
└── tsconfig.json
```

## Immediate Action Items:

1. **Create `frontend/` directory** alongside existing `src/` (backend)
2. **Set up React + Vite + Tailwind CSS** development environment
3. **Implement WebSocket hook** for real-time communication testing
4. **Build basic dashboard layout** with tabbed agent consoles
5. **Add mock data service** for development without backend dependency

This frontend implementation will provide the human interface layer for the BotArmy system, connecting to the existing agent infrastructure via WebSocket and REST APIs.