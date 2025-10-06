from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

import os
import alembic.config


_ = load_dotenv()

# --- Database Configuration ---
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://user:password@db:5432/fastapi_db"
)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()  # This will be replaced by models.Base eventually


# --- Alembic Autostart Migration ---
def run_migrations():
    """Runs Alembic migrations at application startup."""
    print("Attempting to run Alembic migrations...")
    try:
        alembic_args = [
            "-c",
            "/app/alembic.ini",  # Path to alembic.ini from Docker WORKDIR /app
            "upgrade",
            "head",
        ]
        alembic.config.main(argv=alembic_args)
        print("Alembic migrations applied successfully.")
    except Exception as e:
        print(f"Error applying Alembic migrations: {e}")
        # Depending on criticality, you might want to re-raise the exception or log it more severely
        # For now, we'll let the app try to start, but migrations are crucial.


# --- Dependency to get DB session ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- FastAPI Application Instance ---
app = FastAPI(
    title="SchedulerCreator API",
    description="API for managing schedules and events.",
    version="0.1.0",
)


# --- Startup Event ---
@app.on_event("startup")
async def startup_event():
    print("Application startup event triggered.")
    run_migrations()
    # In a real application, you might also create initial data or perform other setup here.

    return {"message": "This is a placeholder for items from the database."}


# You would import and include routers for users, schedules, events here
# e.g., from .routers import users, schedules, events
# app.include_router(users.router)
# app.include_router(schedules.router)
# app.include_router(events.router)
