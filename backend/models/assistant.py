# backend/models/assistant.py
from pydantic import BaseModel
from typing import Optional

class AssistantBase(BaseModel):
    assistant_name: str
    role: str
    system_prompt: str

class AssistantCreate(AssistantBase):
    pass

class AssistantUpdate(BaseModel):
    assistant_name: Optional[str] = None
    role: Optional[str] = None
    system_prompt: Optional[str] = None

class AssistantInDB(AssistantBase):
    assistant_id: str
    created_by: str
    modified_by: str
    created_date: str
    last_modified_date: str