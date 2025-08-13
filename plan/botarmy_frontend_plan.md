# BotArmy Frontend Implementation Plan

## 1. Executive Summary

This implementation plan details the complete frontend development for the BotArmy POC using React + Vite + Tailwind CSS + TypeScript. The frontend will provide a real-time dashboard for monitoring AI agent interactions, handling human escalations, and managing project specifications.

## 2. Technology Stack & Setup

### 2.1 Core Technologies
| Technology | Version | Purpose |
|------------|---------|---------|
| **React** | 18.x | Component-based UI framework |
| **Vite** | 4.x | Fast build tool and dev server |
| **TypeScript** | 5.x | Type safety and developer experience |
| **Tailwind CSS** | 3.x | Utility-first CSS framework |
| **Zustand** | 4.x | Global state management |
| **React Query** | 4.x | Server state and caching |
| **React Testing Library** | 13.x | Component testing |
| **MSW** | 1.x | API mocking for tests |
| **Axios** | 1.x | HTTP client |

### 2.2 Project Structure
```
frontend/
├── public/
│   ├── favicon.ico
│   └── index.html
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── AgentConsole/
│   │   │   ├── index.ts
│   │   │   ├── BaseAgentConsole.tsx
│   │   │   ├── ConversationView.tsx
│   │   │   ├── MessageItem.tsx
│   │   │   ├── AgentStatusIndicator.tsx
│   │   │   └── AgentTab.tsx
│   │   ├── ActionQueue/
│   │   │   ├── index.ts
│   │   │   ├── ActionQueue.tsx
│   │   │   ├── ActionItem.tsx
│   │   │   ├── ActionModal.tsx
│   │   │   └── PriorityBadge.tsx
│   │   ├── SpecViewer/
│   │   │   ├── index.ts
│   │   │   ├── SpecViewer.tsx
│   │   │   ├── SpecHistory.tsx
│   │   │   ├── SpecDiff.tsx
│   │   │   └── SpecExport.tsx
│   │   ├── Layout/
│   │   │   ├── index.ts
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── TabNavigation.tsx
│   │   └── UI/              # Shared UI primitives
│   │       ├── index.ts
│   │       ├── Button.tsx
│   │       ├── Modal.tsx
│   │       ├── Toast.tsx
│   │       ├── LoadingSpinner.tsx
│   │       └── ErrorBoundary.tsx
│   ├── hooks/               # Custom React hooks
│   │   ├── index.ts
│   │   ├── useWebSocket.ts
│   │   ├── useConversations.ts
│   │   ├── useProjectSpec.ts
│   │   ├── useOptimisticUpdates.ts
│   │   ├── useLocalStorage.ts
│   │   └── useNotifications.ts
│   ├── stores/              # Zustand stores
│   │   ├── index.ts
│   │   ├── agentStore.ts
│   │   ├── conversationStore.ts
│   │   ├── specStore.ts
│   │   ├── actionQueueStore.ts
│   │   └── uiStore.ts
│   ├── services/            # API and external services
│   │   ├── index.ts
│   │   ├── api.ts
│   │   ├── websocket.ts
│   │   ├── indexedDb.ts
│   │   └── storage.ts
│   ├── types/               # TypeScript type definitions
│   │   ├── index.ts
│   │   ├── agent.ts
│   │   ├── conversation.ts
│   │   ├── project.ts
│   │   ├── websocket.ts
│   │   └── api.ts
│   ├── utils/               # Utility functions
│   │   ├── index.ts
│   │   ├── formatters.ts
│   │   ├── validators.ts
│   │   ├── constants.ts
│   │   └── helpers.ts
│   ├── styles/              # Global styles and Tailwind config
│   │   ├── globals.css
│   │   └── components.css
│   ├── tests/               # Test utilities and setup
│   │   ├── __mocks__/
│   │   ├── setup.ts
│   │   ├── testUtils.tsx
│   │   └── mockData.ts
│   ├── App.tsx              # Root component
│   ├── main.tsx             # Entry point
│   └── vite-env.d.ts        # Vite type declarations
├── .env.example
├── .env.local
├── .gitignore
├── index.html
├── package.json
├── postcss.config.js
├── tailwind.config.js
├── tsconfig.json
├── tsconfig.node.json
├── vite.config.ts
└── vitest.config.ts
```

## 3. Implementation Phases

### 3.1 Phase 1: Project Setup & Core Infrastructure (Days 1-3)

#### 3.1.1 Initial Setup
```bash
# Create Vite React TypeScript project
npm create vite@latest botarmy-frontend -- --template react-ts
cd botarmy-frontend

# Install dependencies
npm install zustand axios react-query
npm install -D tailwindcss postcss autoprefixer
npm install -D @testing-library/react @testing-library/jest-dom
npm install -D vitest jsdom msw
npm install -D @types/node

# Initialize Tailwind CSS
npx tailwindcss init -p
```

#### 3.1.2 Configuration Files

**vite.config.ts**
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    host: '0.0.0.0',
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true,
      },
    },
  },
})
```

**tailwind.config.js**
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
        success: '#10b981',
        warning: '#f59e0b',
        error: '#ef4444',
      },
      animation: {
        'fade-in': 'fadeIn 0.2s ease-in-out',
        'slide-in': 'slideIn 0.3s ease-out',
        'pulse-slow': 'pulse 2s infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideIn: {
          '0%': { transform: 'translateX(100%)' },
          '100%': { transform: 'translateX(0)' },
        },
      },
    },
  },
  plugins: [],
}
```

#### 3.1.3 TypeScript Type Definitions

