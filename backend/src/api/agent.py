from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging

from ..agent.executor import AgentExecutor
from ..agent.exceptions import (
    AgentError,
    IntentRecognitionError,
    MissingParameterError,
    InvalidTaskIdError,
    BackendAPIError,
    AmbiguousReferenceError,
)

logger = logging.getLogger(__name__)

router = APIRouter()


class AgentRequest(BaseModel):
    """Request model for agent instruction."""
    instruction: str


class AgentResponse(BaseModel):
    """Response model for agent execution."""
    success: bool
    response: str
    error: str | None = None


@router.post("/agent/execute", response_model=AgentResponse)
async def execute_agent_instruction(request: AgentRequest):
    """Execute a natural language instruction via the AI Agent.
    
    The agent interprets natural language and performs task management operations
    (create, read, update, delete) through the backend API.
    
    Args:
        request: AgentRequest containing the natural language instruction
        
    Returns:
        AgentResponse with the agent's response or error message
    """
    try:
        logger.info(f"Received agent instruction: {request.instruction}")
        
        # Create agent executor
        executor = AgentExecutor()
        
        try:
            # Execute the instruction
            response = await executor.execute(request.instruction)
            
            logger.info(f"Agent execution successful")
            
            return AgentResponse(
                success=True,
                response=response,
                error=None
            )
        finally:
            # Clean up resources
            await executor.close()
            
    except IntentRecognitionError as e:
        logger.warning(f"Intent recognition failed: {e.message}")
        raise HTTPException(
            status_code=400,
            detail=f"I couldn't understand that instruction. {e.user_message}"
        )
    except MissingParameterError as e:
        logger.warning(f"Missing parameter: {e.message}")
        raise HTTPException(
            status_code=400,
            detail=f"Please provide more information: {e.user_message}"
        )
    except InvalidTaskIdError as e:
        logger.warning(f"Invalid task ID: {e.task_id}")
        raise HTTPException(
            status_code=404,
            detail=f"Task #{e.task_id} not found. Please check the task ID and try again."
        )
    except AmbiguousReferenceError as e:
        logger.warning(f"Ambiguous reference: {e.message}")
        raise HTTPException(
            status_code=400,
            detail=f"Your request is ambiguous. {e.user_message}"
        )
    except BackendAPIError as e:
        logger.error(f"Backend API error: {e.message}")
        raise HTTPException(
            status_code=503,
            detail=f"Backend service unavailable: {e.message}"
        )
    except AgentError as e:
        logger.error(f"Agent error: {e.message}")
        raise HTTPException(
            status_code=500,
            detail=f"Agent error: {e.user_message}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again."
        )


@router.get("/agent/health")
async def agent_health_check():
    """Health check endpoint for the agent service.
    
    Returns:
        dict: Health status
    """
    return {"status": "healthy", "service": "ai-agent"}
