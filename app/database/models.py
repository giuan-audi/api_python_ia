from sqlalchemy import Column, Integer, String, Text
from .base import Base  # Importe Base do arquivo base.py


class Prompt(Base):
    __tablename__ = "prompts"
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    system = Column(Text)
    user = Column(Text)
    assistant = Column(Text)
