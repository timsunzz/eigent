from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import text

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    status: str
    service: str
    database: str = "unknown"


@router.get("/health", name="health check", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for monitoring and container orchestration."""
    db_status = "ok"
    try:
        from app.component.database import engine

        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception:
        db_status = "error"
        return JSONResponse(
            status_code=503,
            content={"status": "error", "service": "eigent-server", "database": db_status},
        )

    return HealthResponse(status="ok", service="eigent-server", database=db_status)
