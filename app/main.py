from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException

from app.api import auth_routes, notes_routes, user_routes
from app.exceptions.exception_handler import http_exception_handler, validation_exception_handler
from contextlib import asynccontextmanager
from app.db.database import create_db_and_tables, close_all_connections

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    close_all_connections()

app = FastAPI(
    title="Notes App",
    description="A secure notes API with login, OTP, and password reset.",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(auth_routes.router)
app.include_router(notes_routes.router)
app.include_router(user_routes.router)  # 👈 Added this line

# Health check
@app.get("/", tags=["Health Check"])
def health_check():
    return {
        "status": "success",
        "message": "Notes API is running",
        "data": None,
        "status_code": 200
    }

# Register exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
