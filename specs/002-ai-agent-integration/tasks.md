# Tasks: AI Agent Integration

**Input**: Design documents from `/specs/002-ai-agent-integration/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are INCLUDED for this feature as required by Constitution Principle X (Testing Requirement) and spec.md FR-027 to FR-030.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `backend/src/`, `backend/tests/` (agent module added to existing backend)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create agent module directory structure in backend/src/agent/
- [X] T002 Add httpx dependency to backend/requirements.txt for async HTTP client
- [X] T003 [P] Create agent/__init__.py to initialize agent module
- [X] T004 [P] Create test directories backend/tests/agent/ and backend/tests/integration/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 [P] Create ToolResult and ToolCall Pydantic schemas in backend/src/agent/schemas.py
- [X] T006 [P] Create HTTP client wrapper with error handling in backend/src/agent/http_client.py
- [X] T007 Configure backend API base URL and timeout settings in backend/src/agent/config.py
- [X] T008 [P] Implement base exception classes for agent errors in backend/src/agent/exceptions.py
- [X] T009 Setup logging configuration for agent operations in backend/src/agent/logging_config.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create Tasks via Natural Language (Priority: P1) 🎯 MVP

**Goal**: Enable users to create tasks by telling the AI Agent what to do in natural language

**Independent Test**: User says "Add a task to buy groceries tomorrow" and the system creates a task with title "Buy groceries", returning confirmation.

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T010 [P] [US1] Unit test for create_task tool success path in backend/tests/agent/test_tools.py
- [X] T011 [P] [US1] Unit test for intent recognition of create instructions in backend/tests/agent/test_intent.py
- [ ] T012 [US1] Integration test for end-to-end task creation flow in backend/tests/integration/test_agent_create.py

### Implementation for User Story 1

- [X] T013 [P] [US1] Implement create_task tool function in backend/src/agent/tools.py
- [X] T014 [P] [US1] Implement intent patterns for CREATE in backend/src/agent/intent.py
- [X] T015 [P] [US1] Implement parameter extraction for task title/description in backend/src/agent/intent.py
- [X] T016 [US1] Implement response template for task creation success in backend/src/agent/response.py
- [X] T017 [US1] Add error handling for missing title in intent parser in backend/src/agent/intent.py
- [X] T018 [US1] Add logging for task creation operations in backend/src/agent/tools.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Retrieve Tasks via Natural Language (Priority: P2)

**Goal**: Enable users to query and view their tasks using natural language with optional filtering

**Independent Test**: User says "Show me all my pending tasks" and the system returns a formatted list of only PENDING status tasks.

### Tests for User Story 2

- [ ] T019 [P] [US2] Unit test for get_tasks tool with and without status filter in backend/tests/agent/test_tools.py
- [ ] T020 [P] [US2] Unit test for intent recognition of READ instructions in backend/tests/agent/test_intent.py
- [ ] T021 [US2] Integration test for end-to-end task retrieval flow in backend/tests/integration/test_agent_retrieve.py

### Implementation for User Story 2

- [X] T022 [P] [US2] Implement get_tasks tool function with optional status filter in backend/src/agent/tools.py
- [X] T023 [P] [US2] Implement intent patterns for READ instructions in backend/src/agent/intent.py
- [X] T024 [P] [US2] Implement parameter extraction for status filter keywords in backend/src/agent/intent.py
- [X] T025 [US2] Implement response template for single task display in backend/src/agent/response.py
- [X] T026 [US2] Implement response template for multiple task list formatting in backend/src/agent/response.py
- [X] T027 [US2] Add logging for task retrieval operations in backend/src/agent/tools.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Task Status via Natural Language (Priority: P3)

**Goal**: Enable users to mark tasks as complete or pending using natural language instructions

**Independent Test**: User says "Mark task 3 as done" and the system updates the task status to COMPLETED and confirms the change.

### Tests for User Story 3

- [ ] T028 [P] [US3] Unit test for update_task tool with status change in backend/tests/agent/test_tools.py
- [ ] T029 [P] [US3] Unit test for intent recognition of UPDATE instructions in backend/tests/agent/test_intent.py
- [ ] T030 [US3] Integration test for end-to-end task status update flow in backend/tests/integration/test_agent_update.py

### Implementation for User Story 3

- [X] T031 [P] [US3] Implement update_task tool function in backend/src/agent/tools.py
- [X] T032 [P] [US3] Implement intent patterns for UPDATE instructions (mark complete, finish, done) in backend/src/agent/intent.py
- [X] T033 [P] [US3] Implement task ID extraction from natural language in backend/src/agent/intent.py
- [X] T034 [US3] Implement response template for task update confirmation in backend/src/agent/response.py
- [X] T035 [US3] Add error handling for non-existent task IDs in backend/src/agent/tools.py
- [X] T036 [US3] Add clarification logic for ambiguous task references in backend/src/agent/intent.py
- [X] T037 [US3] Add logging for task update operations in backend/src/agent/tools.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Delete Tasks via Natural Language (Priority: P4)

**Goal**: Enable users to remove tasks using natural language with appropriate safety measures

**Independent Test**: User says "Delete task 2" and the system removes the task and returns success message.

### Tests for User Story 4

- [ ] T038 [P] [US4] Unit test for delete_task tool success path in backend/tests/agent/test_tools.py
- [ ] T039 [P] [US4] Unit test for intent recognition of DELETE instructions in backend/tests/agent/test_intent.py
- [ ] T040 [US4] Integration test for end-to-end task deletion flow in backend/tests/integration/test_agent_delete.py

### Implementation for User Story 4

- [X] T041 [P] [US4] Implement delete_task tool function in backend/src/agent/tools.py
- [X] T042 [P] [US4] Implement intent patterns for DELETE instructions (delete, remove, cancel) in backend/src/agent/intent.py
- [X] T043 [US4] Implement response template for task deletion confirmation in backend/src/agent/response.py
- [X] T044 [US4] Add error handling for non-existent task IDs in delete operation in backend/src/agent/tools.py
- [X] T045 [US4] Add logging for task deletion operations in backend/src/agent/tools.py

**Checkpoint**: All four user stories should now be independently functional

---

## Phase 7: Agent Execution Engine

**Purpose**: Orchestrate intent recognition, tool selection, and execution flow

- [X] T046 [P] Implement AgentExecutor class with execute() method in backend/src/agent/executor.py
- [X] T047 [P] Implement tool selection logic based on detected intent in backend/src/agent/executor.py
- [X] T048 Implement tool invocation and response processing in backend/src/agent/executor.py
- [X] T049 Implement error handling wrapper for tool execution in backend/src/agent/executor.py
- [X] T050 [P] Implement CLI interface for interactive agent testing in backend/src/agent/cli.py
- [X] T051 [P] Add comprehensive logging throughout executor flow in backend/src/agent/executor.py

---

## Phase 8: Safety & Error Handling

**Purpose**: Handle all error scenarios with user-friendly messages and clarification requests

- [ ] T052 Implement IntentRecognitionError with user-friendly message in backend/src/agent/exceptions.py
- [ ] T053 Implement MissingParameterError with clarification request in backend/src/agent/exceptions.py
- [ ] T054 Implement InvalidTaskIdError with suggestion to view tasks in backend/src/agent/exceptions.py
- [ ] T055 Implement BackendAPIError with appropriate user message in backend/src/agent/exceptions.py
- [ ] T056 Implement AmbiguousReferenceError with disambiguation options in backend/src/agent/exceptions.py
- [ ] T057 Add error handling tests for all exception types in backend/tests/agent/test_exceptions.py

---

## Phase 9: Observability & Verification

**Purpose**: Log agent decisions, tool invocations, and backend responses for traceability

- [ ] T058 [P] Add structured logging for all tool invocations with parameters in backend/src/agent/tools.py
- [ ] T059 [P] Add structured logging for intent recognition results in backend/src/agent/intent.py
- [ ] T060 [P] Add structured logging for executor decision flow in backend/src/agent/executor.py
- [ ] T061 Implement execution trace ID for request tracking across modules in backend/src/agent/executor.py
- [ ] T062 [P] Add backend response logging in backend/src/agent/tools.py

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T063 [P] Update quickstart.md with actual implementation examples
- [ ] T064 [P] Add docstrings to all public functions in agent module
- [ ] T065 [P] Run ruff check on agent module for code quality in backend/src/agent/
- [ ] T066 [P] Run pytest on all agent tests to verify coverage in backend/tests/
- [ ] T067 Performance optimization for intent pattern matching in backend/src/agent/intent.py
- [ ] T068 [P] Update QWEN.md with agent architecture documentation
- [ ] T069 [P] Validate implementation against spec.md success criteria
- [ ] T070 [P] Run end-to-end manual testing per quickstart.md scenarios

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - **BLOCKS all user stories**
- **User Stories (Phases 3-6)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Execution Engine (Phase 7)**: Depends on all user story tool implementations
- **Safety & Error Handling (Phase 8)**: Depends on execution engine
- **Observability (Phase 9)**: Can run in parallel with Phase 7-8
- **Polish (Phase 10)**: Depends on all previous phases

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of US1
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independent of US1/US2
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Independent of US1/US2/US3

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Tool implementations can run in parallel within each story [P]
- Intent patterns can run in parallel with tools [P]
- Response templates depend on tool implementations
- Story complete before moving to next priority

### Parallel Opportunities

**Setup Phase**:
- T003, T004 can run in parallel (different files)

**Foundational Phase**:
- T005, T006, T008 can run in parallel (different files)

**User Story 1**:
- T010, T011, T013, T014, T015 can run in parallel (different files)

**User Story 2**:
- T019, T020, T022, T023, T024 can run in parallel (different files)

**User Story 3**:
- T028, T029, T031, T032, T033 can run in parallel (different files)

**User Story 4**:
- T038, T039, T041, T042 can run in parallel (different files)

**Execution Engine**:
- T046, T047, T050 can run in parallel (different files)

**Observability**:
- T058, T059, T060, T062 can run in parallel (different files)

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Unit test for create_task tool in backend/tests/agent/test_tools.py"
Task: "Unit test for intent recognition in backend/tests/agent/test_intent.py"
Task: "Integration test in backend/tests/integration/test_agent_create.py"

# Launch all tool/intent implementations for User Story 1 together:
Task: "Implement create_task tool in backend/src/agent/tools.py"
Task: "Implement CREATE intent patterns in backend/src/agent/intent.py"
Task: "Implement parameter extraction in backend/src/agent/intent.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T009)
3. Complete Phase 3: User Story 1 (T010-T018)
4. **STOP and VALIDATE**: Test "Add a task to buy groceries" → task created
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Create) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (Retrieve) → Test independently → Deploy/Demo
4. Add User Story 3 (Update) → Test independently → Deploy/Demo
5. Add User Story 4 (Delete) → Test independently → Deploy/Demo
6. Complete Execution Engine, Error Handling, Observability
7. Polish and documentation

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Create)
   - Developer B: User Story 2 (Retrieve)
   - Developer C: User Story 3 (Update) + User Story 4 (Delete)
3. Stories complete and integrate independently
4. Team collaborates on Execution Engine (Phase 7)

---

## Task Summary

| Phase | Description | Task Count |
|-------|-------------|------------|
| Phase 1 | Setup | 4 tasks |
| Phase 2 | Foundational | 5 tasks |
| Phase 3 | User Story 1 (Create) | 9 tasks (3 tests + 6 implementation) |
| Phase 4 | User Story 2 (Retrieve) | 9 tasks (3 tests + 6 implementation) |
| Phase 5 | User Story 3 (Update) | 10 tasks (3 tests + 7 implementation) |
| Phase 6 | User Story 4 (Delete) | 8 tasks (3 tests + 5 implementation) |
| Phase 7 | Execution Engine | 6 tasks |
| Phase 8 | Safety & Error Handling | 6 tasks |
| Phase 9 | Observability | 5 tasks |
| Phase 10 | Polish | 8 tasks |
| **Total** | **All phases** | **70 tasks** |

**MVP Scope** (User Story 1 only): Phases 1-3 = 18 tasks

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
