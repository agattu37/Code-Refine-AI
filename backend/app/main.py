from fastapi import FastAPI, HTTPException
from app.schemas import RefactorRequest, RefactorResponse
from app.services.llm import llm_client

app = FastAPI(title="CodeRefine AI Core", version="0.1.0")

@app.get("/")
async def root():
    return {"status": "active", "service": "CodeRefine AI"}

@app.get("/health")
async def health():
    """Lightweight health check for platform readiness/liveness probes."""
    return {"status": "ok", "service": "CodeRefine AI"}

@app.post("/refactor", response_model=RefactorResponse)
async def refactor_code(payload: RefactorRequest):
    """
    Receives code snippet, sends it to Gemini, and returns the result.
    """
    # Call the LLM Service
    try:
        ai_response = await llm_client.analyze_code(
            code=payload.code, 
            instruction=payload.instruction
        )
        
        # Simple parsing logic (we will make this robust in Phase 3)
        # Assuming the AI returns the code block first.
        # snippet from main.py (no changes needed)
        
        return RefactorResponse(
            original_code=payload.code,
            refactored_code=ai_response.code, 
            explanation=ai_response.explanation
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))