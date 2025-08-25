from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings

from routers import story, job

from db.database import create_tables

import logging

create_tables()



# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(asctime)s - %(name)s  - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

app = FastAPI(
    title="Play with LLMs",
    description="An application to experiment with Large Language Models (LLMs) and their capabilities.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact= {
        "name": "Nadeeka Dilhan",
        "email": "nadeekaxdilhan@gmail.com",
        "url": "https://github.com/Nadee95/"
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(story.router, prefix=settings.API_PREFIX)
app.include_router(job.router, prefix=settings.API_PREFIX)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)




