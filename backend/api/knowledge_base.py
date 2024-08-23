# backend/api/knowledge_base.py
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from ..models.knowledge_base import KnowledgeBaseCreate, KnowledgeBaseInDB
from ..crud import knowledge_base
from typing import List
from fastapi.responses import StreamingResponse
import io

router = APIRouter()

@router.post("/", response_model=KnowledgeBaseInDB)
async def create_knowledge_base(
    kb: KnowledgeBaseCreate = Depends(),
    file: UploadFile = File(...)
):
    content = await file.read()
    return knowledge_base.create_knowledge_base(kb, content)

@router.get("/{assistant_id}", response_model=List[KnowledgeBaseInDB])
def read_knowledge_base(assistant_id: str):
    return knowledge_base.get_knowledge_base(assistant_id)

@router.get("/content/{kb_id}")
def read_knowledge_base_content(kb_id: str):
    content = knowledge_base.get_knowledge_base_content(kb_id)
    if content is None:
        raise HTTPException(status_code=404, detail="Knowledge base entry not found")
    return StreamingResponse(io.BytesIO(content), media_type="application/octet-stream")

@router.delete("/{kb_id}")
def delete_knowledge_base(kb_id: str):
    if not knowledge_base.delete_knowledge_base(kb_id):
        raise HTTPException(status_code=404, detail="Knowledge base entry not found")
    return {"detail": "Knowledge base entry deleted"}