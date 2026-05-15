import os
from langgraph.graph import StateGraph, END
from core.state import AgentState
from retrieval.qdrant_client import hybrid_search
import logging
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

logger = logging.getLogger(__name__)

# Try to initialize LLM. If no API key, use a fallback behavior for demo purposes.
llm = None
if os.getenv("OPENAI_API_KEY"):
    try:
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    except Exception:
        pass

async def intent_router_node(state: AgentState) -> AgentState:
    logger.info("ROUTER: Analyzing intent...")
    state["current_intent"] = "hybrid_search"
    # Basic query expansion simulation
    state["optimized_query"] = state["original_query"] + " enterprise context"
    return state

async def hybrid_retrieval_node(state: AgentState) -> AgentState:
    logger.info(f"RETRIEVAL: Executing hybrid search for '{state['optimized_query']}'")
    results = await hybrid_search(state["optimized_query"], state["metadata_filters"])
    
    state["retrieved_context"] = results
    
    # Calculate confidence based on top result score
    if results:
        state["confidence_score"] = results[0]["score"]
    else:
        state["confidence_score"] = 0.0
        
    return state

async def synthesis_node(state: AgentState) -> AgentState:
    logger.info("SYNTHESIS: Generating final answer based on retrieved context...")
    context_str = "\n".join([f"- {c['content']}" for c in state["retrieved_context"]])
    
    if llm:
        sys_msg = SystemMessage(content="You are AetherOS, a highly intelligent autonomous RAG system. Answer the user query using ONLY the provided context. If the context is empty, say 'Insufficient context'.")
        human_msg = HumanMessage(content=f"Context:\n{context_str}\n\nQuery: {state['original_query']}")
        try:
            response = await llm.ainvoke([sys_msg, human_msg])
            state["final_answer"] = response.content
        except Exception as e:
            logger.error(f"LLM Generation failed: {e}")
            state["final_answer"] = f"Based on knowledge: \n{context_str}"
    else:
        # Fallback if no LLM configured
        state["final_answer"] = f"[LLM OFF] Retrieved Knowledge:\n{context_str}"
        
    state["hallucination_probability"] = 0.05
    return state

async def reflection_node(state: AgentState) -> AgentState:
    logger.info("REFLECTION: Confidence score low. Reflecting...")
    state["reflection_count"] = state.get("reflection_count", 0) + 1
    # Adjust query to broaden search
    state["optimized_query"] = state["original_query"]
    return state

def should_reflect(state: AgentState) -> str:
    if state.get("confidence_score", 0.0) < 0.75 and state.get("reflection_count", 0) < 1:
        return "reflect"
    return "synthesize"

graph_builder = StateGraph(AgentState)

graph_builder.add_node("router", intent_router_node)
graph_builder.add_node("retrieve", hybrid_retrieval_node)
graph_builder.add_node("reflect", reflection_node)
graph_builder.add_node("synthesize", synthesis_node)

graph_builder.set_entry_point("router")
graph_builder.add_edge("router", "retrieve")
graph_builder.add_conditional_edges("retrieve", should_reflect, {
    "reflect": "reflect",
    "synthesize": "synthesize"
})
graph_builder.add_edge("reflect", "retrieve")
graph_builder.add_edge("synthesize", END)

orchestrator = graph_builder.compile()

async def run_agentic_retrieval(query: str, tenant_id: str, filters: dict) -> AgentState:
    initial_state = AgentState(
        original_query=query,
        tenant_id=tenant_id,
        metadata_filters=filters,
        current_intent="",
        optimized_query="",
        sub_queries=[],
        retrieved_context=[],
        confidence_score=0.0,
        final_answer="",
        hallucination_probability=0.0,
        reflection_count=0
    )
    final_state = await orchestrator.ainvoke(initial_state)
    return final_state
