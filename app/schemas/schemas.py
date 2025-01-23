from pydantic import BaseModel


class Prompt(BaseModel):
    name: str
    system: str
    user: str
    assistant: str

    class Config:
        from_attributes = True


class Epic(BaseModel):
    description: str


class WbsItem(BaseModel):
    description: str


class Feature(BaseModel):
    epic_id: int
    description: str


class UserStory(BaseModel):
    feature_id: int
    user_type: str
    goal: str
    reason: str


class Task(BaseModel):
    user_story_id: int
    description: str
