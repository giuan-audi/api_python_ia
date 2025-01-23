from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database.models import Prompt
from app.schemas.schemas import Prompt as PromptSchema

router = APIRouter()


@router.post("/prompts/", response_model=PromptSchema)
def create_prompt(prompt: PromptSchema, db: Session = Depends(get_db)):
    db_prompt = Prompt(**prompt.dict())
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt


@router.get("/prompts/{prompt_id}", response_model=PromptSchema)
def read_prompt(prompt_id: int, db: Session = Depends(get_db)):
    db_prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if db_prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return db_prompt


@router.get("/prompts/", response_model=list[PromptSchema])
def read_prompts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    prompts = db.query(Prompt).offset(skip).limit(limit).all()
    return prompts


@router.put("/prompts/{prompt_id}", response_model=PromptSchema)
def update_prompt(prompt_id: int, prompt: PromptSchema, db: Session = Depends(get_db)):
    db_prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if db_prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")

    for key, value in prompt.dict().items():
        setattr(db_prompt, key, value)

    db.commit()
    db.refresh(db_prompt)
    return db_prompt


@router.delete("/prompts/{prompt_id}")
def delete_prompt(prompt_id: int, db: Session = Depends(get_db)):
    db_prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if db_prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")

    db.delete(db_prompt)
    db.commit()
    return {"message": "Prompt deleted"}