**src/types/agent.ts**
```typescript
export type AgentType = 'analyst' | 'architect' | 'developer' | 'tester' | 'deployer';

export type AgentStatus = 'idle' | 'thinking' | 'waiting' | 'error';

export interface Agent {
  id: string;
  type: AgentType;
  name: string;
  description: string;
  status: AgentStatus;
  currentTask?: string;
  lastActivity: string;
  confidence: number;
  isActive: boolean;
}

export interface AgentMessage {
  id: string;
  timestamp: string;
  fromAgent: string;
  toAgent: string | null;
  messageType: 'handoff' | 'conflict' | 'agreement' | 'escalation';
  content: {
    text: string;
    metadata: Record<string, any>;
    confidence?: number;
    attachments?: string[];
  };
  threadId: string;
  attemptNumber: number;
}
```

**src/types/websocket.ts**
```typescript
export interface WebSocketMessage {
  type: 'agent_message' | 'status_update' | 'action_required' | 'spec_update' | 'system_notification';
  timestamp: string;
  projectId: string;
  data: MessageData;
}

export interface MessageData {
  message?: AgentMessage;
  status?: {
    agentId: string;
    status: AgentStatus;
    currentTask?: string;
    confidence: number;
    lastActivity: string;
  };
  action?: HumanAction;
  specUpdate?: SpecUpdate;
}

export interface HumanAction {
  id: string;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  title: string;
  description: string;
  options: Array<{
    id: string;
    label: string;
    description?: string;
  }>;
  deadline?: string;
  context: Record<string, any>;
}
```

### 3.2 Phase 2: State Management & Services (Days 4-6)

#### 3.2.1 Zustand Stores

**src/stores/agentStore.ts**
```typescript
import { create } from 'zustand';
import { Agent, AgentStatus } from '@/types/agent';

interface AgentState {
  agents: Record<string, Agent>;
  activeAgent: string | null;
  
  // Actions
  updateAgentStatus: (agentId: string, status: Partial<Agent>) => void;
  setActiveAgent: (agentId: string) => void;
  initializeAgents: (agents: Agent[]) => void;
  resetAgents: () => void;
}

export const useAgentStore = create<AgentState>((set, get) => ({
  agents: {},
  activeAgent: null,

  updateAgentStatus: (agentId: string, statusUpdate: Partial<Agent>) =>
    set((state) => ({
      agents: {
        ...state.agents,
        [agentId]: {
          ...state.agents[agentId],
          ...statusUpdate,
          lastActivity: new Date().toISOString(),
        },
      },
    })),

  setActiveAgent: (agentId: string) =>
    set({ activeAgent: agentId }),

  initializeAgents: (agents: Agent[]) =>
    set({
      agents: agents.reduce((acc, agent) => ({
        ...acc,
        [agent.id]: agent,
      }), {}),
      activeAgent: agents[0]?.id || null,
    }),

  resetAgents: () =>
    set({ agents: {}, activeAgent: null }),
}));
```

**src/stores/conversationStore.ts**
```typescript
import { create } from 'zustand';
import { AgentMessage } from '@/types/agent';

interface ConversationState {
  conversations: Record<string, AgentMessage[]>;
  messageCache: Map<string, AgentMessage[]>;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  addMessage: (agentId: string, message: AgentMessage) => void;
  loadConversation: (agentId: string) => Promise<void>;
  updateMessage: (messageId: string, updates: Partial<AgentMessage>) => void;
  clearConversation: (agentId: string) => void;
  setError: (error: string | null) => void;
}

export const useConversationStore = create<ConversationState>((set, get) => ({
  conversations: {},
  messageCache: new Map(),
  isLoading: false,
  error: null,

  addMessage: (agentId: string, message: AgentMessage) =>
    set((state) => {
      const agentMessages = state.conversations[agentId] || [];
      const updatedMessages = [...agentMessages, message];
      
      // Keep only last 100 messages per agent for performance
      const trimmedMessages = updatedMessages.slice(-100);
      
      return {
        conversations: {
          ...state.conversations,
          [agentId]: trimmedMessages,
        },
      };
    }),

  loadConversation: async (agentId: string) => {
    set({ isLoading: true, error: null });
    try {
      // This will be replaced with actual API call
      const response = await fetch(`/api/conversations/${agentId}`);
      const messages = await response.json();
      
      set((state) => ({
        conversations: {
          ...state.conversations,
          [agentId]: messages,
        },
        isLoading: false,
      }));
    } catch (error) {
      set({ 
        error: error instanceof Error ? error.message : 'Failed to load conversation',
        isLoading: false,
      });
    }
  },

  updateMessage: (messageId: string, updates: Partial<AgentMessage>) =>
    set((state) => {
      const updatedConversations = { ...state.conversations };
      
      Object.keys(updatedConversations).forEach((agentId) => {
        updatedConversations[agentId] = updatedConversations[agentId].map((msg) =>
          msg.id === messageId ? { ...msg, ...updates } : msg
        );
      });
      
      return { conversations: updatedConversations };
    }),

  clearConversation: (agentId: string) =>
    set((state) => ({
      conversations: {
        ...state.conversations,
        [agentId]: [],
      },
    })),

  setError: (error: string | null) =>
    set({ error }),
}));
```

#### 3.2.2 WebSocket Service

