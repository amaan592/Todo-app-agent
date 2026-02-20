from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import tasks
from src.api import agent

app = FastAPI(title="Todo API", version="1.0.0")

# CORS middleware - allowing all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(tasks.router, prefix="/api/v1", tags=["tasks"])
app.include_router(agent.router, prefix="/api/v1", tags=["agent"])

@app.get("/")
def read_root():
    return {"message": "Todo API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)