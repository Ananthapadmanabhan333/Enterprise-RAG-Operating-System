from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List
import logging
from agents.orchestrator import run_agentic_retrieval

app = FastAPI(title="AetherOS API", version="2.0.0-rc1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QueryRequest(BaseModel):
    query: str
    tenant_id: str
    metadata_filters: Dict[str, Any] = {}

class QueryResponse(BaseModel):
    answer: str
    confidence_score: float
    retrieved_chunks: List[Dict[str, Any]]

@app.get("/health")
async def health_check():
    return {"status": "operational", "system": "AetherOS Core"}

@app.post("/api/v1/retrieval/query", response_model=QueryResponse)
async def retrieval_query(req: QueryRequest):
    try:
        logger.info(f"Received query: {req.query} for tenant: {req.tenant_id}")
        
        # Invoke LangGraph multi-agent orchestrator
        result_state = await run_agentic_retrieval(req.query, req.tenant_id, req.metadata_filters)
        
        return QueryResponse(
            answer=result_state.get("final_answer", "No answer generated."),
            confidence_score=result_state.get("confidence_score", 0.0),
            retrieved_chunks=result_state.get("retrieved_context", [])
        )
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))
