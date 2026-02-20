"""Unit tests for AI Agent intent recognition.

Tests cover pattern matching, parameter extraction, and error handling.
"""

import pytest

from src.agent.intent import IntentParser, ParsedIntent
from src.agent.exceptions import IntentRecognitionError, MissingParameterError


@pytest.fixture
def parser():
    """Create an IntentParser instance for testing."""
    return IntentParser()


class TestCreateIntent:
    """Tests for CREATE intent recognition."""
    
    def test_create_simple(self, parser):
        """Test simple create instruction."""
        # Act
        result = parser.parse("Add a task to buy groceries")
        
        # Assert
        assert result.intent == "create"
        assert result.parameters["title"] == "buy groceries"
    
    def test_create_with_need(self, parser):
        """Test create with 'I need to' pattern."""
        # Act
        result = parser.parse("I need to finish the project report")
        
        # Assert
        assert result.intent == "create"
        assert result.parameters["title"] == "finish the project report"
    
    def test_create_with_want(self, parser):
        """Test create with 'I want to' pattern."""
        # Act
        result = parser.parse("I want to call the dentist")
        
        # Assert
        assert result.intent == "create"
        assert result.parameters["title"] == "call the dentist"
    
    def test_create_direct(self, parser):
        """Test direct create pattern."""
        # Act
        result = parser.parse("Create task: Review Q1 budget")
        
        # Assert
        assert result.intent == "create"
        assert result.parameters["title"] == "Review Q1 budget"


class TestReadIntent:
    """Tests for READ intent recognition."""
    
    def test_read_all_tasks(self, parser):
        """Test reading all tasks."""
        # Act
        result = parser.parse("Show me my tasks")
        
        # Assert
        assert result.intent == "read"
        assert result.parameters == {}
    
    def test_read_pending_tasks(self, parser):
        """Test reading pending tasks."""
        # Act
        result = parser.parse("Show me my pending tasks")
        
        # Assert
        assert result.intent == "read"
        assert result.parameters["status"] == "PENDING"
    
    def test_read_completed_tasks(self, parser):
        """Test reading completed tasks."""
        # Act
        result = parser.parse("Show completed tasks")
        
        # Assert
        assert result.intent == "read"
        assert result.parameters["status"] == "COMPLETED"
    
    def test_read_what_do_i_have(self, parser):
        """Test 'what do I have' pattern."""
        # Act
        result = parser.parse("What do I have to do?")
        
        # Assert
        assert result.intent == "read"


class TestUpdateIntent:
    """Tests for UPDATE intent recognition."""
    
    def test_update_mark_complete(self, parser):
        """Test marking task complete."""
        # Act
        result = parser.parse("Mark task 3 complete")
        
        # Assert
        assert result.intent == "update"
        assert result.parameters["task_id"] == 3
        assert result.parameters["status"] == "COMPLETED"
    
    def test_update_finished(self, parser):
        """Test 'I finished' pattern."""
        # Act
        result = parser.parse("I finished task 5")
        
        # Assert
        assert result.intent == "update"
        assert result.parameters["task_id"] == 5
    
    def test_update_mark_done(self, parser):
        """Test marking task done."""
        # Act
        result = parser.parse("Mark task 1 as done")
        
        # Assert
        assert result.intent == "update"
        assert result.parameters["task_id"] == 1
        assert result.parameters["status"] == "COMPLETED"
    
    def test_update_mark_pending(self, parser):
        """Test marking task pending."""
        # Act
        result = parser.parse("Mark task 2 as pending")
        
        # Assert
        assert result.intent == "update"
        assert result.parameters["task_id"] == 2
        assert result.parameters["status"] == "PENDING"


class TestDeleteIntent:
    """Tests for DELETE intent recognition."""
    
    def test_delete_by_id(self, parser):
        """Test deleting task by ID."""
        # Act
        result = parser.parse("Delete task 2")
        
        # Assert
        assert result.intent == "delete"
        assert result.parameters["task_id"] == 2
    
    def test_delete_remove(self, parser):
        """Test 'remove' pattern."""
        # Act
        result = parser.parse("Remove task 4")
        
        # Assert
        assert result.intent == "delete"
        assert result.parameters["task_id"] == 4
    
    def test_delete_cancel(self, parser):
        """Test 'cancel' pattern."""
        # Act
        result = parser.parse("Cancel task 1")
        
        # Assert
        assert result.intent == "delete"
        assert result.parameters["task_id"] == 1


class TestIntentRecognitionErrors:
    """Tests for error handling in intent recognition."""
    
    def test_empty_instruction(self, parser):
        """Test empty instruction raises error."""
        # Act & Assert
        with pytest.raises(MissingParameterError):
            parser.parse("")
    
    def test_whitespace_only(self, parser):
        """Test whitespace-only instruction raises error."""
        # Act & Assert
        with pytest.raises(MissingParameterError):
            parser.parse("   ")
    
    def test_unrecognized_intent(self, parser):
        """Test unrecognized intent raises error."""
        # Act & Assert
        with pytest.raises(IntentRecognitionError):
            parser.parse("Something completely unrelated")
    
    def test_gibberish(self, parser):
        """Test gibberish raises error."""
        # Act & Assert
        with pytest.raises(IntentRecognitionError):
            parser.parse("asdfghjkl qwerty")


class TestTaskIdExtraction:
    """Tests for task ID extraction utility."""
    
    def test_extract_task_id_simple(self, parser):
        """Test simple task ID extraction."""
        # Act
        result = parser.extract_task_id("Delete task 5")
        
        # Assert
        assert result == 5
    
    def test_extract_task_id_with_word(self, parser):
        """Test task ID extraction with 'task' word."""
        # Act
        result = parser.extract_task_id("Mark task 12 complete")
        
        # Assert
        assert result == 12
    
    def test_extract_task_id_bare_number(self, parser):
        """Test task ID extraction with bare number."""
        # Act
        result = parser.extract_task_id("Delete 3")
        
        # Assert
        assert result == 3
    
    def test_extract_task_id_none(self, parser):
        """Test extraction when no ID present."""
        # Act
        result = parser.extract_task_id("Show my tasks")
        
        # Assert
        assert result is None
