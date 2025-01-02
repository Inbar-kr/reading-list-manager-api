from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    yield
    pass

app = FastAPI(
    title="Reading List Manager API",
    description="API for managing your reading list, tracking progress, and more.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)

# Root health check endpoint
@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the Reading List Manager API!"}

# Run the application directly if executed
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
