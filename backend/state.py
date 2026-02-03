from typing import List, TypedDict, Annotated, Optional
import operator

class AgentThought(TypedDict):
    agent: str
    thought: str
    timestamp: str

class ResearchFinding(TypedDict):
    id: str
    category: str  # e.g., "Technology", "Geopolitical", "Science"
    title: str
    description: str
    source: str

class KnowledgeTopic(TypedDict):
    topic: str
    depth_score: int # 0-100
    status: str # Under-analyzed, Comprehensive, Needs Update

class StrategicRecommendation(TypedDict):
    recommendation: str
    impact: str
    confidence: str

class ResearchState(TypedDict):
    # The history of agent reasoning
    thoughts: Annotated[List[AgentThought], operator.add]
    
    # Extracted findings
    findings: List[ResearchFinding]
    
    # Existing knowledge context
    knowledge_hub: List[KnowledgeTopic]
    
    # Final strategies
    strategies: List[StrategicRecommendation]
    
    # The user's research query
    query: str
    
    # Current focus/status
    current_agent: str
    next_step: str
