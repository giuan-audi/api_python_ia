from app.core.llm_service import LLMService
from app.database.database import get_db
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.models import Prompt


def generate_task(user_story_description: str, db: Session = Depends(get_db)) -> str:
    """
    Gera uma Tarefa com base na descrição da História de Usuário.

    Args:
        user_story_description: A descrição da História de Usuário.
        db: A sessão do banco de dados.

    Returns:
        A Tarefa gerada pela IA.
    """
    llm_service = LLMService(db)
    prompt_template = llm_service.db_session.query(Prompt).filter(Prompt.name == "task_prompt").first()

    if not prompt_template:
        raise HTTPException(status_code=500, detail=f"Template de prompt 'task_prompt' não encontrado.")

    prompt = prompt_template.user.replace("{user_story_description}", user_story_description)

    task_text = llm_service.generate_text({
        "system": prompt_template.system,
        "user": prompt,
        "assistant": prompt_template.assistant
    })
    return task_text
