"""Pydantic schemas for AI Agent tool calls and results."""

from pydantic import BaseModel, Field
from typing import Any, Optional


class ToolCall(BaseModel):
    """Represents a tool invocation request.
    
    Attributes:
        tool_name: Name of the tool to invoke (e.g., 'create_task', 'get_tasks')
        parameters: Dictionary of parameters to pass to the tool
        call_id: Unique identifier for tracing this call
    """
    tool_name: str = Field(..., description="Name of the tool to invoke")
    parameters: dict = Field(default_factory=dict, description="Tool parameters")
    call_id: str = Field(..., description="Unique identifier for tracing")


class ToolResult(BaseModel):
    """Represents the result of a tool invocation.
    
    Attributes:
        success: Whether the tool execution was successful
        data: Optional data returned by the tool
        error: Optional error message if execution failed
        tool_name: Name of the tool that was invoked
    """
    success: bool = Field(..., description="Whether execution was successful")
    data: Optional[Any] = Field(default=None, description="Data returned by tool")
    error: Optional[str] = Field(default=None, description="Error message if failed")
    tool_name: str = Field(..., description="Name of the tool invoked")
