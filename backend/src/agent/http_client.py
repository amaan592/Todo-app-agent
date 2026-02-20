"""HTTP client wrapper for AI Agent backend communication.

Provides async HTTP client with error handling, timeouts, and retry logic.
"""

import httpx
import logging
from typing import Optional, Any

from .config import AgentConfig
from .exceptions import BackendAPIError

logger = logging.getLogger(__name__)


class AgentHTTPClient:
    """Async HTTP client for backend API communication.
    
    Handles connection management, error handling, and response parsing.
    """
    
    def __init__(self):
        """Initialize the HTTP client with configuration."""
        self.base_url = AgentConfig.BACKEND_BASE_URL
        self.timeout = AgentConfig.BACKEND_TIMEOUT
        self.retry_count = AgentConfig.BACKEND_RETRY_COUNT
        self._client: Optional[httpx.AsyncClient] = None
    
    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create the async HTTP client.
        
        Returns:
            Configured AsyncClient instance
        """
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=httpx.Timeout(self.timeout),
                headers={"Content-Type": "application/json"},
            )
        return self._client
    
    async def close(self):
        """Close the HTTP client connection."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None
    
    async def request(
        self,
        method: str,
        path: str,
        json_data: Optional[dict] = None,
        params: Optional[dict] = None,
    ) -> dict[str, Any]:
        """Make an HTTP request to the backend API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            path: API path (e.g., '/api/v1/tasks')
            json_data: Optional JSON payload for POST/PUT requests
            params: Optional query parameters
            
        Returns:
            Parsed JSON response as dictionary
            
        Raises:
            BackendAPIError: If request fails or returns error status
        """
        client = await self._get_client()
        url = f"{self.base_url}{path}"
        
        try:
            logger.debug(f"Making {method} request to {url}")
            
            response = await client.request(
                method=method,
                url=url,
                json=json_data,
                params=params,
            )
            
            # Handle error status codes
            if response.status_code >= 400:
                logger.error(f"Backend API error: {response.status_code} - {response.text}")
                raise BackendAPIError(
                    message=f"Backend returned {response.status_code}",
                    status_code=response.status_code,
                )
            
            # Parse and return JSON response
            try:
                return response.json()
            except httpx.JSONDecodeError:
                logger.warning(f"Non-JSON response from {url}")
                return {}
                
        except httpx.ConnectError as e:
            logger.error(f"Connection error to {url}: {str(e)}")
            raise BackendAPIError(
                message=f"Failed to connect to backend: {str(e)}",
                status_code=None,
            )
        except httpx.TimeoutException as e:
            logger.error(f"Request timeout to {url}: {str(e)}")
            raise BackendAPIError(
                message="Request timed out",
                status_code=None,
            )
        except httpx.RequestError as e:
            logger.error(f"Request error to {url}: {str(e)}")
            raise BackendAPIError(
                message=f"Request failed: {str(e)}",
                status_code=None,
            )
    
    async def get(self, path: str, params: Optional[dict] = None) -> dict[str, Any]:
        """Make a GET request.
        
        Args:
            path: API path
            params: Optional query parameters
            
        Returns:
            Parsed JSON response
        """
        return await self.request("GET", path, params=params)
    
    async def post(self, path: str, json_data: dict) -> dict[str, Any]:
        """Make a POST request.
        
        Args:
            path: API path
            json_data: JSON payload
            
        Returns:
            Parsed JSON response
        """
        return await self.request("POST", path, json_data=json_data)
    
    async def put(self, path: str, json_data: dict) -> dict[str, Any]:
        """Make a PUT request.
        
        Args:
            path: API path
            json_data: JSON payload
            
        Returns:
            Parsed JSON response
        """
        return await self.request("PUT", path, json_data=json_data)
    
    async def delete(self, path: str) -> dict[str, Any]:
        """Make a DELETE request.
        
        Args:
            path: API path
            
        Returns:
            Parsed JSON response
        """
        return await self.request("DELETE", path)
