from pydantic import BaseModel
from typing import List, Optional

# Request model — what comes IN
class CompletionRequest(BaseModel):
    prompt: str
    system_prompt: str = "You are a helpful assistant"
    model: str = "gemini/gemini-3.6-flash"
    temperature: float = 0.7
    max_tokens: int = 500

# Response model — what goes OUT
class CompletionResponse(BaseModel):
    response: str
    model_used: str
    tokens_used: int
    estimated_cost_usd: float
    latency_seconds: float