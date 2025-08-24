import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session

from db.database import get_db
from models.job import StoryJob
from schemas.job import StoryJobResponse

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("/{job_id}", response_model=StoryJobResponse)
def get_job_status(
    job_id: str,
    db: Session = Depends(get_db)
):
    try:
        job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Query error")
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job