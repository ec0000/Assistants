# backend/crud/knowledge_base.py

import uuid
from datetime import datetime
from backend.models.knowledge_base import KnowledgeBaseCreate, KnowledgeBaseInDB
from backend.database import get_db

def create_knowledge_base(knowledge_base: KnowledgeBaseCreate, content: bytes):
    with get_db() as db:
        cursor = db.cursor()
        kb_id = str(uuid.uuid4())
        current_time = datetime.now().isoformat()
        
        cursor.execute("""
        INSERT INTO knowledge_base (kb_id, assistant_id, file_name, content, created_by, created_date)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (kb_id, knowledge_base.assistant_id, knowledge_base.file_name, content, 
              "system", current_time))
        
        db.commit()
        
        created_kb = cursor.execute("SELECT kb_id, assistant_id, file_name, created_by, created_date FROM knowledge_base WHERE kb_id = ?", (kb_id,)).fetchone()
        return KnowledgeBaseInDB(**dict(created_kb))

def get_knowledge_base(assistant_id: str):
    with get_db() as db:
        cursor = db.cursor()
        kb_entries = cursor.execute("SELECT kb_id, assistant_id, file_name, created_by, created_date FROM knowledge_base WHERE assistant_id = ?", (assistant_id,)).fetchall()
        return [KnowledgeBaseInDB(**dict(kb)) for kb in kb_entries]

def get_knowledge_base_content(kb_id: str):
    with get_db() as db:
        cursor = db.cursor()
        content = cursor.execute("SELECT content FROM knowledge_base WHERE kb_id = ?", (kb_id,)).fetchone()
        return content['content'] if content else None

def delete_knowledge_base(kb_id: str):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("DELETE FROM knowledge_base WHERE kb_id = ?", (kb_id,))
        db.commit()
        return cursor.rowcount > 0