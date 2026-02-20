# Quick Start: AI Agent Integration

**Feature**: AI Agent Integration (002-ai-agent-integration)
**Created**: 2026-02-19
**Purpose**: Setup and usage instructions for the AI Agent

---

## Prerequisites

Before setting up the AI Agent, ensure:

- ✅ Python 3.9+ installed
- ✅ Backend Todo API is operational
- ✅ Backend dependencies installed (`pip install -r backend/requirements.txt`)
- ✅ Backend server running on `http://localhost:8000`

---

## Setup Instructions

### 1. Install Agent Dependencies

The AI Agent uses the existing backend Python environment. No additional dependencies required if backend is already set up.

If starting fresh:

```bash
cd backend
pip install -r requirements.txt
```

### 2. Verify Backend Connectivity

Test that the backend API is accessible:

```bash
curl http://localhost:8000/api/v1/tasks
```

Expected response: `[]` (empty task list) or existing tasks

### 3. Configure Backend URL (if needed)

If backend runs on a different port or host, update the agent configuration:

```python
# backend/src/agent/executor.py
BACKEND_URL = "http://localhost:8000"  # Update if needed
```

---

## Running the AI Agent

### Interactive Mode (CLI)

```bash
cd backend
python -m src.agent.cli
```

Example session:
```
AI Agent: Hello! I can help you manage your tasks. What would you like to do?
You: Add a task to buy groceries
AI Agent: ✅ Task #1 created: Buy groceries
You: Show me my tasks
AI Agent: 📋 You have 1 task:
         #1: Buy groceries (Pending)
You: Mark task 1 complete
AI Agent: ✅ Task #1 updated. Status is now COMPLETED
You: Delete task 1
AI Agent: ✅ Task #1 deleted: Buy groceries
```

### Programmatic Usage

```python
from src.agent.executor import AgentExecutor

async def main():
    agent = AgentExecutor()
    
    # Create a task
    result = await agent.execute("Add a task to finish the project report")
    print(result)
    
    # Get tasks
    result = await agent.execute("Show me my tasks")
    print(result)
    
    # Update a task
    result = await agent.execute("Mark task 1 complete")
    print(result)
    
    # Delete a task
    result = await agent.execute("Delete task 1")
    print(result)

# Run the agent
import asyncio
asyncio.run(main())
```

---

## Supported Instructions

### Create Tasks

| Example | Action |
|---------|--------|
| "Add a task to buy groceries" | Creates task with title "Buy groceries" |
| "Create a new task: Finish project report" | Creates task with title "Finish project report" |
| "I need to call the dentist" | Creates task with title "Call the dentist" |
| "Add task: Review documents - due Monday" | Creates task with title and description |

### Retrieve Tasks

| Example | Action |
|---------|--------|
| "Show me my tasks" | Returns all tasks |
| "What are my pending tasks?" | Returns only PENDING tasks |
| "List all completed tasks" | Returns only COMPLETED tasks |
| "What do I have to do?" | Returns all PENDING tasks |

### Update Tasks

| Example | Action |
|---------|--------|
| "Mark task 1 complete" | Sets task #1 status to COMPLETED |
| "I finished task 3" | Sets task #3 status to COMPLETED |
| "Mark task 2 as pending" | Sets task #2 status to PENDING |
| "I need to redo task 5" | Sets task #5 status back to PENDING |

### Delete Tasks

| Example | Action |
|---------|--------|
| "Delete task 2" | Deletes task #2 |
| "Remove the grocery task" | Deletes task matching "grocery" (asks for clarification if multiple match) |
| "Cancel task 4" | Deletes task #4 |

---

## Error Handling

### Missing Information

```
You: Add a task
AI Agent: I need a bit more information. What would you like to name this task?
```

### Invalid Task ID

```
You: Delete task 999
AI Agent: I couldn't find task #999. Would you like to see your current tasks?
```

### Ambiguous Reference

```
You: Delete the meeting task
AI Agent: I found multiple tasks matching "meeting task":
         #3: Team meeting Monday
         #5: Client meeting Wednesday
         Could you specify which one by task ID?
```

### Backend Unavailable

```
You: Add a task to buy groceries
AI Agent: I'm having trouble connecting to the task service. Please try again in a moment.
```

---

## Testing the Agent

### Run Unit Tests

```bash
cd backend
pytest tests/agent/ -v
```

### Run Integration Tests

```bash
cd backend
pytest tests/integration/ -v
```

### Manual Testing

1. Start backend: `python -m uvicorn src.main:app --reload --port 8000`
2. Start agent CLI: `python -m src.agent.cli`
3. Test each instruction type from the supported instructions table
4. Verify database reflects changes: `curl http://localhost:8000/api/v1/tasks`

---

## Troubleshooting

### Agent doesn't recognize my instruction

- Try rephrasing using the example formats above
- Use clear action verbs: "add", "show", "mark", "delete"
- Include task IDs when referencing specific tasks

### Backend connection errors

1. Verify backend is running: `curl http://localhost:8000/api/v1/tasks`
2. Check backend URL configuration in `executor.py`
3. Ensure no firewall blocking localhost connections

### Tests failing

1. Ensure backend is running for integration tests
2. Check test fixtures are loaded
3. Run tests with verbose output: `pytest -v`

---

## Architecture Overview

```
┌─────────────┐
│    User     │
└──────┬──────┘
       │ Natural Language
       ↓
┌─────────────────────┐
│   Intent Parser     │ → Extracts intent + parameters
└──────┬──────────────┘
       │ Selected Tool
       ↓
┌─────────────────────┐
│   Tool Executor     │ → Calls backend API
└──────┬──────────────┘
       │ HTTP Request
       ↓
┌─────────────────────┐
│   Backend API       │ → Validates, processes, persists
└──────┬──────────────┘
       │ JSON Response
       ↓
┌─────────────────────┐
│ Response Generator  │ → Human-readable output
└──────┬──────────────┘
       │ Formatted Response
       ↓
┌─────────────┐
│    User     │
└─────────────┘
```

---

## Next Steps

- Review [data-model.md](./data-model.md) for Task entity details
- Review [contracts/agent-tools.yaml](./contracts/agent-tools.yaml) for tool specifications
- Review [research.md](./research.md) for technical decisions
- See [spec.md](./spec.md) for complete feature requirements

---

## References

- Backend API Documentation: `backend/README.md`
- Agent Implementation: `backend/src/agent/`
- Test Suite: `backend/tests/agent/`
