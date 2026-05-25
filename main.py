"""
FastAPI wrapper for Quick Wiki Research Assistant
Provides REST API endpoints for the LangGraph-based research system
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import os
from dotenv import load_dotenv

# Import your existing LangGraph code
from research_assistant import graph

load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Quick Wiki API",
    description="Multi-agent Wikipedia research assistant powered by LangGraph",
    version="1.0.0"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",          # Local development
        "https://sahil.page",             # Production
        "https://*.vercel.app",           # Vercel previews
        "https://*.up.railway.app"        # Railway previews
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class AnalystInfo(BaseModel):
    """Information about a generated analyst"""
    name: str
    role: str
    affiliation: str

class ResearchRequest(BaseModel):
    """Request model for research endpoint"""
    topic: str = Field(..., description="Research topic or question", min_length=5, max_length=500)
    max_analysts: int = Field(default=3, description="Number of analyst perspectives", ge=2, le=5)
    human_analyst_feedback: str = Field(default="approve", description="Feedback for analyst creation")

class ResearchResponse(BaseModel):
    """Response model for research endpoint"""
    final_report: str = Field(..., description="Complete research report in Markdown format")
    analysts: List[AnalystInfo] = Field(..., description="List of analysts who contributed")
    status: str = Field(..., description="Status of the research process")

# API Endpoints

@app.get("/")
def root():
    """Root endpoint - API information"""
    return {
        "service": "Quick Wiki API",
        "version": "1.0.0",
        "description": "Multi-agent Wikipedia research assistant",
        "endpoints": {
            "health": "/api/health",
            "research": "/api/research"
        }
    }

@app.get("/api/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "Quick Wiki API",
        "openrouter_configured": bool(os.getenv("OPENROUTER_API_KEY")),
        "tavily_configured": bool(os.getenv("TAVILY_API_KEY"))
    }

@app.post("/api/research", response_model=ResearchResponse)
async def conduct_research(request: ResearchRequest):
    """
    Conduct multi-agent research on a topic
    
    This endpoint:
    1. Creates multiple AI analyst personas based on the topic
    2. Each analyst conducts interviews with expert sub-agents
    3. Gathers information from Wikipedia and web search
    4. Compiles a comprehensive research report
    
    **Parameters:**
    - **topic**: Research topic or question (5-500 characters)
    - **max_analysts**: Number of analyst perspectives (2-5, default: 3)
    - **human_analyst_feedback**: Feedback for analyst creation (default: "approve")
    
    **Returns:**
    - **final_report**: Complete research report in Markdown format
    - **analysts**: List of analyst personas who contributed
    - **status**: Status of the research process
    
    **Note:** This endpoint may take 1-3 minutes depending on the number of analysts.
    """
    try:
        # Validate API keys
        if not os.getenv("OPENROUTER_API_KEY"):
            raise HTTPException(status_code=500, detail="OpenRouter API key not configured")
        if not os.getenv("TAVILY_API_KEY"):
            raise HTTPException(status_code=500, detail="Tavily API key not configured")
        
        # Initial state for LangGraph
        initial_state = {
            "topic": request.topic,
            "max_analysts": request.max_analysts,
            "human_analyst_feedback": request.human_analyst_feedback,
            "analysts": [],
            "sections": [],
            "introduction": "",
            "content": "",
            "conclusion": "",
            "final_report": ""
        }
        
        # Execute the LangGraph workflow
        final_state = graph.invoke(initial_state)
        
        # Extract analyst information
        analysts_info = [
            AnalystInfo(
                name=analyst.name,
                role=analyst.role,
                affiliation=analyst.affiliation
            ) for analyst in final_state.get("analysts", [])
        ]
        
        # Get final report
        final_report = final_state.get("final_report", "")
        
        if not final_report:
            raise HTTPException(status_code=500, detail="Report generation failed - empty report")
        
        return ResearchResponse(
            final_report=final_report,
            analysts=analysts_info,
            status="completed"
        )
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Research failed: {str(e)}"
        )

# Run the server (for local testing)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True  # Auto-reload on code changes
    )
