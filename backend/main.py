# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import assistants, webhooks, knowledge_base
from .database import init_db
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:8080",  # Vue.js default dev server
    "http://localhost:3000",  # In case you're using a different port
    # Add any other origins (frontend URLs) you want to allow
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.on_event("startup")
async def startup_event():
    init_db()

# Include routers 
app.include_router(assistants.router, prefix="/assistants", tags=["assistants"])
app.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
app.include_router(knowledge_base.router, prefix="/knowledge-base", tags=["knowledge-base"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)