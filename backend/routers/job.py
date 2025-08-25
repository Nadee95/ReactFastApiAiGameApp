import uuid
from typing import Optional
import logging
from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session


from db.database import get_db
from models.job import StoryJob
from schemas.job import StoryJobResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("/{job_id}", response_model=StoryJobResponse)
def get_job_status(
    job_id: str,
    db: Session = Depends(get_db)
):
    try:
        job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()
        logger.debug(f"Database query executed for job_id: {job_id}")
    except Exception as e:
        logger.error(f"Database error while fetching job {job_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Query error")
    if not job:
        logger.warning(f"Job not found: {job_id}")
        raise HTTPException(status_code=404, detail="Job not found")
    return job