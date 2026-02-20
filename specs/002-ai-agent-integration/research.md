# Research: AI Agent Integration

**Feature**: AI Agent Integration (002-ai-agent-integration)
**Created**: 2026-02-19
**Purpose**: Resolve all technical unknowns and establish implementation decisions

---

## Decision 1: Natural Language Processing Approach

**What was chosen**: Hybrid rule-based + pattern matching approach using regex and keyword extraction

**Why chosen**: 
- Task management domain has limited, well-defined intent patterns
- Rule-based approach provides deterministic, predictable behavior (Constitution Principle VI)
- Easier to debug and maintain than ML models
- No external API dependencies required
- Sufficient for supported instruction types (create, read, update, delete)

**Alternatives considered**:
- **spaCy**: Full NLP library with NER and dependency parsing. Rejected due to overhead for simple domain
- **NLTK**: Academic NLP library. Rejected due to complexity and performance overhead
- **Transformers/LLM APIs**: Overkill for structured task commands, requires API keys, latency concerns
- **Pure regex**: Too brittle, hard to maintain. Rejected in favor of hybrid approach

**Implementation approach**:
- Define intent patterns as regex with named groups
- Extract entities (task IDs, titles, status) via pattern matching
- Use keyword dictionaries for intent classification
- Fallback to clarification when confidence is low

---

## Decision 2: HTTP Client Library

**What was chosen**: `httpx` with async support

**Why chosen**:
- Modern Python HTTP client with async/await support
- Excellent error handling and timeout management
- Type hints and IDE support
- Compatible with existing async FastAPI backend patterns
- Better performance than `requests` for async operations
- Clear exception hierarchy for error handling

**Alternatives considered**:
- **requests**: Synchronous, simpler. Rejected due to lack of async support
- **aiohttp**: Async but lower-level. Rejected due to more verbose API
- **urllib3**: Too low-level. Rejected in favor of higher-level client

**Configuration**:
- Base timeout: 10 seconds
- Retry policy: 2 retries with exponential backoff for network errors
- Connection pooling enabled
- JSON response parsing automatic

---

## Decision 3: Tool Definition Pattern

**What was chosen**: Pydantic-based tool schemas with explicit validation

**Why chosen**:
- Consistent with existing backend schema patterns
- Automatic validation and error messages
- Type safety and IDE support
- Self-documenting schemas
- Easy to serialize/deserialize

**Alternatives considered**:
- **Dataclasses**: Less validation, more verbose. Rejected
- **TypedDict**: Runtime validation limited. Rejected
- **Plain dicts**: No validation, error-prone. Rejected

**Tool schema structure**:
```python
class ToolCall(BaseModel):
    tool_name: str
    parameters: dict
    call_id: str  # For tracing

class ToolResult(BaseModel):
    success: bool
    data: Any | None
    error: str | None
    tool_name: str
```

---

## Decision 4: Intent Recognition Rules

**What was chosen**: Keyword + pattern-based intent classification

**Intent patterns defined**:

| Intent | Keywords | Example Patterns |
|--------|----------|------------------|
| CREATE | add, create, make, new, set up | "Add a task to...", "Create new task...", "I need to..." |
| READ | show, list, get, view, what are | "Show my tasks", "What do I have...", "List all tasks" |
| UPDATE | mark, complete, finish, done, update | "Mark task 3 complete", "I finished task...", "Update task..." |
| DELETE | delete, remove, drop, cancel | "Delete task 2", "Remove the...", "Cancel task..." |

**Parameter extraction**:
- Task IDs: Extracted via regex `\b(task\s+)?(\d+)\b`
- Titles: Extracted as remainder after intent keywords
- Status: Mapped from keywords (complete→COMPLETED, pending→PENDING)
- Dates: Basic relative date parsing (tomorrow, next week, Friday)

**Ambiguity handling**:
- Multiple matching intents → Request clarification
- Missing required parameters → Request clarification
- Invalid task IDs → Inform user and suggest alternatives

---

## Decision 5: Error Handling Strategy

**What was chosen**: Structured error taxonomy with user-friendly messages

