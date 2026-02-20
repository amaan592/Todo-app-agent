"""Tool implementations for AI Agent backend operations.

Exposes backend Todo API as structured callable tools:
- create_task: Create a new task
- get_tasks: Retrieve tasks (with optional filter)
- update_task: Update an existing task
- delete_task: Delete a task
"""

import logging
from typing import Optional

from .schemas import ToolResult
from .http_client import AgentHTTPClient
from .exceptions import InvalidTaskIdError

logger = logging.getLogger(__name__)


class TaskTools:
    """Tool implementations for task management operations.
    
    Each tool handles HTTP communication, error handling, and response formatting.
    """
    
    def __init__(self):
        """Initialize task tools with HTTP client."""
        self.http_client = AgentHTTPClient()
    
    async def close(self):
        """Close the HTTP client connection."""
        await self.http_client.close()
    
    async def create_task(
        self,
        title: str,
        description: Optional[str] = None,
    ) -> ToolResult:
        """Create a new task via backend API.
        
        Args:
            title: Task title (required, max 200 chars)
            description: Optional task description (max 1000 chars)
            
        Returns:
            ToolResult with created task data or error
            
        Raises:
            MissingParameterError: If title is missing or empty
        """
        if not title or not title.strip():
            from .exceptions import MissingParameterError
            raise MissingParameterError("Title is required", "name this task")
        
        try:
            logger.info(f"Creating task: {title[:50]}...")
            
            # Build request payload
            payload = {"title": title.strip()}
            if description:
                payload["description"] = description
            
            # Call backend API
            response = await self.http_client.post("/api/v1/tasks", json_data=payload)
            
            logger.info(f"Task created successfully with ID: {response.get('id')}")
            
            return ToolResult(
                success=True,
                data=response,
                error=None,
                tool_name="create_task",
            )
            
        except InvalidTaskIdError:
            raise
        except Exception as e:
            logger.error(f"Failed to create task: {str(e)}")
            from .exceptions import BackendAPIError
            if isinstance(e, BackendAPIError):
                raise
            raise BackendAPIError(f"Failed to create task: {str(e)}")
    
    async def get_tasks(
        self,
        status: Optional[str] = None,
    ) -> ToolResult:
        """Retrieve tasks from backend API.
        
        Args:
            status: Optional status filter ('PENDING' or 'COMPLETED')
            
        Returns:
            ToolResult with list of tasks or error
        """
        try:
            logger.info(f"Retrieving tasks, status filter: {status}")
            
            # Build query parameters
            params = {}
            if status:
                params["status"] = status
            
            # Call backend API
            response = await self.http_client.get("/api/v1/tasks", params=params)
            
            # Ensure response is a list
            tasks = response if isinstance(response, list) else []
            
            logger.info(f"Retrieved {len(tasks)} tasks")
            
            return ToolResult(
                success=True,
                data=tasks,
                error=None,
                tool_name="get_tasks",
            )
            
        except Exception as e:
            logger.error(f"Failed to retrieve tasks: {str(e)}")
            from .exceptions import BackendAPIError
            if isinstance(e, BackendAPIError):
                raise
            raise BackendAPIError(f"Failed to retrieve tasks: {str(e)}")
    
    async def update_task(
        self,
        task_id: int,
        fields: dict,
    ) -> ToolResult:
        """Update an existing task via backend API.
        
        Args:
            task_id: ID of the task to update
            fields: Dictionary of fields to update (title, description, status)
            
        Returns:
            ToolResult with updated task data or error
            
        Raises:
            InvalidTaskIdError: If task doesn't exist
        """
        try:
            logger.info(f"Updating task {task_id} with fields: {fields}")
            
            # Validate fields - only allow specific fields
            allowed_fields = {"title", "description", "status"}
            filtered_fields = {k: v for k, v in fields.items() if k in allowed_fields}
            
            if not filtered_fields:
                from .exceptions import MissingParameterError
                raise MissingParameterError("No valid fields to update", "update")
            
            # Call backend API
            response = await self.http_client.put(
                f"/api/v1/tasks/{task_id}",
                json_data=filtered_fields,
            )
            
            logger.info(f"Task {task_id} updated successfully")
            
            return ToolResult(
                success=True,
                data=response,
                error=None,
                tool_name="update_task",
            )
            
        except Exception as e:
            logger.error(f"Failed to update task {task_id}: {str(e)}")
            from .exceptions import BackendAPIError, InvalidTaskIdError
            if isinstance(e, (InvalidTaskIdError, BackendAPIError)):
                raise
            # Check for 404 (task not found)
            if hasattr(e, 'status_code') and e.status_code == 404:
                raise InvalidTaskIdError(task_id)
            raise BackendAPIError(f"Failed to update task: {str(e)}")
    
    async def delete_task(self, task_id: int) -> ToolResult:
        """Delete a task via backend API.
        
        Args:
            task_id: ID of the task to delete
            
        Returns:
            ToolResult with deletion confirmation or error
            
        Raises:
            InvalidTaskIdError: If task doesn't exist
        """
        try:
            logger.info(f"Deleting task {task_id}")
            
            # Call backend API
            response = await self.http_client.delete(f"/api/v1/tasks/{task_id}")
            
            logger.info(f"Task {task_id} deleted successfully")
            
            return ToolResult(
                success=True,
                data={"id": task_id, "deleted": True},
                error=None,
                tool_name="delete_task",
            )
            
        except Exception as e:
            logger.error(f"Failed to delete task {task_id}: {str(e)}")
            from .exceptions import BackendAPIError, InvalidTaskIdError
            if isinstance(e, (InvalidTaskIdError, BackendAPIError)):
                raise
            # Check for 404 (task not found)
            if hasattr(e, 'status_code') and e.status_code == 404:
                raise InvalidTaskIdError(task_id)
            raise BackendAPIError(f"Failed to delete task: {str(e)}")
