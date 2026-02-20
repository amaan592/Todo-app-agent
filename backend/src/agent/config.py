"""Configuration for AI Agent operations.

Provides centralized configuration for backend API connection and agent behavior.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class AgentConfig:
    """Agent configuration settings.
    
    All settings can be overridden via environment variables.
    """
    
    # Backend API configuration
    BACKEND_BASE_URL: str = os.getenv("AGENT_BACKEND_URL", "http://localhost:8000")
    BACKEND_TIMEOUT: int = int(os.getenv("AGENT_BACKEND_TIMEOUT", "10"))
    BACKEND_RETRY_COUNT: int = int(os.getenv("AGENT_BACKEND_RETRIES", "2"))
    
    # Agent behavior configuration
    AMBIGUITY_THRESHOLD: int = int(os.getenv("AGENT_AMBIGUITY_THRESHOLD", "2"))
    # Maximum number of matching tasks before requesting clarification
    
    @classmethod
    def get_api_endpoint(cls, path: str) -> str:
        """Get full API endpoint URL for a given path.
        
        Args:
            path: API path (e.g., '/api/v1/tasks')
            
        Returns:
            Full URL including base URL
        """
        return f"{cls.BACKEND_BASE_URL}{path}"


# Convenience access
BACKEND_BASE_URL = AgentConfig.BACKEND_BASE_URL
BACKEND_TIMEOUT = AgentConfig.BACKEND_TIMEOUT
BACKEND_RETRY_COUNT = AgentConfig.BACKEND_RETRY_COUNT