**src/hooks/useWebSocket.ts**
```typescript
import { useEffect, useRef, useCallback } from 'react';
import { WebSocketMessage } from '@/types/websocket';
import { useAgentStore } from '@/stores/agentStore';
import { useConversationStore } from '@/stores/conversationStore';
import { useActionQueueStore } from '@/stores/actionQueueStore';

interface UseWebSocketOptions {
  projectId: string;
  onMessage?: (message: WebSocketMessage) => void;
  onError?: (error: Event) => void;
  onClose?: (event: CloseEvent) => void;
  reconnectInterval?: number;
  maxReconnectAttempts?: number;
}

export const useWebSocket = ({
  projectId,
  onMessage,
  onError,
  onClose,
  reconnectInterval = 3000,
  maxReconnectAttempts = 10,
}: UseWebSocketOptions) => {
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectAttempts = useRef(0);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout>();
  
  const updateAgentStatus = useAgentStore((state) => state.updateAgentStatus);
  const addMessage = useConversationStore((state) => state.addMessage);
  const addAction = useActionQueueStore((state) => state.addAction);

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      return;
    }

    const wsUrl = `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}/ws/projects/${projectId}`;
    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      console.log('WebSocket connected');
      reconnectAttempts.current = 0;
    };

    ws.onmessage = (event) => {
      try {
        const message: WebSocketMessage = JSON.parse(event.data);
        
        // Handle different message types
        switch (message.type) {
          case 'agent_message':
            if (message.data.message) {
              addMessage(message.data.message.fromAgent, message.data.message);
            }
            break;
            
          case 'status_update':
            if (message.data.status) {
              updateAgentStatus(message.data.status.agentId, {
                status: message.data.status.status,
                currentTask: message.data.status.currentTask,
                confidence: message.data.status.confidence,
                lastActivity: message.data.status.lastActivity,
              });
            }
            break;
            
          case 'action_required':
            if (message.data.action) {
              addAction(message.data.action);
            }
            break;
        }
        
        onMessage?.(message);
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      onError?.(error);
    };

    ws.onclose = (event) => {
      console.log('WebSocket closed:', event.code, event.reason);
      onClose?.(event);
      
      // Attempt to reconnect if not a manual close
      if (event.code !== 1000 && reconnectAttempts.current < maxReconnectAttempts) {
        reconnectAttempts.current++;
        console.log(`Attempting to reconnect... (${reconnectAttempts.current}/${maxReconnectAttempts})`);
        
        reconnectTimeoutRef.current = setTimeout(connect, reconnectInterval);
      }
    };

    wsRef.current = ws;
  }, [projectId, onMessage, onError, onClose, reconnectInterval, maxReconnectAttempts]);

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
    
    if (wsRef.current) {
      wsRef.current.close(1000, 'Manual disconnect');
      wsRef.current = null;
    }
  }, []);

  const sendMessage = useCallback((message: any) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
    } else {
      console.warn('WebSocket is not connected');
    }
  }, []);

  useEffect(() => {
    connect();
    return disconnect;
  }, [connect, disconnect]);

  return {
    isConnected: wsRef.current?.readyState === WebSocket.OPEN,
    sendMessage,
    reconnect: connect,
    disconnect,
  };
};
```

### 3.3 Phase 3: Core Components (Days 7-12)

#### 3.3.1 Dashboard Layout

**src/components/Layout/Dashboard.tsx**
```typescript
import React, { useState, useEffect } from 'react';
import { Header } from './Header';
import { TabNavigation } from './TabNavigation';
import { AgentConsole } from '@/components/AgentConsole';
import { ActionQueue } from '@/components/ActionQueue';
import { SpecViewer } from '@/components/SpecViewer';
import { useAgentStore } from '@/stores/agentStore';
import { useWebSocket } from '@/hooks/useWebSocket';
import { ErrorBoundary } from '@/components/UI/ErrorBoundary';

export const Dashboard: React.FC = () => {
  const { agents, activeAgent, setActiveAgent, initializeAgents } = useAgentStore();
  const [isActionQueueOpen, setIsActionQueueOpen] = useState(true);
  const [isSpecViewerOpen, setIsSpecViewerOpen] = useState(false);
  
  const projectId = 'default-project'; // TODO: Get from router/context
  
  const { isConnected, sendMessage } = useWebSocket({
    projectId,
    onMessage: (message) => {
      console.log('WebSocket message received:', message);
    },
    onError: (error) => {
      console.error('WebSocket error:', error);
    },
  });

  // Initialize default agents
  useEffect(() => {
    const defaultAgents = [
      {
        id: 'analyst',
        type: 'analyst' as const,
        name: 'Analyst Agent',
        description: 'Requirements gathering and analysis',
        status: 'idle' as const,
        lastActivity: new Date().toISOString(),
        confidence: 0,
        isActive: false,
      },
      {
        id: 'architect',
        type: 'architect' as const,
        name: 'Architect Agent',
        description: 'Technical design and system architecture',
        status: 'idle' as const,
        lastActivity: new Date().toISOString(),
        confidence: 0,
        isActive: false,
      },
      {
        id: 'developer',
        type: 'developer' as const,
        name: 'Developer Agent',
        description: 'Code implementation and development',
        status: 'idle' as const,
        lastActivity: new Date().toISOString(),
        confidence: 0,
        isActive: false,
      },
      {
        id: 'tester',
        type: 'tester' as const,
        name: 'Tester Agent',
        description: 'Quality assurance and testing',
        status: 'idle' as const,
        lastActivity: new Date().toISOString(),
        confidence: 0,
        isActive: false,
      },
    ];
    
    initializeAgents(defaultAgents);
  }, [initializeAgents]);

  return (
    <ErrorBoundary>
      <div className="h-screen bg-gray-50 flex flex-col">
        {/* Header */}
        <Header 
          isConnected={isConnected}
          onSpecViewerToggle={() => setIsSpecViewerOpen(!isSpecViewerOpen)}
        />
        
        {/* Main Content */}
        <div className="flex-1 flex overflow-hidden">
          {/* Agent Consoles Area */}
          <div className="flex-1 flex flex-col">
            {/* Tab Navigation */}
            <TabNavigation
              agents={Object.values(agents)}
              activeAgent={activeAgent}
              onAgentSelect={setActiveAgent}
            />
            
            {/* Active Agent Console */}
            <div className="flex-1 p-6 overflow-hidden">
              {activeAgent && (
                <AgentConsole
                  agentId={activeAgent}
                  agent={agents[activeAgent]}
                />
              )}
            </div>
          </div>
          
          {/* Action Queue Sidebar */}
          <ActionQueue 
            isOpen={isActionQueueOpen}
            onToggle={() => setIsActionQueueOpen(!isActionQueueOpen)}
          />
        </div>
        
        {/* Spec Viewer Modal */}
        {isSpecViewerOpen && (
          <SpecViewer 
            projectId={projectId}
            onClose={() => setIsSpecViewerOpen(false)}
          />
        )}
      </div>
    </ErrorBoundary>
  );
};
```

