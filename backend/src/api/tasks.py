from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.task import Task
from ..schemas.task import TaskCreateRequest, TaskResponse, TaskUpdateRequest
from ..services.task_service import TaskService

router = APIRouter()


# NOTE: Route order matters! More specific routes must come AFTER general routes


@router.get("/tasks", response_model=List[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    """Get all tasks."""
    task_service = TaskService(db)
    tasks = task_service.get_all_tasks()
    return tasks


@router.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task_data: TaskCreateRequest, db: Session = Depends(get_db)):
    """Create a new task."""
    try:
        task_service = TaskService(db)
        task = task_service.create_task(task_data)
        return task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# NOTE: These specific routes must come AFTER general routes


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get a specific task by ID."""
    task_service = TaskService(db)
    task = task_service.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskUpdateRequest, db: Session = Depends(get_db)):
    """Update a specific task by ID."""
    task_service = TaskService(db)
    task = task_service.update_task(task_id, task_data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a specific task by ID."""
    task_service = TaskService(db)
    success = task_service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    # Return nothing for 204 No Content