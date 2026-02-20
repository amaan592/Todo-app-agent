"""Intent recognition for natural language instruction parsing.

Uses hybrid rule-based + pattern matching approach for deterministic intent detection.
"""

import re
import logging
from typing import Optional, Any
from dataclasses import dataclass

from .exceptions import IntentRecognitionError, MissingParameterError, AmbiguousReferenceError

logger = logging.getLogger(__name__)


@dataclass
class ParsedIntent:
    """Represents a parsed user instruction.
    
    Attributes:
        intent: Detected intent type (create, read, update, delete)
        parameters: Extracted parameters from the instruction
        confidence: Confidence score (0.0 to 1.0)
        raw_instruction: Original user instruction
    """
    intent: str
    parameters: dict[str, Any]
    confidence: float
    raw_instruction: str


class IntentParser:
    """Parses natural language instructions into structured intents.
    
    Uses keyword matching and regex patterns for intent detection.
    """
    
    # Intent patterns with named groups for parameter extraction
    CREATE_PATTERNS = [
        r"(?i)\b(add|create|make|new|set up)\s+(a\s+)?task\s*(to\s+)?(?P<title>.+)",
        r"(?i)\b(i\s+need\s+to|i\s+want\s+to|i\s+must)\s+(?P<title>.+)",
        r"(?i)\b(add|add task|create task)\s*:\s*(?P<title>.+)",
    ]
    
    READ_PATTERNS = [
        r"(?i)\b(show|list|get|view|what\s+are)\s+(my\s+)?(?P<filter>.+)?\s*tasks?",
        r"(?i)\b(what('|')?s|what is)\s+(my\s+)?(?P<filter>.+)?",
    ]
    
    UPDATE_PATTERNS = [
        r"(?i)\b(mark|complete|finish|done)\s+(task\s+)?(?P<task_id>\d+)",
        r"(?i)\b(update|modify|change)\s+(task\s+)?(?P<task_id>\d+)",
        r"(?i)\b(i('|')?m|i am)\s+(done|finished)\s+with\s+(task\s+)?(?P<task_id>\d+)",
        r"(?i)\b(mark|set)\s+(task\s+)?(?P<task_id>\d+)\s+as\s+(?P<status>pending|complete|done)",
    ]
    
    DELETE_PATTERNS = [
        r"(?i)\b(delete|remove|drop|cancel)\s+(task\s+)?(?P<task_id>\d+)",
        r"(?i)\b(delete|remove)\s+(the\s+)?(?P<title>.+)\s+task",
    ]
    
    # Status keywords for filtering
    STATUS_KEYWORDS = {
        "pending": "PENDING",
        "incomplete": "PENDING",
        "todo": "PENDING",
        "left": "PENDING",
        "completed": "COMPLETED",
        "complete": "COMPLETED",
        "done": "COMPLETED",
        "finished": "COMPLETED",
    }
    
    def __init__(self):
        """Initialize the intent parser with compiled regex patterns."""
        self._compiled_patterns = {
            "create": [re.compile(p) for p in self.CREATE_PATTERNS],
            "read": [re.compile(p) for p in self.READ_PATTERNS],
            "update": [re.compile(p) for p in self.UPDATE_PATTERNS],
            "delete": [re.compile(p) for p in self.DELETE_PATTERNS],
        }
    
    def parse(self, instruction: str) -> ParsedIntent:
        """Parse a natural language instruction into a structured intent.
        
        Args:
            instruction: User's natural language instruction
            
        Returns:
            ParsedIntent with detected intent and extracted parameters
            
        Raises:
            IntentRecognitionError: If intent cannot be determined
            MissingParameterError: If required parameters are missing
        """
        instruction = instruction.strip()
        
        if not instruction:
            raise MissingParameterError("Empty instruction", "say")
        
        logger.debug(f"Parsing instruction: {instruction}")
        
        # Try each intent type in priority order
        for intent_type in ["create", "read", "update", "delete"]:
            parsed = self._try_match_intent(instruction, intent_type)
            if parsed:
                logger.info(f"Detected intent: {intent_type} (confidence: {parsed.confidence})")
                return parsed
        
        # No intent matched
        logger.warning(f"No intent matched for instruction: {instruction}")
        raise IntentRecognitionError()
    
    def _try_match_intent(self, instruction: str, intent_type: str) -> Optional[ParsedIntent]:
        """Try to match instruction against patterns for a specific intent.
        
        Args:
            instruction: User instruction
            intent_type: Intent type to match
            
        Returns:
            ParsedIntent if matched, None otherwise
        """
        for pattern in self._compiled_patterns[intent_type]:
            match = pattern.search(instruction)
            if match:
                parameters = self._extract_parameters(match, intent_type, instruction)
                if parameters is not None:
                    return ParsedIntent(
                        intent=intent_type,
                        parameters=parameters,
                        confidence=0.9,  # High confidence for pattern match
                        raw_instruction=instruction,
                    )
        return None
    
    def _extract_parameters(
        self,
        match: re.Match,
        intent_type: str,
        instruction: str,
    ) -> Optional[dict[str, Any]]:
        """Extract parameters from a regex match.
        
        Args:
            match: Regex match object
            intent_type: Type of intent
            instruction: Original instruction
            
        Returns:
            Dictionary of extracted parameters, or None if extraction fails
        """
        groups = match.groupdict()
        
        if intent_type == "create":
            return self._extract_create_params(groups, instruction)
        elif intent_type == "read":
            return self._extract_read_params(groups)
        elif intent_type == "update":
            return self._extract_update_params(groups)
        elif intent_type == "delete":
            return self._extract_delete_params(groups, instruction)
        
        return None
    
    def _extract_create_params(
        self,
        groups: dict[str, Optional[str]],
        instruction: str,
    ) -> Optional[dict[str, Any]]:
        """Extract parameters for create intent."""
        title = groups.get("title", "").strip()
        
        if not title:
            # Try to extract from remainder of instruction
            title = instruction.strip()
            # Remove common prefixes
            for prefix in ["i need to ", "i want to ", "i must ", "add ", "create "]:
                if title.lower().startswith(prefix):
                    title = title[len(prefix):]
        
        if not title:
            return None
        
        return {"title": title}
    
    def _extract_read_params(
        self,
        groups: dict[str, Optional[str]],
    ) -> dict[str, Any]:
        """Extract parameters for read intent."""
        filter_text = groups.get("filter", "")
        
        if filter_text:
            filter_text = filter_text.lower().strip()
            # Check for status filter
            for keyword, status in self.STATUS_KEYWORDS.items():
                if keyword in filter_text:
                    return {"status": status}
        
        return {}  # No filter = return all tasks
    
    def _extract_update_params(
        self,
        groups: dict[str, Optional[str]],
    ) -> Optional[dict[str, Any]]:
        """Extract parameters for update intent."""
        task_id_str = groups.get("task_id")
        status_str = groups.get("status")
        
        if task_id_str:
            task_id = int(task_id_str)
            params = {"task_id": task_id}
            
            # Determine status change
            if status_str:
                status_str = status_str.lower()
                if status_str in ["complete", "done"]:
                    params["status"] = "COMPLETED"
                elif status_str == "pending":
                    params["status"] = "PENDING"
            
            return params
        
        return None
    
    def _extract_delete_params(
        self,
        groups: dict[str, Optional[str]],
        instruction: str,
    ) -> Optional[dict[str, Any]]:
        """Extract parameters for delete intent."""
        task_id_str = groups.get("task_id")
        title = groups.get("title")
        
        if task_id_str:
            return {"task_id": int(task_id_str)}
        elif title:
            # Delete by title - will need clarification if multiple match
            return {"title_query": title.strip()}
        
        return None
    
    def extract_task_id(self, instruction: str) -> Optional[int]:
        """Extract a task ID from instruction using simple pattern.
        
        Args:
            instruction: User instruction
            
        Returns:
            Task ID if found, None otherwise
        """
        pattern = r"\b(task\s+)?(\d+)\b"
        match = re.search(pattern, instruction, re.IGNORECASE)
        if match:
            return int(match.group(2))
        return None