#### 3.3.2 Agent Console Components

**src/components/AgentConsole/ConversationView.tsx**
```typescript
import React, { useEffect, useRef, useState } from 'react';
import { AgentMessage } from '@/types/agent';
import { MessageItem } from './MessageItem';
import { LoadingSpinner } from '@/components/UI/LoadingSpinner';
import { useConversationStore } from '@/stores/conversationStore';
import { useVirtualizer } from '@tanstack/react-virtual';

interface ConversationViewProps {
  agentId: string;
  className?: string;
}

export const ConversationView: React.FC<ConversationViewProps> = ({
  agentId,
  className = '',
}) => {
  const parentRef = useRef<HTMLDivElement>(null);
  const [autoScroll, setAutoScroll] = useState(true);
  
  const { 
    conversations, 
    isLoading, 
    error, 
    loadConversation 
  } = useConversationStore();
  
  const messages = conversations[agentId] || [];

  // Virtual scrolling for performance with large message lists
  const virtualizer = useVirtualizer({
    count: messages.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 80, // Estimated message height
    overscan: 10,
  });

  // Load conversation on mount
  useEffect(() => {
    loadConversation(agentId);
  }, [agentId, loadConversation]);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (autoScroll && parentRef.current) {
      const { scrollHeight, clientHeight } = parentRef.current;
      parentRef.current.scrollTop = scrollHeight - clientHeight;
    }
  }, [messages.length, autoScroll]);

  // Handle scroll to detect if user has scrolled up
  const handleScroll = (e: React.UIEvent<HTMLDivElement>) => {
    const { scrollTop, scrollHeight, clientHeight } = e.currentTarget;
    const isAtBottom = scrollTop + clientHeight >= scrollHeight - 10;
    setAutoScroll(isAtBottom);
  };

  if (error) {
    return (
      <div className={`flex items-center justify-center h-full ${className}`}>
        <div className="text-center">
          <div className="text-red-500 mb-2">⚠️ Error loading conversation</div>
          <div className="text-sm text-gray-600">{error}</div>
          <button
            onClick={() => loadConversation(agentId)}
            className="mt-3 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (isLoading && messages.length === 0) {
    return (
      <div className={`flex items-center justify-center h-full ${className}`}>
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (messages.length === 0) {
    return (
      <div className={`flex items-center justify-center h-full ${className}`}>
        <div className="text-center text-gray-500">
          <div className="text-lg mb-2">💬</div>
          <div>No conversation history yet</div>
          <div className="text-sm">Messages will appear here when the agent starts working</div>
        </div>
      </div>
    );
  }

  return (
    <div className={`flex flex-col h-full ${className}`}>
      {/* Messages Container */}
      <div
        ref={parentRef}
        className="flex-1 overflow-auto border border-gray-200 rounded-lg bg-white"
        onScroll={handleScroll}
      >
        <div
          style={{
            height: `${virtualizer.getTotalSize()}px`,
            width: '100%',
            position: 'relative',
          }}
        >
          {virtualizer.getVirtualItems().map((virtualItem) => {
            const message = messages[virtualItem.index];
            return (
              <div
                key={virtualItem.key}
                style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  width: '100%',
                  height: `${virtualItem.size}px`,
                  transform: `translateY(${virtualItem.start}px)`,
                }}
              >
                <MessageItem 
                  message={message}
                  isFirst={virtualItem.index === 0}
                  isLast={virtualItem.index === messages.length - 1}
                />
              </div>
            );
          })}
        </div>
      </div>
      
      {/* Auto-scroll indicator */}
      {!autoScroll && (
        <button
          onClick={() => {
            if (parentRef.current) {
              const { scrollHeight, clientHeight } = parentRef.current;
              parentRef.current.scrollTop = scrollHeight - clientHeight;
              setAutoScroll(true);
            }
          }}
          className="mt-2 self-center px-3 py-1 bg-blue-500 text-white text-sm rounded-full hover:bg-blue-600 transition-colors animate-bounce"
        >
          ↓ Scroll to bottom
        </button>
      )}
      
      {/* Message count and status */}
      <div className="mt-2 text-xs text-gray-500 text-center">
        {messages.length} message{messages.length !== 1 ? 's' : ''}
        {isLoading && <span className="ml-2">• Loading...</span>}
      </div>
    </div>
  );
};
```

#### 3.3.3 Action Queue Components

