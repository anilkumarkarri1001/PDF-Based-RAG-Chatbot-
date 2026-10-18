from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI()

# Import routers
from routers import upload, ask

# Include routers
app.include_router(upload.router)
app.include_router(ask.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG API with Gemini"}