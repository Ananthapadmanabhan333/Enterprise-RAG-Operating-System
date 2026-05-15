from typing import TypedDict, List, Dict, Any, Optional

class AgentState(TypedDict):
    """The shared state dictionary used across all LangGraph nodes."""
    original_query: str
    tenant_id: str
    metadata_filters: Dict[str, Any]
    
    # Execution Tracking
    current_intent: str
    optimized_query: str
    sub_queries: List[str]
    
    # Retrieval
    retrieved_context: List[Dict[str, Any]]
    confidence_score: float
    
    # Generation
    final_answer: str
    hallucination_probability: float
    
    # Loop control
    reflection_count: int