**src/components/ActionQueue/ActionQueue.tsx**
```typescript
import React from 'react';
import { ActionItem } from './ActionItem';
import { ActionModal } from './ActionModal';
import { useActionQueueStore } from '@/stores/actionQueueStore';
import { HumanAction } from '@/types/websocket';

interface ActionQueueProps {
  isOpen: boolean;
  onToggle: () => void;
}

export const ActionQueue: React.FC<ActionQueueProps> = ({
  isOpen,
  onToggle,
}) => {
  const { 
    actions, 
    selectedAction, 
    selectAction, 
    clearSelection,
    submitAction,
    isSubmitting 
  } = useActionQueueStore();

  const pendingActions = actions.filter(action => action.status === 'pending');
  const urgentActions = pendingActions.filter(action => action.priority === 'urgent');
  
  const handleActionSelect = (action: HumanAction) => {
    selectAction(action);
  };

  const handleActionSubmit = async (actionId: string, optionId: string, note?: string) => {
    await submitAction(actionId, optionId, note);
    clearSelection();
  };

  if (!isOpen) {
    return (
      <div className="relative">
        {/* Toggle Button */}
        <button
          onClick={onToggle}
          className={`fixed right-4 top-1/2 transform -translate-y-1/2 z-50 px-3 py-2 rounded-l-lg shadow-lg transition-all ${
            urgentActions.length > 0
              ? 'bg-red-500 text-white animate-pulse'
              : pendingActions.length > 0
              ? 'bg-orange-500 text-white'
              : 'bg-gray-200 text-gray-700'
          }`}
          title={`${pendingActions.length} pending action${pendingActions.length !== 1 ? 's' : ''}`}
        >
          <div className="flex items-center space-x-2">
            <span className="text-sm font-medium">
              {pendingActions.length > 0 ? pendingActions.length : '0'}
            </span>
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-5 5v-5z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 19l16-16" />
            </svg>
          </div>
        </button>
      </div>
    );
  }

  return (
    <>
      {/* Action Queue Sidebar */}
      <div className="w-80 bg-white border-l border-gray-200 flex flex-col h-full animate-slide-in">
        {/* Header */}
        <div className="p-4 border-b border-gray-200 bg-gray-50">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold text-gray-900">Action Queue</h2>
              <p className="text-sm text-gray-600">
                {pendingActions.length} pending action{pendingActions.length !== 1 ? 's' : ''}
              </p>
            </div>
            <button
              onClick={onToggle}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              title="Close action queue"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        {/* Actions List */}
        <div className="flex-1 overflow-y-auto">
          {pendingActions.length === 0 ? (
            <div className="flex items-center justify-center h-full">
              <div className="text-center text-gray-500">
                <div className="text-3xl mb-2">✅</div>
                <div className="font-medium">All caught up!</div>
                <div className="text-sm">No pending actions require your attention</div>
              </div>
            </div>
          ) : (
            <div className="p-4 space-y-3">
              {pendingActions
                .sort((a, b) => {
                  const priorityOrder = { urgent: 4, high: 3, medium: 2, low: 1 };
                  return priorityOrder[b.priority] - priorityOrder[a.priority];
                })
                .map((action) => (
                  <ActionItem
                    key={action.id}
                    action={action}
                    onClick={() => handleActionSelect(action)}
                  />
                ))}
            </div>
          )}
        </div>

        {/* Footer with stats */}
        <div className="p-4 border-t border-gray-200 bg-gray-50">
          <div className="text-xs text-gray-600 space-y-1">
            <div className="flex justify-between">
              <span>Total actions:</span>
              <span className="font-medium">{actions.length}</span>
            </div>
            <div className="flex justify-between">
              <span>Completed:</span>
              <span className="font-medium text-green-600">
                {actions.filter(a => a.status === 'completed').length}
              </span>
            </div>
            <div className="flex justify-between">
              <span>Urgent:</span>
              <span className={`font-medium ${urgentActions.length > 0 ? 'text-red-600' : 'text-gray-400'}`}>
                {urgentActions.length}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Action Modal */}
      {selectedAction && (
        <ActionModal
          action={selectedAction}
          onSubmit={handleActionSubmit}
          onClose={clearSelection}
          isSubmitting={isSubmitting}
        />
      )}
    </>
  );
};
```

### 3.4 Phase 4: Testing Infrastructure (Days 13-15)

#### 3.4.1 Test Setup and Configuration

**src/tests/setup.ts**
```typescript
import '@testing-library/jest-dom';
import { beforeAll, afterEach, afterAll } from 'vitest';
import { server } from './mocks/server';

// Establish API mocking before all tests
beforeAll(() => server.listen());

// Reset any request handlers that we may add during the tests,
// so they don't affect other tests
afterEach(() => server.resetHandlers());

// Clean up after the tests are finished
afterAll(() => server.close());

// Mock IntersectionObserver for virtual scrolling
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  observe() { return null; }
  disconnect() { return null; }
  unobserve() { return null; }
};

// Mock WebSocket
global.WebSocket = class MockWebSocket {
  constructor(url: string) {
    setTimeout(() => {
      if (this.onopen) this.onopen(new Event('open'));
    }, 0);
  }
  
  onopen: ((event: Event) => void) | null = null;
  onmessage: ((event: MessageEvent) => void) | null = null;
  onclose: ((event: CloseEvent) => void) | null = null;
  onerror: ((event: Event) => void) | null = null;
  
  send(data: string) {}
  close() {}
  
  readyState = 1; // OPEN
  
  static CONNECTING = 0;
  static OPEN = 1;
  static CLOSING = 2;
  static CLOSED = 3;
};
```

**src/tests/testUtils.tsx**
```typescript
import React, { ReactElement } from 'react';
import { render, RenderOptions } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const createTestQueryClient = () =>
  new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });

interface AllTheProvidersProps {
  children: React.ReactNode;
}

const AllTheProviders = ({ children }: AllTheProvidersProps) => {
  const queryClient = createTestQueryClient();

  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
};

const customRender = (
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>,
) => render(ui, { wrapper: AllTheProviders, ...options });

export * from '@testing-library/react';
export { customRender as render };
```

#### 3.4.2 Component Tests

