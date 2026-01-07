from pydantic import BaseModel, Field
from typing import Optional

class RefactorRequest(BaseModel):
    # The code selected by the user
    code: str = Field(..., description="The raw source code to refactor")
    
    # Context regarding the file (helpful for later)
    language: str = Field(default="python", description="Language of the snippet")
    file_path: Optional[str] = Field(None, description="Path to the file in the workspace")
    
    # What the user wants to do (e.g., "Optimize", "Fix Security")
    instruction: Optional[str] = Field(default="Refactor this code", description="User's specific intent")

class RefactorResponse(BaseModel):
    original_code: str
    refactored_code: str
    explanation: str