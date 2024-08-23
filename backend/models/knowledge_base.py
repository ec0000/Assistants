# backend/models/knowledge_base.py
from pydantic import BaseModel
from typing import Optional

class KnowledgeBaseBase(BaseModel):
    assistant_id: str
    file_name: str

class KnowledgeBaseCreate(KnowledgeBaseBase):
    pass

class KnowledgeBaseInDB(KnowledgeBaseBase):
    kb_id: str
    created_by: str
    created_date: str