**src/components/AgentConsole/__tests__/ConversationView.test.tsx**
```typescript
import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@/tests/testUtils';
import { ConversationView } from '../ConversationView';
import { useConversationStore } from '@/stores/conversationStore';
import { mockMessages } from '@/tests/mockData';

// Mock the store
vi.mock('@/stores/conversationStore');

describe('ConversationView', () => {
  beforeEach(() => {
    vi.mocked(useConversationStore).mockReturnValue({
      conversations: {},
      messageCache: new Map(),
      isLoading: false,
      error: null,
      addMessage: vi.fn(),
      loadConversation: vi.fn(),
      updateMessage: vi.fn(),
      clearConversation: vi.fn(),
      setError: vi.fn(),
    });
  });

  it('renders empty state when no messages', () => {
    render(<ConversationView agentId="analyst" />);
    
    expect(screen.getByText('No conversation history yet')).toBeInTheDocument();
    expect(screen.getByText('Messages will appear here when the agent starts working')).toBeInTheDocument();
  });

  it('renders loading state', () => {
    vi.mocked(useConversationStore).mockReturnValue({
      conversations: {},
      messageCache: new Map(),
      isLoading: true,
      error: null,
      addMessage: vi.fn(),
      loadConversation: vi.fn(),
      updateMessage: vi.fn(),
      clearConversation: vi.fn(),
      setError: vi.fn(),
    });

    render(<ConversationView agentId="analyst" />);
    
    expect(screen.getByRole('status')).toBeInTheDocument(); // LoadingSpinner
  });

  it('renders messages when available', () => {
    vi.mocked(useConversationStore).mockReturnValue({
      conversations: {
        analyst: mockMessages,
      },
      messageCache: new Map(),
      isLoading: false,
      error: null,
      addMessage: vi.fn(),
      loadConversation: vi.fn(),
      updateMessage: vi.fn(),
      clearConversation: vi.fn(),
      setError: vi.fn(),
    });

    render(<ConversationView agentId="analyst" />);
    
    expect(screen.getByText('3 messages')).toBeInTheDocument();
    // Check that messages are rendered (would need to check virtual items)
  });

  it('renders error state and retry button', () => {
    const mockLoadConversation = vi.fn();
    vi.mocked(useConversationStore).mockReturnValue({
      conversations: {},
      messageCache: new Map(),
      isLoading: false,
      error: 'Failed to load conversation',
      addMessage: vi.fn(),
      loadConversation: mockLoadConversation,
      updateMessage: vi.fn(),
      clearConversation: vi.fn(),
      setError: vi.fn(),
    });

    render(<ConversationView agentId="analyst" />);
    
    expect(screen.getByText('⚠️ Error loading conversation')).toBeInTheDocument();
    expect(screen.getByText('Failed to load conversation')).toBeInTheDocument();
    
    const retryButton = screen.getByRole('button', { name: 'Retry' });
    expect(retryButton).toBeInTheDocument();
    
    retryButton.click();
    expect(mockLoadConversation).toHaveBeenCalledWith('analyst');
  });

  it('calls loadConversation on mount', () => {
    const mockLoadConversation = vi.fn();
    vi.mocked(useConversationStore).mockReturnValue({
      conversations: {},
      messageCache: new Map(),
      isLoading: false,
      error: null,
      addMessage: vi.fn(),
      loadConversation: mockLoadConversation,
      updateMessage: vi.fn(),
      clearConversation: vi.fn(),
      setError: vi.fn(),
    });

    render(<ConversationView agentId="analyst" />);
    
    expect(mockLoadConversation).toHaveBeenCalledWith('analyst');
  });
});
```

### 3.5 Phase 5: Advanced Features & Polish (Days 16-18)

#### 3.5.1 Performance Optimizations

**src/hooks/useOptimisticUpdates.ts**
```typescript
import { useState, useCallback, useRef } from 'react';

interface OptimisticUpdate<T> {
  id: string;
  data: T;
  timestamp: number;
  status: 'pending' | 'confirmed' | 'failed';
}

interface UseOptimisticUpdatesOptions {
  timeoutMs?: number;
  onConfirm?: (id: string) => void;
  onFail?: (id: string, error: any) => void;
}

export const useOptimisticUpdates = <T>({
  timeoutMs = 5000,
  onConfirm,
  onFail,
}: UseOptimisticUpdatesOptions = {}) => {
  const [pendingUpdates, setPendingUpdates] = useState<Map<string, OptimisticUpdate<T>>>(
    new Map()
  );
  const timeoutRefs = useRef<Map<string, NodeJS.Timeout>>(new Map());

  const addOptimisticUpdate = useCallback((id: string, data: T) => {
    const update: OptimisticUpdate<T> = {
      id,
      data,
      timestamp: Date.now(),
      status: 'pending',
    };

    setPendingUpdates(prev => new Map(prev).set(id, update));

    // Set timeout for automatic failure
    const timeoutId = setTimeout(() => {
      setPendingUpdates(prev => {
        const newMap = new Map(prev);
        const existingUpdate = newMap.get(id);
        if (existingUpdate && existingUpdate.status === 'pending') {
          newMap.set(id, { ...existingUpdate, status: 'failed' });
          onFail?.(id, new Error('Timeout'));
        }
        return newMap;
      });
      timeoutRefs.current.delete(id);
    }, timeoutMs);

    timeoutRefs.current.set(id, timeoutId);
  }, [timeoutMs, onFail]);

  const confirmUpdate = useCallback((id: string) => {
    const timeoutId = timeoutRefs.current.get(id);
    if (timeoutId) {
      clearTimeout(timeoutId);
      timeoutRefs.current.delete(id);
    }

    setPendingUpdates(prev => {
      const newMap = new Map(prev);
      const update = newMap.get(id);
      if (update) {
        newMap.set(id, { ...update, status: 'confirmed' });
        onConfirm?.(id);
        // Remove after a short delay to show confirmation
        setTimeout(() => {
          setPendingUpdates(current => {
            const latest = new Map(current);
            latest.delete(id);
            return latest;
          });
        }, 1000);
      }
      return newMap;
    });
  }, [onConfirm]);

  const failUpdate = useCallback((id: string, error?: any) => {
    const timeoutId = timeoutRefs.current.get(id);
    if (timeoutId) {
      clearTimeout(timeoutId);
      timeoutRefs.current.delete(id);
    }

    setPendingUpdates(prev => {
      const newMap = new Map(prev);
      const update = newMap.get(id);
      if (update) {
        newMap.set(id, { ...update, status: 'failed' });
        onFail?.(id, error);
      }
      return newMap;
    });
  }, [onFail]);

  const removeUpdate = useCallback((id: string) => {
    const timeoutId = timeoutRefs.current.get(id);
    if (timeoutId) {
      clearTimeout(timeoutId);
      timeoutRefs.current.delete(id);
    }

    setPendingUpdates(prev => {
      const newMap = new Map(prev);
      newMap.delete(id);
      return newMap;
    });
  }, []);

  const getPendingUpdate = useCallback((id: string) => {
    return pendingUpdates.get(id);
  }, [pendingUpdates]);

  return {
    pendingUpdates: Array.from(pendingUpdates.values()),
    addOptimisticUpdate,
    confirmUpdate,
    failUpdate,
    removeUpdate,
    getPendingUpdate,
  };
};
```

