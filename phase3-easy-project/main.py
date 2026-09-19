from fastapi import FastAPI
from models import CompletionRequest, CompletionResponse
import litellm
import time

from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

history = []

@app.post("/complete", response_model=CompletionResponse)
async def complete(request: CompletionRequest):
    start_time = time.time()

    response = litellm.completion(
        model=request.model,
        messages=[
            {"role": "system", "content": request.system_prompt},
            {"role": "user", "content": request.prompt}
        ],
        temperature=request.temperature,
        max_tokens=request.max_tokens
    )

    latency_seconds = time.time() - start_time
    response_text = response.choices[0].message.content
    tokens_used = response.usage.total_tokens
    estimated_cost_usd = litellm.completion_cost(completion_response=response)

    history.append({
        "prompt": request.prompt,
        "model_used": request.model,
        "tokens_used": tokens_used,
        "estimated_cost_usd": estimated_cost_usd,
        "latency_seconds": latency_seconds
    })

    if len(history) > 10:
        history.pop(0)

    return CompletionResponse(
        response=response_text,
        model_used=request.model,
        tokens_used=tokens_used,
        estimated_cost_usd=estimated_cost_usd,
        latency_seconds=latency_seconds
    )

@app.get("/models")
def get_models():
    return {
        "models": [
            "groq/llama-3.1-8b-instant",
            "groq/mixtral-8x7b-32768",
            "gpt-3.5-turbo",
            "gpt-4"
        ]
    }

@app.get("/history")
def get_history():
    return history