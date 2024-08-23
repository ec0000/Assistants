# backend/crud/webhooks.py

import uuid
from datetime import datetime
from backend.models.webhook import WebhookCreate, WebhookUpdate, WebhookInDB
from backend.database import get_db

def create_webhook(webhook: WebhookCreate):
    with get_db() as db:
        cursor = db.cursor()
        webhook_id = str(uuid.uuid4())
        current_time = datetime.now().isoformat()
        
        cursor.execute("""
        INSERT INTO webhooks (webhook_id, assistant_id, whatsapp_number, webhook_url, enabled, created_by, created_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (webhook_id, webhook.assistant_id, webhook.whatsapp_number, webhook.webhook_url, 
              webhook.enabled, "system", current_time))
        
        db.commit()
        
        created_webhook = cursor.execute("SELECT * FROM webhooks WHERE webhook_id = ?", (webhook_id,)).fetchone()
        return WebhookInDB(**dict(created_webhook))

def get_webhooks(assistant_id: str):
    with get_db() as db:
        cursor = db.cursor()
        webhooks = cursor.execute("SELECT * FROM webhooks WHERE assistant_id = ?", (assistant_id,)).fetchall()
        return [WebhookInDB(**dict(webhook)) for webhook in webhooks]

def get_webhook(webhook_id: str):
    with get_db() as db:
        cursor = db.cursor()
        webhook = cursor.execute("SELECT * FROM webhooks WHERE webhook_id = ?", (webhook_id,)).fetchone()
        return WebhookInDB(**dict(webhook)) if webhook else None

def update_webhook(webhook_id: str, webhook: WebhookUpdate):
    with get_db() as db:
        cursor = db.cursor()
        stored_webhook = cursor.execute("SELECT * FROM webhooks WHERE webhook_id = ?", (webhook_id,)).fetchone()
        if stored_webhook is None:
            return None
        
        update_data = webhook.dict(exclude_unset=True)
        
        update_fields = ", ".join([f"{k} = ?" for k in update_data.keys()])
        update_values = tuple(update_data.values()) + (webhook_id,)
        
        cursor.execute(f"UPDATE webhooks SET {update_fields} WHERE webhook_id = ?", update_values)
        db.commit()
        
        updated_webhook = cursor.execute("SELECT * FROM webhooks WHERE webhook_id = ?", (webhook_id,)).fetchone()
        return WebhookInDB(**dict(updated_webhook))

def delete_webhook(webhook_id: str):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("DELETE FROM webhooks WHERE webhook_id = ?", (webhook_id,))
        db.commit()
        return cursor.rowcount > 0