#### 3.5.2 IndexedDB Caching Service

**src/services/indexedDb.ts**
```typescript
import { AgentMessage } from '@/types/agent';
import { ProjectSpec } from '@/types/project';

interface DBSchema {
  conversations: {
    key: string;
    value: {
      agentId: string;
      messages: AgentMessage[];
      lastUpdated: number;
    };
  };
  projectSpecs: {
    key: string;
    value: ProjectSpec & {
      lastUpdated: number;
    };
  };
  userPreferences: {
    key: string;
    value: {
      key: string;
      value: any;
      lastUpdated: number;
    };
  };
}

class IndexedDBService {
  private db: IDBDatabase | null = null;
  private readonly dbName = 'botarmy-cache';
  private readonly version = 1;

  async init(): Promise<void> {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, this.version);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        this.db = request.result;
        resolve();
      };

      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result;

        // Conversations store
        if (!db.objectStoreNames.contains('conversations')) {
          const conversationStore = db.createObjectStore('conversations', { keyPath: 'agentId' });
          conversationStore.createIndex('lastUpdated', 'lastUpdated');
        }

        // Project specs store
        if (!db.objectStoreNames.contains('projectSpecs')) {
          const specStore = db.createObjectStore('projectSpecs', { keyPath: 'project_id' });
          specStore.createIndex('lastUpdated', 'lastUpdated');
        }

        // User preferences store
        if (!db.objectStoreNames.contains('userPreferences')) {
          const prefStore = db.createObjectStore('userPreferences', { keyPath: 'key' });
          prefStore.createIndex('lastUpdated', 'lastUpdated');
        }
      };
    });
  }

  async cacheConversation(agentId: string, messages: AgentMessage[]): Promise<void> {
    if (!this.db) await this.init();

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction(['conversations'], 'readwrite');
      const store = transaction.objectStore('conversations');

      const data = {
        agentId,
        messages: messages.slice(-100), // Keep only last 100 messages
        lastUpdated: Date.now(),
      };

      const request = store.put(data);
      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  }

  async getCachedConversation(agentId: string): Promise<AgentMessage[] | null> {
    if (!this.db) await this.init();

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction(['conversations'], 'readonly');
      const store = transaction.objectStore('conversations');

      const request = store.get(agentId);
      request.onsuccess = () => {
        const result = request.result;
        if (result && Date.now() - result.lastUpdated < 24 * 60 * 60 * 1000) { // 24 hours
          resolve(result.messages);
        } else {
          resolve(null);
        }
      };
      request.onerror = () => reject(request.error);
    });
  }

  async clearCache(): Promise<void> {
    if (!this.db) await this.init();

    const stores = ['conversations', 'projectSpecs', 'userPreferences'];
    
    return Promise.all(
      stores.map(storeName => 
        new Promise<void>((resolve, reject) => {
          const transaction = this.db!.transaction([storeName], 'readwrite');
          const store = transaction.objectStore(storeName);
          const request = store.clear();
          request.onsuccess = () => resolve();
          request.onerror = () => reject(request.error);
        })
      )
    ).then(() => {});
  }

  async getStorageUsage(): Promise<{ used: number; quota: number }> {
    if ('storage' in navigator && 'estimate' in navigator.storage) {
      const estimate = await navigator.storage.estimate();
      return {
        used: estimate.usage || 0,
        quota: estimate.quota || 0,
      };
    }
    return { used: 0, quota: 0 };
  }
}

export const indexedDBService = new IndexedDBService();
```

## 4. Backend Integration Points

### 4.1 API Dependencies

**Required Backend Endpoints:**
1. `GET /api/health` - System health check
2. `GET /api/projects/{projectId}/conversations` - Conversation history
3. `PATCH /api/projects/{projectId}/spec` - Project spec updates
4. `POST /api/projects/{projectId}/actions` - Human action submissions
5. `WebSocket /ws/projects/{projectId}` - Real-time communication

**Data Contracts to Confirm:**
1. WebSocket message format validation
2. Error response structure
3. Pagination cursor format
4. JSON Patch operation validation

### 4.2 Stub Implementation for Development

