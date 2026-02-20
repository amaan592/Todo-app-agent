"""Agent execution engine for orchestrating intent recognition, tool selection, and execution.

Implements the core agent decision flow:
1. Interpret instruction
2. Select tool
3. Execute tool
4. Process response
5. Generate output
"""

import logging
import uuid
from typing import Optional

from .intent import IntentParser, ParsedIntent
from .tools import TaskTools
from .response import ResponseGenerator
from .schemas import ToolResult
from .exceptions import AgentError

logger = logging.getLogger(__name__)


class AgentExecutor:
    """Orchestrates natural language instruction execution.
    
    Coordinates intent parsing, tool selection, execution, and response generation.
    """
    
    def __init__(self):
        """Initialize the agent executor with all components."""
        self.intent_parser = IntentParser()
        self.task_tools = TaskTools()
        self.response_generator = ResponseGenerator()
        self._execution_id: Optional[str] = None
    
    async def execute(self, instruction: str) -> str:
        """Execute a natural language instruction.
        
        Args:
            instruction: User's natural language instruction
            
        Returns:
            Human-readable response string
            
        Raises:
            AgentError: If execution fails
        """
        # Generate unique execution ID for tracing
        self._execution_id = str(uuid.uuid4())[:8]
        logger.info(f"[{self._execution_id}] Executing instruction: {instruction}")
        
        try:
            # Step 1: Parse intent
            parsed_intent = self.intent_parser.parse(instruction)
            logger.info(f"[{self._execution_id}] Parsed intent: {parsed_intent.intent}")
            
            # Step 2: Select and execute tool
            tool_result = await self._execute_intent(parsed_intent)
            logger.info(f"[{self._execution_id}] Tool execution complete: success={tool_result.success}")
            
            # Step 3: Generate response
            if tool_result.error:
                response = self.response_generator.generate_response(
                    parsed_intent.intent,
                    None,
                    tool_result.error,
                )
            else:
                response = self.response_generator.generate_response(
                    parsed_intent.intent,
                    tool_result.data,
                    None,
                )
            
            logger.info(f"[{self._execution_id}] Response generated: {response[:100]}...")
            
            return response
            
        except AgentError as e:
            logger.error(f"[{self._execution_id}] Agent error: {e.message}")
            # Generate user-friendly error response
            return self.response_generator.generate_response(
                "error",
                None,
                e.user_message,
            )
        except Exception as e:
            logger.error(f"[{self._execution_id}] Unexpected error: {str(e)}")
            return (
                "❌ An unexpected error occurred. Please try again. "
                "If the problem persists, check the logs for details."
            )
    
    async def _execute_intent(self, intent: ParsedIntent) -> ToolResult:
        """Execute a parsed intent using the appropriate tool.
        
        Args:
            intent: Parsed intent with parameters
            
        Returns:
            ToolResult from tool execution
            
        Raises:
            AgentError: If tool execution fails
        """
        logger.debug(f"[{self._execution_id}] Executing intent: {intent.intent}")
        
        if intent.intent == "create":
            return await self._execute_create(intent.parameters)
        elif intent.intent == "read":
            return await self._execute_read(intent.parameters)
        elif intent.intent == "update":
            return await self._execute_update(intent.parameters)
        elif intent.intent == "delete":
            return await self._execute_delete(intent.parameters)
        else:
            logger.error(f"[{self._execution_id}] Unknown intent: {intent.intent}")
            from .exceptions import IntentRecognitionError
            raise IntentRecognitionError()
    
    async def _execute_create(self, parameters: dict) -> ToolResult:
        """Execute create intent.
        
        Args:
            parameters: Parsed parameters including title
            
        Returns:
            ToolResult from create_task
        """
        title = parameters.get("title", "")
        
        if not title:
            from .exceptions import MissingParameterError
            raise MissingParameterError("Title is required", "name this task")
        
        logger.info(f"[{self._execution_id}] Creating task: {title}")
        
        return await self.task_tools.create_task(title=title)
    
    async def _execute_read(self, parameters: dict) -> ToolResult:
        """Execute read intent.
        
        Args:
            parameters: Parsed parameters including optional status filter
            
        Returns:
            ToolResult from get_tasks
        """
        status = parameters.get("status")
        
        logger.info(f"[{self._execution_id}] Retrieving tasks, status filter: {status}")
        
        return await self.task_tools.get_tasks(status=status)
    
    async def _execute_update(self, parameters: dict) -> ToolResult:
        """Execute update intent.
        
        Args:
            parameters: Parsed parameters including task_id and optional status
            
        Returns:
            ToolResult from update_task
        """
        task_id = parameters.get("task_id")
        
        if not task_id:
            from .exceptions import MissingParameterError
            raise MissingParameterError("Task ID is required", "specify which task")
        
        # Determine status change
        fields = {}
        if "status" in parameters:
            fields["status"] = parameters["status"]
        else:
            # Default to marking as complete
            fields["status"] = "COMPLETED"
        
        logger.info(f"[{self._execution_id}] Updating task {task_id}")
        
        return await self.task_tools.update_task(task_id=task_id, fields=fields)
    
    async def _execute_delete(self, parameters: dict) -> ToolResult:
        """Execute delete intent.
        
        Args:
            parameters: Parsed parameters including task_id or title_query
            
        Returns:
            ToolResult from delete_task
        """
        task_id = parameters.get("task_id")
        title_query = parameters.get("title_query")
        
        if task_id:
            logger.info(f"[{self._execution_id}] Deleting task {task_id}")
            return await self.task_tools.delete_task(task_id=task_id)
        elif title_query:
            # Need to find task by title - may need clarification
            logger.info(f"[{self._execution_id}] Deleting task by title: {title_query}")
            # For now, this would require additional logic to find matching tasks
            # and request clarification if multiple match
            from .exceptions import MissingParameterError
            raise MissingParameterError(
                "Please specify the task ID",
                "specify which task by ID",
            )
        else:
            from .exceptions import MissingParameterError
            raise MissingParameterError("Task identifier is required", "specify which task")
    
    async def close(self):
        """Close the executor and release resources."""
        await self.task_tools.close()
        logger.info("Agent executor closed")
