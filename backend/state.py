from typing import List, TypedDict, Annotated, Optional
import operator

class AgentThought(TypedDict):
    agent: str
    thought: str
    timestamp: str

class Disruption(TypedDict):
    id: str
    type: str  # e.g., "Natural Disaster", "Port Strike", "Geopolitical"
    location: str
    severity: str # High, Medium, Low
    description: str
    source: str

class InventoryStatus(TypedDict):
    product: str
    stock_level: int
    reorder_point: int
    status: str # OK, At Risk, Out of Stock

class MitigationStep(TypedDict):
    action: str
    priority: str
    impact: str

class SupplyChainState(TypedDict):
    # The history of agent reasoning
    thoughts: Annotated[List[AgentThought], operator.add]
    
    # Extracted risk data
    disruptions: List[Disruption]
    
    # Inventory health
    inventory: List[InventoryStatus]
    
    # Final recommendations
    mitigation_plan: List[MitigationStep]
    
    # Current focus/status
    current_agent: str
    next_step: str
