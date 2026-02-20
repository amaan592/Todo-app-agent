# Data Model: AI Agent Integration

**Feature**: AI Agent Integration (002-ai-agent-integration)
**Created**: 2026-02-19
**Purpose**: Document data models used by the AI Agent

---

## Overview

The AI Agent does **not** introduce new data models. It operates exclusively on the existing Todo data model through the backend API.

This document describes the existing model for reference and agent implementation context.

---

## Existing Data Model: Task

**Source**: `backend/src/models/task.py`

### Entity: Task

Represents a single todo item in the system.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| id | integer | Unique task identifier | Auto-increment, primary key |
| title | string | Task title/name | Required, max 200 characters |
| description | string | Detailed task description | Optional, max 1000 characters |
| status | enum | Task completion status | PENDING or COMPLETED, default PENDING |
| created_at | datetime | Task creation timestamp | Auto-generated on creation |

### Status Enum Values

| Value | Description |
|-------|-------------|
| PENDING | Task is not yet completed |
| COMPLETED | Task has been marked complete |

### State Transitions

```
PENDING ←→ COMPLETED
```

- New tasks always start as PENDING
- Users can mark PENDING tasks as COMPLETED
- Users can mark COMPLETED tasks back to PENDING (redo)
- No other status transitions exist

---

## Agent Interaction Model

The AI Agent interacts with the Task entity **only** through backend API endpoints:

### Read Operations

| Operation | Endpoint | Agent Tool | Parameters |
|-----------|----------|------------|------------|
| Get all tasks | GET /api/v1/tasks | get_tasks() | status (optional) |
| Get single task | GET /api/v1/tasks/{id} | (internal) | task_id |

### Write Operations

| Operation | Endpoint | Agent Tool | Parameters |
|-----------|----------|------------|------------|
| Create task | POST /api/v1/tasks | create_task() | title, description (optional) |
| Update task | PUT /api/v1/tasks/{id} | update_task() | task_id, fields (dict) |
| Delete task | DELETE /api/v1/tasks/{id} | delete_task() | task_id |

---

## Data Validation Rules

### Creation Validation

- **title**: Required, non-empty string, max 200 characters
- **description**: Optional, max 1000 characters if provided
- **status**: Auto-set to PENDING on creation

### Update Validation

- **task_id**: Must reference existing task
- **fields**: Only title, description, status can be updated
- **status**: Must be valid enum value (PENDING or COMPLETED)

### Deletion Validation

- **task_id**: Must reference existing task
- Deletion is permanent (no soft delete)

---

## Agent Data Handling Rules

### What the Agent CAN Do

- Read task data through API responses
- Extract task IDs, titles, descriptions from API responses
- Use task data to generate human-readable responses
- Validate user input against known task constraints

### What the Agent CANNOT Do

- Access database directly (Constitution Principle II)
- Modify data model or schema
- Bypass backend validation
- Store task data independently
- Create new entity types

---

## Example Task Data

### Single Task Response

```json
{
  "id": 3,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, vegetables",
  "status": "PENDING",
  "created_at": "2026-02-19T10:30:00Z"
}
```

### Multiple Tasks Response

```json
[
  {
    "id": 1,
    "title": "Finish project report",
    "description": "Complete Q1 analysis",
    "status": "PENDING",
    "created_at": "2026-02-18T09:00:00Z"
  },
  {
    "id": 2,
    "title": "Call dentist",
    "description": null,
    "status": "COMPLETED",
    "created_at": "2026-02-17T14:20:00Z"
  }
]
```

---

## References

- Backend Model: `backend/src/models/task.py`
- Backend Schema: `backend/src/schemas/task.py`
- API Endpoints: `backend/src/api/tasks.py`
- Agent Tools: [contracts/agent-tools.yaml](./contracts/agent-tools.yaml)
