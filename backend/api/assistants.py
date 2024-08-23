# backend/api/assistants.py
import logging
from fastapi import HTTPException, Depends, APIRouter
from backend.crud import assistants
from backend.crud.assistants import DuplicateAssistantError
from backend.models.assistant import AssistantCreate, AssistantInDB, AssistantUpdate
from typing import List

router = APIRouter()

logger = logging.getLogger(__name__)


router = APIRouter()

@router.post("/", response_model=AssistantInDB)
def create_assistant(assistant: AssistantCreate):
    try:
        return assistants.create_assistant(assistant)
    except DuplicateAssistantError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error creating assistant: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@router.get("/", response_model=List[AssistantInDB])
def read_assistants(skip: int = 0, limit: int = 100):
    return assistants.get_assistants(skip, limit)

@router.get("/{assistant_id}", response_model=AssistantInDB)
def read_assistant(assistant_id: str):
    assistant = assistants.get_assistant(assistant_id)
    if assistant is None:
        raise HTTPException(status_code=404, detail="Assistant not found")
    return assistant

@router.put("/{assistant_id}", response_model=AssistantInDB)
def update_assistant(assistant_id: str, assistant: AssistantUpdate):
    updated_assistant = assistants.update_assistant(assistant_id, assistant)
    if updated_assistant is None:
        raise HTTPException(status_code=404, detail="Assistant not found")
    return updated_assistant

@router.delete("/{assistant_id}")
def delete_assistant(assistant_id: str):
    if not assistants.delete_assistant(assistant_id):
        raise HTTPException(status_code=404, detail="Assistant not found")
    return {"detail": "Assistant deleted"}