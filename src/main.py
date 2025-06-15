import os
from typing import Dict
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import logging
import traceback

from agents.orchestrator import OrchestratorAgent
from agents.web_navigation import WebNavigationAgent
from agents.form_analysis import FormAnalysisAgent
from agents.code_generation import CodeGenerationAgent
from config.logging import setup_logging

# Load environment variables
load_dotenv()

# Set up logging
setup_logging()

# Initialize FastAPI app
app = FastAPI(
    title="ART Code Generation System",
    description="A system for automating the migration of legacy ASP.NET WebForms to modern REST APIs and HTML forms",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
orchestrator = OrchestratorAgent()

class GenerationRequest(BaseModel):
    url: str
    platform: str
    form_name: str
    language: str

@app.on_event("startup")
async def startup_event():
    """Initialize agents on startup."""
    try:
        await orchestrator.initialize()
        logging.info("Application started successfully")
    except Exception as e:
        logging.error(f"Error during startup: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup resources on shutdown."""
    try:
        await orchestrator.cleanup()
        logging.info("Application shutdown successfully")
    except Exception as e:
        logging.error(f"Error during shutdown: {str(e)}")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logging.error(f"Unhandled exception: {str(exc)}")
    logging.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "error": "Internal server error",
            "detail": str(exc)
        }
    )

@app.post("/generate")
async def generate_code(request: GenerationRequest) -> Dict:
    """
    Generate code based on the provided request.
    
    Args:
        request: GenerationRequest containing URL, platform, form name, and language
        
    Returns:
        Dictionary containing generated code and analysis results
    """
    try:
        logging.info(f"Received generation request: {request.dict()}")
        
        result = await orchestrator.execute({
            "url": request.url,
            "platform": request.platform,
            "form_name": request.form_name,
            "language": request.language
        })
        
        if result["status"] == "error":
            logging.error(f"Generation failed: {result['error']}")
            raise HTTPException(status_code=500, detail=result["error"])
        
        logging.info("Generation completed successfully")
        return result
    except Exception as e:
        logging.error(f"Error during code generation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check() -> Dict:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    ) 