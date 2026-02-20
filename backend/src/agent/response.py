"""Response generation for AI Agent.

Translates backend responses into clear, human-readable output.
"""

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class ResponseGenerator:
    """Generates human-readable responses from tool results.
    
    Uses templates for consistent response formatting.
    """
    
    # Response templates
    TEMPLATES = {
        "create_success": "✅ Task #{id} created: {title}",
        "read_single": "📋 Task #{id}: {title}\nStatus: {status}\nDescription: {description}",
        "read_multiple": "📋 You have {count} task{plural}:\n\n{tasks}",
        "update_success": "✅ Task #{id} updated. Status is now {status}",
        "delete_success": "✅ Task #{id} deleted: {title}",
        "error_generic": "❌ {message}",
    }
    
    def generate_response(self, intent: str, result: Any, error: Optional[str] = None) -> str:
        """Generate a human-readable response from tool execution result.
        
        Args:
            intent: The intent type (create, read, update, delete)
            result: Tool result data
            error: Optional error message
            
        Returns:
            Formatted response string
        """
        if error:
            logger.info(f"Generating error response: {error}")
            return self.TEMPLATES["error_generic"].format(message=error)
        
        if result is None:
            return self.TEMPLATES["error_generic"].format(message="No data returned")
        
        if intent == "create":
            return self._format_create_response(result)
        elif intent == "read":
            return self._format_read_response(result)
        elif intent == "update":
            return self._format_update_response(result)
        elif intent == "delete":
            return self._format_delete_response(result)
        else:
            logger.warning(f"Unknown intent type: {intent}")
            return str(result)
    
    def _format_create_response(self, result: dict[str, Any]) -> str:
        """Format response for task creation."""
        task_id = result.get("id", "?")
        title = result.get("title", "Untitled")
        
        logger.debug(f"Formatting create response for task #{task_id}")
        
        return self.TEMPLATES["create_success"].format(
            id=task_id,
            title=title,
        )
    
    def _format_read_response(self, result: Any) -> str:
        """Format response for task retrieval."""
        if not isinstance(result, list):
            result = [result]
        
        if len(result) == 0:
            return "📋 You have no tasks."
        elif len(result) == 1:
            # Single task - show details
            task = result[0]
            return self.TEMPLATES["read_single"].format(
                id=task.get("id", "?"),
                title=task.get("title", "Untitled"),
                status=task.get("status", "UNKNOWN"),
                description=task.get("description") or "No description",
            )
        else:
            # Multiple tasks - show summary list
            task_lines = []
            for task in result:
                status_icon = "✓" if task.get("status") == "COMPLETED" else "○"
                task_lines.append(
                    f"  {status_icon} #{task.get('id')}: {task.get('title')} "
                    f"({task.get('status', 'UNKNOWN')})"
                )
            
            tasks_text = "\n".join(task_lines)
            plural = "s" if len(result) != 1 else ""
            
            logger.debug(f"Formatting read response for {len(result)} tasks")
            
            return self.TEMPLATES["read_multiple"].format(
                count=len(result),
                plural=plural,
                tasks=tasks_text,
            )
    
    def _format_update_response(self, result: dict[str, Any]) -> str:
        """Format response for task update."""
        task_id = result.get("id", "?")
        status = result.get("status", "UNKNOWN")
        
        logger.debug(f"Formatting update response for task #{task_id}")
        
        return self.TEMPLATES["update_success"].format(
            id=task_id,
            status=status,
        )
    
    def _format_delete_response(self, result: dict[str, Any]) -> str:
        """Format response for task deletion."""
        task_id = result.get("id", "?")
        title = result.get("title", "Task")
        
        logger.debug(f"Formatting delete response for task #{task_id}")
        
        return self.TEMPLATES["delete_success"].format(
            id=task_id,
            title=title,
        )
    
    def format_clarification_request(
        self,
        message: str,
        options: Optional[list[str]] = None,
    ) -> str:
        """Format a clarification request to the user.
        
        Args:
            message: Clarification message
            options: Optional list of suggested options
            
        Returns:
            Formatted clarification request
        """
        if options:
            options_text = "\n".join(f"  {i+1}. {opt}" for i, opt in enumerate(options))
            return f"❓ {message}\n\nPlease choose:\n{options_text}"
        return f"❓ {message}"