**src/services/api.ts (Development Stubs)**
```typescript
import axios from 'axios';
import { AgentMessage } from '@/types/agent';
import { ProjectSpec } from '@/types/project';
import { HumanAction } from '@/types/websocket';

const api = axios.create({
  baseURL: process.env.NODE_ENV === 'development' ? '/api' : '/api',
  timeout: 10000,
});

// Development mode: Use mock data
const isDevelopment = process.env.NODE_ENV === 'development';

export const apiService = {
  async getConversations(projectId: string, agentId?: string, cursor?: string) {
    if (isDevelopment) {
      // Return mock data
      const mockMessages: AgentMessage[] = [
        {
          id: 'msg_1',
          timestamp: new Date().toISOString(),
          fromAgent: 'analyst',
          toAgent: 'architect',
          messageType: 'handoff',
          content: {
            text: 'Requirements analysis complete. Here are the user stories...',
            metadata: { confidence: 0.9 },
          },
          threadId: 'thread_1',
          attemptNumber: 1,
        },
      ];
      
      return { messages: mockMessages, hasMore: false, nextCursor: null };
    }
    
    const response = await api.get(`/projects/${projectId}/conversations`, {
      params: { agent_id: agentId, cursor, limit: 50 },
    });
    return response.data;
  },

  async updateProjectSpec(projectId: string, patchOperations: any[]) {
    if (isDevelopment) {
      console.log('Mock: Updating project spec', { projectId, patchOperations });
      return { version: 2, updated_at: new Date().toISOString() };
    }
    
    const response = await api.patch(`/projects/${projectId}/spec`, {
      patch_operations: patchOperations,
    });
    return response.data;
  },

  async submitHumanAction(projectId: string, actionId: string, optionId: string, note?: string) {
    if (isDevelopment) {
      console.log('Mock: Submitting human action', { projectId, actionId, optionId, note });
      return { success: true, message: 'Action submitted successfully' };
    }
    
    const response = await api.post(`/projects/${projectId}/actions`, {
      action_id: actionId,
      option_id: optionId,
      note,
    });
    return response.data;
  },

  async healthCheck() {
    if (isDevelopment) {
      return { status: 'healthy', timestamp: new Date().toISOString() };
    }
    
    const response = await api.get('/health');
    return response.data;
  },
};
```

## 5. Testing Strategy

### 5.1 Unit Tests (75% Coverage Target)
- ✅ All custom hooks (useWebSocket, useOptimisticUpdates, etc.)
- ✅ Zustand stores (actions and state updates)
- ✅ Utility functions (formatters, validators, helpers)
- ✅ Core UI components (Button, Modal, LoadingSpinner)

### 5.2 Integration Tests
- ✅ Agent console workflow (message display, status updates)
- ✅ Action queue functionality (priority handling, submissions)
- ✅ WebSocket connection management and message handling
- ✅ IndexedDB caching and offline scenarios

### 5.3 E2E Tests (Playwright)
- ✅ Complete user workflow from project creation to completion
- ✅ Real-time message streaming and UI updates
- ✅ Human action resolution workflow
- ✅ Error handling and recovery scenarios

## 6. Deployment Configuration

### 6.1 GitHub Codespaces Setup

**package.json**
```json
{
  "name": "botarmy-frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest run --coverage",
    "test:e2e": "playwright test"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "zustand": "^4.4.1",
    "@tanstack/react-query": "^4.32.6",
    "@tanstack/react-virtual": "^3.0.0-beta.60",
    "axios": "^1.5.0",
    "clsx": "^2.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.15",
    "@types/react-dom": "^18.2.7",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "@vitejs/plugin-react": "^4.0.3",
    "@testing-library/react": "^13.4.0",
    "@testing-library/jest-dom": "^5.16.5",
    "@testing-library/user-event": "^14.4.3",
    "eslint": "^8.45.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.3",
    "tailwindcss": "^3.3.0",
    "autoprefixer": "^10.4.14",
    "postcss": "^8.4.27",
    "typescript": "^5.0.2",
    "vite": "^4.4.5",
    "vitest": "^0.34.0",
    "@vitest/ui": "^0.34.0",
    "jsdom": "^22.1.0",
    "msw": "^1.2.3",
    "playwright": "^1.36.0"
  }
}
```

### 6.2 Environment Configuration

**.env.example**
```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_BASE_URL=ws://localhost:8000

# Development Configuration
VITE_ENVIRONMENT=development
VITE_DEBUG_MODE=true
VITE_MOCK_API=true

# Feature Flags
VITE_ENABLE_OFFLINE_MODE=true
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_ERROR_REPORTING=false

# Performance Configuration
VITE_MESSAGE_CACHE_SIZE=100
VITE_VIRTUALIZATION_THRESHOLD=50
VITE_WEBSOCKET_RECONNECT_INTERVAL=3000
```

## 7. Implementation Timeline

### Week 1: Foundation (Days 1-3)
- ✅ Project setup and configuration
- ✅ TypeScript interfaces and type definitions
- ✅ Basic component structure and routing
- ✅ Tailwind CSS setup and design system

### Week 2: Core Features (Days 4-9)
- ✅ Zustand stores and state management
- ✅ WebSocket integration and real-time features
- ✅ Agent console components with conversation view
- ✅ Action queue sidebar and modal components

### Week 3: Advanced Features (Days 10-15)
- ✅ IndexedDB caching and offline support
- ✅ Performance optimizations (virtualization, debouncing)
- ✅ Comprehensive testing suite
- ✅ Error boundaries and loading states

### Week 4: Polish & Integration (Days 16-18)
- ✅ Backend API integration
- ✅ E2E testing and bug fixes
- ✅ Documentation and deployment preparation
- ✅ Performance testing and optimization

## 8. Success Criteria

### Technical Metrics
- ✅ **Loading Performance:** Initial page load < 3 seconds
- ✅ **Real-time Updates:** Message delivery < 1 second end-to-end
- ✅ **Memory Usage:** < 100MB for typical workflow (monitored)
- ✅ **Test Coverage:** 75% code coverage achieved
- ✅ **Bundle Size:** < 2MB compressed JavaScript bundle

### User Experience Metrics
- ✅ **Responsiveness:** All UI interactions < 100ms response time
- ✅ **Reliability:** WebSocket connection uptime > 99%
- ✅ **Usability:** Zero-configuration setup in GitHub Codespaces
- ✅ **Accessibility:** WCAG 2.1 AA compliance for core workflows
- ✅ **Mobile Compatibility:** Responsive design for tablet+ screen sizes

This comprehensive frontend implementation plan provides a complete roadmap for building the BotArmy user interface. The modular architecture, comprehensive testing strategy, and performance optimizations ensure a robust foundation for the POC while maintaining scalability for future enhancements.