from app.db.database import Base, engine
import app.models
from fastapi import FastAPI
from sqlalchemy import text

from app.db.database import Base, engine

from app.api.user import router as user_router
from app.api.asset import router as asset_router
from app.api.asset_assignment import (
    router as assignment_router
)

import app.models.asset
import app.models.asset_assignment
import app.models.audit_log

from app.api.audit_log import router as audit_router
from app.api.asset_disposal import (
    router as asset_disposal_router
)

from app.api.dashboard import router as dashboard_router

from app.api.auth import (
    router as auth_router
)
from app.api.recent_activity import router as recent_activity_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Army Asset Lifecycle Management System",
    description="Backend API for Army Inventory Management",
    version="1.0.0",
    debug=True
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import Request

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"REQUEST: {request.method} {request.url}")
    response = await call_next(request)
    print(f"RESPONSE: {response.status_code}")
    return response

app.include_router(user_router)
app.include_router(asset_router)
app.include_router(assignment_router)
app.include_router(asset_disposal_router)
app.include_router(auth_router)
app.include_router(audit_router)
app.include_router(dashboard_router)
app.include_router(recent_activity_router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {
        "message": "Welcome to Army Asset Lifecycle Management System"
    }


@app.get("/health")
def health_check():
    return {
        "status": "Healthy",
        "application": "AALMS"
    }


@app.get("/db-test")
def db_test():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {
            "database": "Connected Successfully"
        }

    except Exception as e:
        return {
            "database": "Connection Failed",
            "error": str(e)
        }