# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a multi-agent scheduling system demonstrating the Agent-to-Agent (A2A) protocol. Four agents (Host/Brandon, Karley, Nate, Kaitlynn) collaborate to schedule pickleball games, each built with different frameworks (Google ADK, CrewAI, LangGraph) to showcase interoperability.

## Common Development Commands

### Running Individual Agents

Each agent runs on its own port and requires environment setup:

```bash
# Kaitlynn (LangGraph) - Port 10004
cd kaitlynn_agent_langgraph && uv run --active app/__main__.py

# Nate (CrewAI) - Port 10003
cd nate_agent_crewai && uv run --active .

# Karley (ADK) - Port 10002
cd karley_agent_adk && uv run --active .

# Host/Brandon (ADK) - Port 10001
cd host_agent_adk && uv run --active adk web
```

### Environment Setup

Before running any agent:
1. Create `.env` file with `GOOGLE_API_KEY=your-api-key`
2. Use `uv` package manager (Python 3.13 required)
3. Virtual environment is handled automatically by `uv run`

### Running Full System

1. Start all four agents in separate terminals
2. Access Host Agent web interface at http://localhost:10001
3. Click "Schedule a pickleball game" to initiate the process

## Architecture

### Agent Communication Flow
```
User → Host Agent (10001) → Friend Agents (10002-10004) → A2A Protocol
         ↓                      ↓
    Orchestrates           Check availability
    scheduling             Return preferences
         ↓                      ↓
    Book court ← Find common time slot
```

### Key Components

1. **A2A Protocol Layer**: Each agent has an `agent_executor.py` that handles A2A message routing
2. **Agent-Specific Logic**: Core agent behavior in each module's `agent.py`
3. **Tools**: Framework-specific tool implementations (e.g., `get_availability`, `book_pickleball_court`)
4. **Session Management**: Each agent maintains session state for conversations

### Framework Patterns

- **ADK Agents** (Host, Karley): Use `@genkit.action` decorators for tools
- **CrewAI Agent** (Nate): Uses `Agent` and `Task` classes with custom tools
- **LangGraph Agent** (Kaitlynn): Uses StateGraph with nodes and edges for flow control

### Important Design Decisions

1. **Port Allocation**: Fixed ports (10001-10004) for each agent
2. **In-Memory Storage**: Court bookings stored in memory (resets on restart)
3. **Mock Calendars**: Friend agents use random availability generation
4. **Async Operations**: Heavy use of async/await for concurrent agent communication
5. **Error Handling**: Connection failures handled gracefully with fallback responses

## Memories