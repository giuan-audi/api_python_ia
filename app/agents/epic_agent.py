from app.core.llm_service import LLMService
from app.database.database import get_db
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.models import Prompt


def generate_epic(dialog: str, db: Session = Depends(get_db)) -> str:
    """
    Gera um Épico com base no diálogo fornecido.

    Args:
        dialog: O texto do diálogo inicial.
        db: A sessão do banco de dados.

    Returns:
        O Épico gerado pela IA.
    """
    llm_service = LLMService(db)
    prompt_template = llm_service.db_session.query(Prompt).filter(Prompt.name == "epic_prompt").first()

    if not prompt_template:
        raise HTTPException(status_code=500, detail=f"Template de prompt 'epic_prompt' não encontrado.")

    prompt = prompt_template.user.replace("{dialog}", dialog)

    epic_text = llm_service.generate_text({
        "system": prompt_template.system,
        "user": prompt,
        "assistant": prompt_template.assistant
    })
    return epic_text