**Error categories**:

1. **IntentRecognitionError**: Unable to determine user intent
   - User message: "I'm not sure what you're asking. Could you rephrase? You can ask me to create, show, update, or delete tasks."

2. **MissingParameterError**: Required information missing
   - User message: "I need a bit more information. What would you like to name this task?"

3. **InvalidTaskIdError**: Referenced task doesn't exist
   - User message: "I couldn't find task #{task_id}. Would you like to see your current tasks?"

4. **BackendAPIError**: Backend service unavailable or returned error
   - User message: "I'm having trouble connecting to the task service. Please try again in a moment."

5. **AmbiguousReferenceError**: Multiple tasks match user reference
   - User message: "I found multiple tasks matching that description. Could you specify which one by task ID?"

**Error flow**:
1. Catch exception at executor level
2. Map to error category
3. Generate user-friendly message
4. Log technical details for debugging
5. Return to user with clarification option

---

## Decision 6: Response Generation Pattern

**What was chosen**: Template-based response generation with context awareness

**Response templates**:

| Operation | Success Template |
|-----------|-----------------|
| CREATE | "✅ Task #{id} created: {title}" |
| READ (single) | "📋 Task #{id}: {title}\nStatus: {status}\nDescription: {description}" |
| READ (multiple) | "📋 You have {count} tasks:\n\n{formatted_list}" |
| UPDATE | "✅ Task #{id} updated. Status is now {status}" |
| DELETE | "✅ Task #{id} deleted: {title}" |

**Response principles**:
- Confirm successful operations with task ID and title
- Use emojis for visual scanning (✅, 📋, ❌)
- Keep responses concise but informative
- Include next-step suggestions when helpful

---

## Decision 7: Agent Architecture Pattern

**What was chosen**: Modular pipeline architecture

**Architecture flow**:
```
User Input
    ↓
Intent Parser (intent.py)
    ↓
Tool Selector (tools.py)
    ↓
Executor (executor.py)
    ↓
Backend API Call
    ↓
Response Generator (response.py)
    ↓
User Output
```

**Module responsibilities**:
- **intent.py**: Parse natural language, extract intent and parameters
- **tools.py**: Define tool schemas, validate parameters, format API requests
- **executor.py**: Orchestrate tool selection and execution, handle errors
- **response.py**: Generate human-readable responses from backend results

**Benefits**:
- Clear separation of concerns (Constitution Principle IX)
- Each module independently testable
- Easy to extend with new intents/tools
- Debugging and logging at each stage

---

## Decision 8: Testing Strategy

**What was chosen**: Three-tier testing approach

**Test levels**:

1. **Unit Tests** (test_intent.py, test_tools.py):
   - Intent recognition accuracy
   - Parameter extraction correctness
   - Tool validation behavior
   - Response formatting

2. **Integration Tests** (test_executor.py):
   - Full instruction → tool → API → response flow
   - Error handling end-to-end
   - Backend connectivity

3. **Acceptance Tests** (manual + automated):
   - User story scenarios from spec
   - Edge case handling
   - Multi-step workflows

**Test data**:
- Fixture tasks for testing
- Mock backend responses for unit tests
- Real backend for integration tests

---

## Summary of Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| NLP Approach | Hybrid rule-based + patterns | Deterministic, maintainable, sufficient for domain |
| HTTP Client | httpx (async) | Modern, async support, excellent error handling |
| Tool Definitions | Pydantic schemas | Consistent with backend, automatic validation |
| Intent Recognition | Keyword + pattern matching | Clear, testable, debuggable |
| Error Handling | Structured taxonomy | User-friendly, traceable |
| Response Generation | Template-based | Consistent, concise, extensible |
| Architecture | Modular pipeline | Separation of concerns, testable |
| Testing | Three-tier approach | Comprehensive coverage |

---

## Next Steps

All technical unknowns resolved. Proceed to Phase 1:
1. Create data-model.md (existing model documentation)
2. Create contracts/agent-tools.yaml (tool definitions)
3. Create quickstart.md (setup instructions)
4. Update agent context with new technology
