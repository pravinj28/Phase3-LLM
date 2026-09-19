from pydantic import BaseModel
from typing import List, Optional

class RouteRequest(BaseModel):
    prompt: str
    task_type : Optional[str] = "auto"

class RouteResponse(BaseModel):
    response: str
    model_used: str
    tokens_used: int
    cost_usd: float
    latency_seconds: float
    complexity : str


class DashboardStats(BaseModel):
    model : str
    total_calls: int
    total_cost : float
    avg_latency : float
    total_tokens : int
