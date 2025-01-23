from app.core.llm_service import LLMService
from app.database.database import get_db
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.models import Prompt


def generate_feature(epic_description: str, db: Session = Depends(get_db)) -> str:
    """
    Gera uma Feature com base na descrição do Épico.

    Args:
        epic_description: A descrição do Épico.
        db: A sessão do banco de dados.

    Returns:
        A Feature gerada pela IA.
    """
    llm_service = LLMService(db)
    prompt_template = llm_service.db_session.query(Prompt).filter(Prompt.name == "feature_prompt").first()

    if not prompt_template:
        raise HTTPException(status_code=500, detail=f"Template de prompt 'feature_prompt' não encontrado.")

    prompt = prompt_template.user.replace("{epic_description}", epic_description)

    feature_text = llm_service.generate_text({
        "system": prompt_template.system,
        "user": prompt,
        "assistant": prompt_template.assistant
    })
    return feature_text
