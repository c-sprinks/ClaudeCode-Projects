from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import text
from config.database import get_db, engine
from app.models import Base
from app.routes import conversations, users, jobs, equipment, solutions, companies

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="AIBrainFrame API",
    description="AI-powered field technician support system for Fire Alarm, Access Control, Networking, and Cyber-security",
    version="1.0.0"
)

# CORS middleware for web interface
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="assets"), name="static")

# Include routers
app.include_router(conversations.router)
app.include_router(users.router)
app.include_router(jobs.router)
app.include_router(equipment.router)
app.include_router(solutions.router)
app.include_router(companies.router)

@app.get("/")
async def root():
    from fastapi.responses import FileResponse
    return FileResponse("simple_lbob.html")

@app.get("/api")
async def api_root():
    return {
        "message": "AIBrainFrame API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Test database connection with SQLite compatible query
        result = db.execute(text("SELECT 1 as test")).fetchone()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)