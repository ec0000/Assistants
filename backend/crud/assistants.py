# app/crud/assistants.py

import uuid
from datetime import datetime
from ..models.assistant import AssistantCreate, AssistantUpdate, AssistantInDB
from ..database import get_db

from sqlite3 import IntegrityError
import logging

logger = logging.getLogger(__name__)

class DuplicateAssistantError(Exception):
    pass

def create_assistant(assistant: AssistantCreate):
    with get_db() as db:
        cursor = db.cursor()
        assistant_id = str(uuid.uuid4())
        current_time = datetime.now().isoformat()
        
        logger.info(f"Inserting assistant into database: {assistant.assistant_name}")
        try:
            cursor.execute("""
            INSERT INTO assistants (assistant_id, assistant_name, role, system_prompt, created_by, modified_by, created_date, last_modified_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (assistant_id, assistant.assistant_name, assistant.role, assistant.system_prompt,
                  "system", "system", current_time, current_time))
            
            db.commit()
            logger.info(f"Assistant inserted successfully: {assistant_id}")
            
            created_assistant = cursor.execute("SELECT * FROM assistants WHERE assistant_id = ?", (assistant_id,)).fetchone()
            return AssistantInDB(**dict(created_assistant))
        except IntegrityError:
            logger.error(f"IntegrityError: Assistant with name '{assistant.assistant_name}' already exists")
            db.rollback()
            raise DuplicateAssistantError(f"Assistant with name '{assistant.assistant_name}' already exists")
        except Exception as e:
            logger.error(f"Unexpected error creating assistant: {str(e)}")
            db.rollback()
            raise

def get_assistants(skip: int = 0, limit: int = 100):
    with get_db() as db:
        cursor = db.cursor()
        assistants = cursor.execute("SELECT * FROM assistants LIMIT ? OFFSET ?", (limit, skip)).fetchall()
        return [AssistantInDB(**dict(assistant)) for assistant in assistants]

def get_assistant(assistant_id: str):
    with get_db() as db:
        cursor = db.cursor()
        assistant = cursor.execute("SELECT * FROM assistants WHERE assistant_id = ?", (assistant_id,)).fetchone()
        return AssistantInDB(**dict(assistant)) if assistant else None

def update_assistant(assistant_id: str, assistant: AssistantUpdate):
    with get_db() as db:
        cursor = db.cursor()
        stored_assistant = cursor.execute("SELECT * FROM assistants WHERE assistant_id = ?", (assistant_id,)).fetchone()
        if stored_assistant is None:
            return None
        
        update_data = assistant.dict(exclude_unset=True)
        update_data["modified_by"] = "system"
        update_data["last_modified_date"] = datetime.now().isoformat()
        
        update_fields = ", ".join([f"{k} = ?" for k in update_data.keys()])
        update_values = tuple(update_data.values()) + (assistant_id,)
        
        cursor.execute(f"UPDATE assistants SET {update_fields} WHERE assistant_id = ?", update_values)
        db.commit()
        
        updated_assistant = cursor.execute("SELECT * FROM assistants WHERE assistant_id = ?", (assistant_id,)).fetchone()
        return AssistantInDB(**dict(updated_assistant))

def delete_assistant(assistant_id: str):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("DELETE FROM assistants WHERE assistant_id = ?", (assistant_id,))
        db.commit()
        return cursor.rowcount > 0