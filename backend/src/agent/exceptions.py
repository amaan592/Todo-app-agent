"""Exception classes for AI Agent operations.

Provides structured exception handling with user-friendly error messages.
"""

from typing import Optional


class AgentError(Exception):
    """Base exception for all agent-related errors."""
    
    def __init__(self, message: str, user_message: Optional[str] = None):
        self.message = message
        self.user_message = user_message or message
        super().__init__(self.message)


class IntentRecognitionError(AgentError):
    """Raised when the agent cannot determine user intent from the instruction.
    
    User-friendly message suggests rephrasing and lists supported actions.
    """
    
    def __init__(self, message: str = "Unable to recognize intent"):
        user_message = (
            "I'm not sure what you're asking. Could you rephrase? "
            "You can ask me to create, show, update, or delete tasks."
        )
        super().__init__(message, user_message)


class MissingParameterError(AgentError):
    """Raised when required parameters are missing from the instruction.
    
    User-friendly message requests the specific missing information.
    """
    
    def __init__(self, message: str, parameter_name: str):
        self.parameter_name = parameter_name
        user_message = f"I need a bit more information. What would you like to {parameter_name}?"
        super().__init__(message, user_message)


class InvalidTaskIdError(AgentError):
    """Raised when a referenced task ID doesn't exist.
    
    User-friendly message explains the issue and suggests viewing tasks.
    """
    
    def __init__(self, task_id: int):
        self.task_id = task_id
        message = f"Task with ID {task_id} not found"
        user_message = (
            f"I couldn't find task #{task_id}. "
            f"Would you like to see your current tasks?"
        )
        super().__init__(message, user_message)


class BackendAPIError(AgentError):
    """Raised when the backend API returns an error or is unavailable.
    
    User-friendly message explains the technical issue without exposing details.
    """
    
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.status_code = status_code
        user_message = (
            "I'm having trouble connecting to the task service. "
            "Please try again in a moment."
        )
        super().__init__(message, user_message)


class AmbiguousReferenceError(AgentError):
    """Raised when user instruction matches multiple tasks.
    
    User-friendly message asks for clarification with task IDs.
    """
    
    def __init__(self, message: str, matching_tasks: list[dict]):
        self.matching_tasks = matching_tasks
        user_message = (
            f"I found multiple tasks matching that description:\n"
            f"{self._format_tasks(matching_tasks)}\n"
            f"Could you specify which one by task ID?"
        )
        super().__init__(message, user_message)
    
    def _format_tasks(self, tasks: list[dict]) -> str:
        """Format matching tasks for display."""
        lines = []
        for task in tasks:
            lines.append(f"  #{task['id']}: {task['title']}")
        return "\n".join(lines)
