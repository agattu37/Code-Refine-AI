import os
from google import genai
from dotenv import load_dotenv
import re
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Configure the SDK
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in environment variables")

class RefractoredCode(BaseModel):
    code: str
    explanation: str

class GeminiService:
    def __init__(self):
        """
        Initialize the Gemini client. 
        Using gemini-3-flash-preview for speed/cost or gemini-2.0-flash-exp for reasoning.
        """
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def _clean_json_string(self, text: str) -> str:
        """
        Helper to strip markdown code blocks if the LLM includes them.
        """
        # Remove ```json and ``` 
        clean_text = re.sub(r"```json\s*", "", text)
        clean_text = re.sub(r"```\s*", "", clean_text)
        return clean_text.strip()

    async def analyze_code(self, code: str, instruction: str) -> str:
        """
        Sends code + context to Gemini and returns the refactored result.
        """
        prompt = f"""
        You are an expert Senior Software Engineer.
        Your task is to refactor the following code based on the user's instruction.
        
        INSTRUCTION: {instruction}
        
        CODE TO REFACTOR:
        ```
        {code}
        ```
        
        OUTPUT FORMAT:
        Return ONLY the refactored code inside markdown code blocks. 
        Followed by a brief explanation.
        """
        
        try:
            # Generate content (asynchronous call if supported, or sync wrapper)
            # The SDK supports async via `generate_content_async`
            response = await self.client.aio.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_json_schema": RefractoredCode.model_json_schema(),
                }
            )
            code = RefractoredCode.model_validate_json(response.text)
            return code
        except Exception as e:
            return f"Error communicating with Gemini: {str(e)}"

# Singleton instance to be imported
llm_client = GeminiService()