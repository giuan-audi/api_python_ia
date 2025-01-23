from app.core.llm_service import LLMService
from app.database.database import get_db
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.models import Prompt


def generate_user_story(feature_description: str, db: Session = Depends(get_db)) -> str:
    """
    Gera uma História de Usuário com base na descrição da feature.

    Args:
        feature_description: A descrição da feature.
        db: A sessão do banco de dados.

    Returns:
        A História de Usuário gerada pela IA.
    """
    llm_service = LLMService(db)
    prompt_template = llm_service.db_session.query(Prompt).filter(Prompt.name == "user_story_prompt").first()

    if not prompt_template:
        raise HTTPException(status_code=500, detail=f"Template de prompt 'user_story_prompt' não encontrado.")

    prompt = prompt_template.user.replace("{feature_description}", feature_description)

    user_story_text = llm_service.generate_text({
        "system": prompt_template.system,
        "user": prompt,
        "assistant": prompt_template.assistant
    })
    return user_story_text
