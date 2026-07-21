from app.db.database import Base, engine
import app.models
from fastapi import FastAPI
from sqlalchemy import text

from app.db.database import Base, engine

from app.api.user import router as user_router

app = FastAPI(
    title="Army Asset Lifecycle Management System",
    description="Backend API for Army Inventory Management",
    version="1.0.0",
    debug=True
)

from fastapi import Request

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"REQUEST: {request.method} {request.url}")
    response = await call_next(request)
    print(f"RESPONSE: {response.status_code}")
    return response

app.include_router(user_router)

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