from fastapi import FastAPI
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import RouteRequest, RouteResponse
from database import engine, Calllog   
from router import route_and_call

app = FastAPI()

@app.post("/route", response_model=RouteResponse)
async def route(request: RouteRequest):
    return route_and_call(request)


@app.get("/dashboard")
def dashboard():
    with Session(engine) as session:
        stats = session.query(
            Calllog.model_used,
            func.count(Calllog.id).label("total_calls"),
            func.sum(Calllog.cost_usd).label("total_cost"),
            func.avg(Calllog.latency_seconds).label("avg_latency"),
            func.sum(Calllog.tokens_used).label("total_tokens")
        ).group_by(Calllog.model_used).all()

        dashboard_stats = [
            {
                "model": stat.model_used,
                "total_calls": stat.total_calls,
                "total_cost": stat.total_cost,
                "avg_latency": stat.avg_latency,
                "total_tokens": stat.total_tokens
            }
            for stat in stats
        ]
    return {"stats": dashboard_stats}

@app.get("/health")
def health():
    return {"status": "ok"}