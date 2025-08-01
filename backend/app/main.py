from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.api import auth, training_plans

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="AI Training App API",
    description="API for managing user authentication and training plans",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "Operations for user registration and login"
        },
        {
            "name": "Training Plans",
            "description": "Operations for managing user training plans"
        }
    ]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth")
app.include_router(training_plans.router, prefix="/training-plans")

@app.get("/")
async def root():
    return {"message": "AI Training App API"} 