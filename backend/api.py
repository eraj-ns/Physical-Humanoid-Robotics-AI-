"""
FastAPI server for RAG Agent integration

This module creates a FastAPI server that exposes a query endpoint
to connect frontend applications with the RAG agent.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import sys
import logging

# Add the backend directory to the path to import the agent
sys.path.append(os.path.join(os.path.dirname(__file__)))

from agent import RAGAgent, AgentResponse

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="RAG Agent API",
    description="API for interacting with the RAG agent",
    version="1.0.0"
)

# Add CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define Pydantic models for request/response
class QueryRequest(BaseModel):
    query: str

class Source(BaseModel):
    id: str
    url: str
    text: str

class APIError(BaseModel):
    error: str
    status_code: int
    details: Optional[Dict[str, Any]] = None

class AgentResponseModel(BaseModel):
    content: str
    sources: List[Source]
    confidence: str
    follow_up_questions: Optional[List[str]] = None

# Initialize the RAG agent
rag_agent = RAGAgent()

@app.get("/")
def read_root():
    return {"message": "RAG Agent API is running!"}

@app.post("/query",
          response_model=AgentResponseModel,
          responses={
              400: {"model": APIError},
              500: {"model": APIError}
          })
async def query_endpoint(request: QueryRequest):
    """
    Process a user query using the RAG agent and return the response.

    Args:
        request: QueryRequest containing the user's query

    Returns:
        AgentResponseModel containing the agent's response with sources and confidence
    """
    try:
        # Validate the query
        if not request.query or not request.query.strip():
            raise HTTPException(
                status_code=400,
                detail={"error": "Query cannot be empty", "status_code": 400}
            )

        # Process the query using the RAG agent
        # Since we're in an async context, we need to run the sync method properly
        import asyncio
        loop = asyncio.get_event_loop()
        agent_response: AgentResponse = await loop.run_in_executor(None, rag_agent.query, request.query)

        # Format the response
        formatted_response = AgentResponseModel(
            content=agent_response.content,
            sources=[Source(id=src["id"], url=src["url"], text=src["text"]) for src in agent_response.sources],
            confidence=agent_response.confidence,
            follow_up_questions=agent_response.follow_up_questions
        )

        logger.info(f"Query processed successfully: {request.query[:50]}...")
        return formatted_response

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error occurred while processing the query",
                "status_code": 500,
                "details": {"message": str(e)}
            }
        )

@app.get("/health")
def health_check():
    """
    Health check endpoint to verify the API is running and the RAG agent is accessible.
    """
    try:
        # Try to initialize an agent to check if dependencies are working
        test_agent = RAGAgent()
        return {"status": "healthy", "agent": "available"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Health check failed",
                "status_code": 500,
                "details": {"message": str(e)}
            }
        )

# Add the option to run the server directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)