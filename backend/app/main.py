"""
Smart Expense Category Prediction & Financial Analytics
FastAPI Backend Application
"""

import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

from backend.app.api.auth import router as auth_router
from backend.app.api.predict import router as predict_router
from backend.app.api.expenses import router as expenses_router
from backend.app.api.income import router as income_router
from backend.app.api.analytics import router as analytics_router
from backend.app.api.model_comparison import router as model_comparison_router
from backend.app.api.categories import router as categories_router
from backend.app.api.health import router as health_router
from backend.app.ml.model_loader import ml_manager

app = FastAPI(
    title="Smart Expense Category Prediction & Financial Analytics API",
    description="Real ML Expense Classification (Proposed Hybrid Model) and Financial Analytics API backed by Oracle Database 21c",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins including localhost:5173
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global safe exception handler: Friendly message, no stack trace or secrets exposed
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log internally
    print(f"[ERROR] {request.method} {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred. Please verify database connectivity and inputs."}
    )

# Include API Routers under /api/v1
api_v1_prefix = "/api/v1"
app.include_router(auth_router, prefix=api_v1_prefix)
app.include_router(predict_router, prefix=api_v1_prefix)
app.include_router(expenses_router, prefix=api_v1_prefix)
app.include_router(income_router, prefix=api_v1_prefix)
app.include_router(analytics_router, prefix=api_v1_prefix)
app.include_router(model_comparison_router, prefix=api_v1_prefix)
app.include_router(categories_router, prefix=api_v1_prefix)
app.include_router(health_router, prefix=api_v1_prefix)


@app.get("/")
def root():
    return {
        "message": "Smart Expense Category Prediction & Financial Analytics API is running.",
        "documentation": "/docs",
        "api_v1": "/api/v1"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
