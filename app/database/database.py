from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from .base import Base
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Garanta que as tabelas sejam criadas
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_prompt_template(db: Session, prompt_name: str):
    """
    Busca um template de prompt no banco de dados.

    Args:
        db: A sessão do banco de dados.
        prompt_name: O nome do prompt a ser buscado.

    Returns:
        O template do prompt (um dicionário) ou None se não for encontrado.
    """
    query = text("SELECT system, user, assistant FROM public.prompts WHERE name = :prompt_name")
    result = db.execute(query, {"prompt_name": prompt_name}).fetchone()

    if result:
        return {
            "system": result[0],
            "user": result[1],
            "assistant": result[2]
        }
    else:
        return None
