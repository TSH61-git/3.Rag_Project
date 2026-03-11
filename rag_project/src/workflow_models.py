from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum

# Events - מה יכול לקרות בכל שלב
class EventType(Enum):
    INPUT_VALID = "input_valid"
    INPUT_INVALID = "input_invalid"
    NODES_FOUND = "nodes_found"
    NO_NODES_FOUND = "no_nodes_found"
    QUALITY_GOOD = "quality_good"
    QUALITY_LOW = "quality_low"
    RESPONSE_READY = "response_ready"
    ERROR = "error"

@dataclass
class Event:
    """אירוע שקורה בזרימה"""
    type: EventType
    message: str = ""
    data: dict = field(default_factory=dict)

# State - מה אנחנו זוכרים לאורך התהליך
@dataclass
class QueryState:
    """מצב השאילתה לאורך כל התהליך"""
    query: str = ""
    nodes: List = field(default_factory=list)
    confidence_score: float = 0.0
    response: str = ""
    error: Optional[str] = None
    
    def has_nodes(self) -> bool:
        return len(self.nodes) > 0
    
    def get_avg_score(self) -> float:
        if not self.nodes:
            return 0.0
        return sum(node.score for node in self.nodes) / len(self.nodes)
