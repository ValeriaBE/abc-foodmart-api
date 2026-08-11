from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.dashboard import router as dashboard_router


app = FastAPI(
    title="ABC Foodmart API",
    description="Analytics API for the ABC Foodmart dashboard",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://valeriabe.github.io/"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(dashboard_router)


@app.get("/")
def root():
    return {
        "message": "ABC Foodmart API",
        "docs": "/docs",
    }