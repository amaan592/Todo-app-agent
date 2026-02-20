# Data Model: Todo Application

## Task Entity

### Fields
- **id**: Integer (Primary Key, Auto-generated)
  - Unique identifier for each task
  - Auto-incremented by the database
- **title**: String (Required, Max length: 255)
  - The main text/description of the task
  - Cannot be empty or null
- **description**: String (Optional, Max length: 1000)
  - Extended details about the task
  - Can be null or empty
- **status**: Enum (Required, Values: "PENDING", "COMPLETED")
  - Current state of the task
  - Defaults to "PENDING"
- **created_at**: DateTime (Auto-generated)
  - Timestamp when the task was created
  - Automatically set by the system

### Validation Rules
- **title**: Required field, minimum length 1 character, maximum length 255 characters
- **description**: Optional field, maximum length 1000 characters
- **status**: Required field, must be one of the allowed enum values ("PENDING", "COMPLETED")
- **id**: System-generated, unique constraint enforced by database
- **created_at**: System-generated timestamp, cannot be modified by user

### Relationships
- No relationships to other entities (standalone entity)

### State Transitions
- **PENDING → COMPLETED**: When user marks task as completed
- **COMPLETED → PENDING**: When user reopens/activates a completed task

## API Data Transfer Objects (DTOs)

### TaskRequest DTO
Used for creating and updating tasks
- **title**: String (Required) - The task title
- **description**: String (Optional) - Extended task details
- **status**: String (Optional) - Task status ("PENDING" or "COMPLETED"), defaults to "PENDING"

### TaskResponse DTO
Used for returning task data to clients
- **id**: Integer - The unique task identifier
- **title**: String - The task title
- **description**: String - Extended task details (nullable)
- **status**: String - Current task status ("PENDING" or "COMPLETED")
- **created_at**: String (ISO 8601 format) - Creation timestamp

## Database Schema

### Tasks Table
```
Table: tasks
- id (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- title (VARCHAR(255), NOT NULL)
- description (TEXT, NULLABLE)
- status (VARCHAR(20), NOT NULL, DEFAULT 'PENDING')
- created_at (DATETIME, NOT NULL, DEFAULT CURRENT_TIMESTAMP)
```

### Indexes
- Primary key index on `id`
- Consider adding index on `status` if filtering by status becomes frequent

## Backend Model (FastAPI/SQLAlchemy)

```python
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

## Frontend Model (TypeScript Interface)

```typescript
interface Task {
  id: number;
  title: string;
  description?: string;
  status: 'PENDING' | 'COMPLETED';
  created_at: string; // ISO 8601 format
}
```