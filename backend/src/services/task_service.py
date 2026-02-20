from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from ..models.task import Task, TaskStatus
from ..schemas.task import TaskCreateRequest, TaskUpdateRequest


class TaskService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_task(self, task_data: TaskCreateRequest) -> Task:
        """Create a new task in the database."""
        db_task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status or TaskStatus.PENDING
        )

        try:
            self.db.add(db_task)
            self.db.commit()
            self.db.refresh(db_task)
            return db_task
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Task could not be created due to integrity constraint")

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by its ID."""
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from the database."""
        return self.db.query(Task).all()

    def update_task(self, task_id: int, task_data: TaskUpdateRequest) -> Optional[Task]:
        """Update an existing task."""
        db_task = self.get_task_by_id(task_id)
        if not db_task:
            return None

        # Update fields that are provided in the request
        update_data = task_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)

        try:
            self.db.commit()
            self.db.refresh(db_task)
            return db_task
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Task could not be updated due to integrity constraint")

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID."""
        db_task = self.get_task_by_id(task_id)
        if not db_task:
            return False

        try:
            self.db.delete(db_task)
            self.db.commit()
            return True
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Task could not be deleted due to integrity constraint")