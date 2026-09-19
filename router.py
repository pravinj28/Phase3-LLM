
from sqlalchemy.orm import declarative_base, Session
import litellm
import time

from database import engine, Calllog
from models import RouteRequest, RouteResponse

def classify_complexity(prompt: str) -> tuple[str, str]:
    if len(prompt.split()) < 20:
        return "low", "gemini/gemini-3.6-flash"
    if any(keyword in prompt.lower() for keyword in ["code", "function", "debug"]):
        return "high", "gemini/gemini-3.6-flash"
    else:
        return "medium", "gemini/gemini-3.6-flash"

def route_and_call(request: RouteRequest) -> RouteResponse:
    complexity, model = classify_complexity(request.prompt)
    
    start_time = time.time()
    response = litellm.completion(
        messages=[{"role": "user", "content": request.prompt}],
        model=model,
        temperature=0.7,
        max_tokens=500
    )
    latency = time.time() - start_time

    response_text = response.choices[0].message.content
    tokens_used = response.usage.total_tokens
    cost_usd = litellm.completion_cost(completion_response=response)

    # Log the call to the database
    with Session(engine) as session:
        call_log = Calllog(
            model_used=model,
            complexity=complexity,
            tokens_used=tokens_used,
            cost_usd=cost_usd,
            latency_seconds=latency
        )
        session.add(call_log)
        session.commit()

    return RouteResponse(
        response=response_text,
        model_used=model,
        tokens_used=tokens_used,
        cost_usd=cost_usd,
        latency_seconds=latency,
        complexity=complexity
    )
