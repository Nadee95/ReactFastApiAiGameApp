import uuid
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks
from sqlalchemy.orm import Session
import logging

from db.database import get_db, SessionLocal
from models.story import Story, StoryNode
from models.job import StoryJob
from schemas.story import (
    CreateStoryRequest,
    CompleteStoryResponse,
    CompleteStoryNodeResponse
)
from schemas.job import StoryJobResponse
from core.story_generator import StoryGenerator

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/stories",
    tags=["stories"],
)


def get_session_id(session_id: Optional[str] = Cookie(None)) -> str:
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id

@router.post("/create", response_model=StoryJobResponse)
def create_story(
    request: CreateStoryRequest,
    background_tasks: BackgroundTasks,
    response: Response,
    session_id: str = Depends(get_session_id),
    db: Session = Depends(get_db)
):
    logger.info(f"Creating story with theme: {request.theme}, session_id: {session_id}")
    response.set_cookie(key=session_id, value=session_id, httponly=True)

    job_id = str(uuid.uuid4())
    job = StoryJob(
        job_id=job_id,
        session_id=session_id,
        theme=request.theme,
        status="pending"
    )

    db.add(job)
    db.commit()

    logger.info(f"Job created successfully. job_id: {job_id}")

    logger.info(f"Adding background task for job_id: {job_id}")
    background_tasks.add_task(generate_story_task, job_id, request.theme, session_id)

    return job

def generate_story_task(job_id: str, theme: str, session_id: str):
    logger.info(f"Starting story generation task. job_id: {job_id}, theme: {theme}")
    db = SessionLocal()
    try:
        job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()
        if not job:
            logger.error(f"Job not found: {job_id}")
            return

        try:
            logger.info(f"Setting job status to processing: {job_id}")
            job.status = "processing"
            db.commit()

            story = StoryGenerator.generate_story(db, session_id, theme)
            logger.info(f"Story generated successfully. story_id: {story.id}, job_id: {job_id}")

            job.story_id = story.id
            job.status = "completed"
            job.completed_at = datetime.now()
            db.commit()
            logger.info(f"Job marked as completed: {job_id}")

        except Exception as e:
            logger.error(f"Failed to generate story: {str(e)}", exc_info=True)
            job.status = "failed"
            job.completed_at = datetime.now()
            job.error = str(e)
            db.commit()
    finally:
        logger.debug(f"Database session closed for job: {job_id}")
        db.close()

@router.get("/{story_id}/complete", response_model=CompleteStoryResponse)
def get_complete_story(
    story_id: int,
    db: Session = Depends(get_db)
):
    logger.info(f"Fetching complete story: {story_id}")
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        logger.warning(f"Story not found: {story_id}")
        raise HTTPException(status_code=404, detail="Story not found")

    logger.debug(f"Building complete story tree for story: {story_id}")
    complete_story = build_complete_story_tree(db, story)
    logger.info(f"Complete story returned: {story_id}")
    return complete_story

def build_complete_story_tree(db: Session, story: Story) -> CompleteStoryResponse:
    logger.debug(f"Querying story nodes for story_id: {story.id}")
    nodes = db.query(StoryNode).filter(StoryNode.story_id == story.id).all()
    logger.debug(f"Found {len(nodes)} nodes for story_id: {story.id}")

    node_dict = {}
    for node in nodes:
        node_response = CompleteStoryNodeResponse(
            id=node.id,
            content=node.content,
            is_ending=node.is_ending,
            is_winning_ending=node.is_winning_ending,
            options=node.options
        )
        node_dict[node.id] = node_response

    root_node = next((node for node in nodes if node.is_root), None)
    if not root_node:
        logger.error(f"Root node not found for story_id: {story.id}")
        raise HTTPException(status_code=500, detail="Story root node not found")

    logger.debug(f"Complete story tree built successfully for story_id: {story.id}")
    return CompleteStoryResponse(
        id=story.id,
        title= story.title,
        session_id=story.session_id,
        created_at=story.created_at,
        root_node=node_dict[root_node.id],
        all_nodes=node_dict
    )

