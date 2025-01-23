from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.agents import epic_agent, feature_agent, user_story_agent, task_agent
from app.schemas import schemas
from app.core.llm_service import LLMService

router = APIRouter()


@router.post("/epics/")
async def create_epic(epic_request: schemas.Epic, db: Session = Depends(get_db)):
    return epic_agent.generate_epic(epic_request.description, db)


@router.post("/features/")
async def create_feature(feature_request: schemas.Feature, db: Session = Depends(get_db)):
    return feature_agent.generate_feature(feature_request.epic_id, feature_request.description, db)


@router.post("/user_stories/")
async def create_user_story(user_story_request: schemas.UserStory, db: Session = Depends(get_db)):
    return user_story_agent.generate_user_story(user_story_request.feature_id, user_story_request.description, db)


@router.post("/tasks/")
async def create_task(task_request: schemas.Task, db: Session = Depends(get_db)):
    return task_agent.generate_task(task_request.user_story_id, task_request.description, db)
