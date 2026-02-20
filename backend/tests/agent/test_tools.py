"""Unit tests for AI Agent tool implementations.

Tests cover success paths, error handling, and parameter validation.
"""

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch, MagicMock

from src.agent.tools import TaskTools
from src.agent.schemas import ToolResult
from src.agent.exceptions import InvalidTaskIdError, BackendAPIError, MissingParameterError


@pytest.fixture
def task_tools():
    """Create a TaskTools instance for testing."""
    return TaskTools()


@pytest.fixture
def mock_http_client():
    """Create a mock HTTP client."""
    client = AsyncMock()
    return client


class TestCreateTask:
    """Tests for create_task tool."""
    
    @pytest.mark.asyncio
    async def test_create_task_success(self, task_tools, mock_http_client):
        """Test successful task creation."""
        # Arrange
        with patch.object(task_tools, 'http_client', mock_http_client):
            mock_http_client.post.return_value = {
                "id": 1,
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "status": "PENDING",
            }
            
            # Act
            result = await task_tools.create_task(
                title="Buy groceries",
                description="Milk, eggs, bread",
            )
            
            # Assert
            assert result.success is True
            assert result.tool_name == "create_task"
            assert result.data["id"] == 1
            assert result.data["title"] == "Buy groceries"
            mock_http_client.post.assert_called_once_with(
                "/api/v1/tasks",
                json_data={"title": "Buy groceries", "description": "Milk, eggs, bread"},
            )
    
    @pytest.mark.asyncio
    async def test_create_task_minimal_params(self, task_tools, mock_http_client):
        """Test task creation with only required title."""
        # Arrange
        with patch.object(task_tools, 'http_client', mock_http_client):
            mock_http_client.post.return_value = {
                "id": 2,
                "title": "Call dentist",
                "description": None,
                "status": "PENDING",
            }
            
            # Act
            result = await task_tools.create_task(title="Call dentist")
            
            # Assert
            assert result.success is True
            assert result.data["title"] == "Call dentist"
            mock_http_client.post.assert_called_once_with(
                "/api/v1/tasks",
                json_data={"title": "Call dentist"},
            )
    
    @pytest.mark.asyncio
    async def test_create_task_empty_title(self, task_tools):
        """Test that empty title raises error."""
        # Act & Assert
        with pytest.raises(MissingParameterError):
            await task_tools.create_task(title="")
    
    @pytest.mark.asyncio
    async def test_create_task_backend_error(self, task_tools, mock_http_client):
        """Test backend API error handling."""
        # Arrange
        with patch.object(task_tools, 'http_client', mock_http_client):
            mock_http_client.post.side_effect = BackendAPIError("Backend unavailable")
            
            # Act & Assert
            with pytest.raises(BackendAPIError):
                await task_tools.create_task(title="Test task")


class TestGetTasks:
    """Tests for get_tasks tool."""
    
    @pytest.mark.asyncio
    async def test_get_tasks_all(self, task_tools, mock_http_client):
        """Test retrieving all tasks."""
        # Arrange
        with patch.object(task_tools, 'http_client', mock_http_client):
            mock_http_client.get.return_value = [
                {"id": 1, "title": "Task 1", "status": "PENDING"},
                {"id": 2, "title": "Task 2", "status": "COMPLETED"},
            ]
            
            # Act
            result = await task_tools.get_tasks()
            
            # Assert
            assert result.success is True
            assert result.tool_name == "get_tasks"
            assert len(result.data) == 2
            mock_http_client.get.assert_called_once_with("/api/v1/tasks", params={})
    
    @pytest.mark.asyncio
    async def test_get_tasks_filtered(self, task_tools, mock_http_client):
        """Test retrieving tasks with status filter."""
        # Arrange
        with patch.object(task_tools, 'http_client', mock_http_client):
            mock_http_client.get.return_value = [
                {"id": 1, "title": "Task 1", "status": "PENDING"},
            ]
            
            # Act
            result = await task_tools.get_tasks(status="PENDING")
            
            # Assert
            assert result.success is True
            assert len(result.data) == 1
            mock_http_client.get.assert_called_once_with(
                "/api/v1/tasks",
                params={"status": "PENDING"},
            )
    
    @pytest.mark.asyncio
    async def test_get_tasks_empty_list(self, task_tools, mock_http_client):
        """Test retrieving empty task list."""
        # Arrange
        with patch.object(task_tools, 'http_client', mock_http_client):
            mock_http_client.get.return_value = []
            
            # Act
            result = await task_tools.get_tasks()
            
            # Assert
            assert result.success is True
            assert result.data == []


class TestUpdateTask:
    """Tests for update_task tool."""
    
    @pytest.mark.asyncio
    async def test_update_task_success(self, task_tools, mock_http_client):
        """Test successful task update."""
        # Arrange
        with patch.object(task_tools, 'http_client', mock_http_client):
            mock_http_client.put.return_value = {
                "id": 3,
                "title": "Buy groceries",
                "status": "COMPLETED",
            }
            
            # Act
            result = await task_tools.update_task(
                task_id=3,
                fields={"status": "COMPLETED"},
            )
            
            # Assert
            assert result.success is True
            assert result.tool_name == "update_task"
            assert result.data["status"] == "COMPLETED"
            mock_http_client.put.assert_called_once_with(
                "/api/v1/tasks/3",
                json_data={"status": "COMPLETED"},
            )
    
    @pytest.mark.asyncio
    async def test_update_task_not_found(self, task_tools, mock_http_client):
        """Test updating non-existent task."""
        # Arrange
        with patch.object(task_tools, 'http_client', mock_http_client):
            mock_http_client.put.side_effect = BackendAPIError(
                "Task not found",
                status_code=404,
            )
            
            # Act & Assert
            with pytest.raises(InvalidTaskIdError):
                await task_tools.update_task(task_id=999, fields={"status": "COMPLETED"})


class TestDeleteTask:
    """Tests for delete_task tool."""
    
    @pytest.mark.asyncio
    async def test_delete_task_success(self, task_tools, mock_http_client):
        """Test successful task deletion."""
        # Arrange
        with patch.object(task_tools, 'http_client', mock_http_client):
            mock_http_client.delete.return_value = {}
            
            # Act
            result = await task_tools.delete_task(task_id=2)
            
            # Assert
            assert result.success is True
            assert result.tool_name == "delete_task"
            assert result.data["deleted"] is True
            mock_http_client.delete.assert_called_once_with("/api/v1/tasks/2")
    
    @pytest.mark.asyncio
    async def test_delete_task_not_found(self, task_tools, mock_http_client):
        """Test deleting non-existent task."""
        # Arrange
        with patch.object(task_tools, 'http_client', mock_http_client):
            mock_http_client.delete.side_effect = BackendAPIError(
                "Task not found",
                status_code=404,
            )
            
            # Act & Assert
            with pytest.raises(InvalidTaskIdError):
                await task_tools.delete_task(task_id=999)
