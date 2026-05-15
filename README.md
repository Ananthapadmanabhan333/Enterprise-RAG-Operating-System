# 🌌 AetherOS: The Autonomous Enterprise RAG Operating System

AetherOS is a next-generation, AI-native Retrieval-Augmented Generation (RAG) Operating System designed to power mission-critical enterprise intelligence. It is a distributed, highly observable, and fully autonomous semantic infrastructure platform. 

This repository contains the deployable ecosystem encompassing:
- **aether-frontend**: Next.js 14 cinematic, highly-responsive UI with real-time vector visualization.
- **aether-backend**: FastAPI-driven, LangGraph orchestrated multi-agent retrieval pipeline.
- **qdrant**: High-performance Vector Database.
- **neo4j**: Semantic Enterprise Knowledge Graph.
- **infrastructure**: Docker Compose setup for one-click deployment.

## 🚀 Features
- **Multi-Agent Orchestration**: Intent routing, query planning, and post-generation hallucination detection via LLM-as-a-judge.
- **Hybrid Retrieval**: Combines Dense Vector Search, Sparse BM25 Search, and Graph Traversal fused via Reciprocal Rank Fusion.
- **Cinematic Observability**: Live retrieval traces and confidence metrics.

## 🛠 Deployment

The entire system can be spun up using Docker Compose:

```bash
# 1. Setup environment variables
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env

# 2. Deploy
docker-compose up -d --build
```

Access the UI at `http://localhost:3000`

## Architecture
See `RAG_OS_ARCHITECTURE_BLUEPRINT.md` for extreme detail on the 32-module infrastructure architecture, including ingestion scaling, AST-aware chunking, and enterprise security guardrails.
