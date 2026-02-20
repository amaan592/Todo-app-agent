# Tasks: Todo Application

**Input**: Design documents from `/specs/001-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan with backend/ and frontend/ directories
- [X] T002 [P] Initialize backend project with FastAPI dependencies in backend/
- [X] T003 [P] Initialize frontend project with React dependencies in frontend/
- [X] T004 [P] Configure linting and formatting tools for both backend and frontend

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Setup database schema and migrations framework in backend/src/database/
- [X] T006 [P] Implement CORS middleware in backend/src/main.py
- [X] T007 [P] Setup API routing and middleware structure in backend/src/api/
- [X] T008 Create base Task model in backend/src/models/task.py
- [X] T009 Configure error handling and logging infrastructure in backend/src/utils/
- [X] T010 [P] Setup environment configuration management in backend/.env
- [X] T011 Create API service layer in frontend/src/services/api.js
- [X] T012 Setup frontend routing structure in frontend/src/App.js

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and Manage Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to create new tasks, view all tasks, update task status from pending to completed, and delete tasks through the frontend communicating with the backend via REST APIs

**Independent Test**: Can be fully tested by creating a task via the frontend, verifying it appears in the task list, updating its status, and deleting it. The system should demonstrate complete CRUD functionality for tasks.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T013 [P] [US1] Contract test for POST /tasks endpoint in backend/tests/contract/test_tasks_create.py
- [ ] T014 [P] [US1] Contract test for GET /tasks endpoint in backend/tests/contract/test_tasks_read.py
- [ ] T015 [P] [US1] Contract test for PUT /tasks/{id} endpoint in backend/tests/contract/test_tasks_update.py
- [ ] T016 [P] [US1] Contract test for DELETE /tasks/{id} endpoint in backend/tests/contract/test_tasks_delete.py

### Implementation for User Story 1

- [X] T017 [P] [US1] Create TaskRequest DTOs in backend/src/schemas/task.py
- [X] T018 [P] [US1] Create TaskResponse DTO in backend/src/schemas/task.py
- [X] T019 [US1] Implement Task CRUD service in backend/src/services/task_service.py
- [X] T020 [US1] Implement POST /tasks endpoint in backend/src/api/tasks.py
- [X] T021 [US1] Implement GET /tasks endpoint in backend/src/api/tasks.py
- [X] T022 [US1] Implement PUT /tasks/{id} endpoint in backend/src/api/tasks.py
- [X] T023 [US1] Implement DELETE /tasks/{id} endpoint in backend/src/api/tasks.py
- [X] T024 [P] [US1] Create Task API service functions in frontend/src/services/taskApi.js
- [X] T025 [US1] Create TaskForm component in frontend/src/components/TaskForm.js
- [X] T026 [US1] Create TaskList component in frontend/src/components/TaskList.js
- [X] T027 [US1] Create TaskItem component in frontend/src/components/TaskItem.js
- [X] T028 [US1] Connect TaskForm to API service in frontend/src/components/TaskForm.js
- [X] T029 [US1] Connect TaskList to API service in frontend/src/components/TaskList.js
- [X] T030 [US1] Add validation and error handling for task creation
- [X] T031 [US1] Add loading states for API calls
- [X] T032 [US1] Add success and error notifications

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Task Details and Status (Priority: P2)

**Goal**: Enable users to see all tasks with their current status (Pending/Completed) and details with clear visual indicators for task states

**Independent Test**: Can be tested by creating multiple tasks, marking some as completed, and verifying that the frontend correctly displays the status of each task visually.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T033 [P] [US2] Integration test for task status display in frontend/tests/integration/test_task_display.js

### Implementation for User Story 2

- [X] T034 [P] [US2] Update TaskItem component to show visual indicators for PENDING/COMPLETED status in frontend/src/components/TaskItem.js
- [X] T035 [US2] Add CSS styling for different task statuses in frontend/src/components/TaskItem.css
- [X] T036 [US2] Display task descriptions in TaskItem component in frontend/src/components/TaskItem.js
- [X] T037 [US2] Add filtering functionality by status in TaskList component in frontend/src/components/TaskList.js
- [X] T038 [US2] Update TaskList UI to clearly distinguish between pending and completed tasks

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Delete Tasks (Priority: P3)

**Goal**: Enable users to remove tasks they no longer need with confirmation that deletion is persisted in the backend

**Independent Test**: Can be tested by creating tasks, deleting them, and verifying they no longer appear in the task list.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T039 [P] [US3] Integration test for task deletion in frontend/tests/integration/test_task_deletion.js

### Implementation for User Story 3

- [X] T040 [P] [US3] Add delete confirmation modal component in frontend/src/components/DeleteConfirmationModal.js
- [X] T041 [US3] Connect delete functionality to TaskItem component in frontend/src/components/TaskItem.js
- [X] T042 [US3] Handle optimistic UI updates for task deletion in frontend/src/components/TaskList.js
- [X] T043 [US3] Add undo functionality for task deletion in frontend/src/components/TaskList.js

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T044 [P] Documentation updates in README.md
- [X] T045 [P] Environment configuration documentation in docs/configuration.md
- [X] T046 Error boundary implementation in frontend/src/components/ErrorBoundary.js
- [ ] T047 Input validation improvements across all forms
- [ ] T048 [P] Performance optimizations for task list rendering
- [X] T049 Accessibility improvements for all components
- [ ] T050 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for POST /tasks endpoint in backend/tests/contract/test_tasks_create.py"
Task: "Contract test for GET /tasks endpoint in backend/tests/contract/test_tasks_read.py"

# Launch all models for User Story 1 together:
Task: "Create TaskRequest DTOs in backend/src/schemas/task.py"
Task: "Create TaskResponse DTO in backend/src/schemas/task.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence