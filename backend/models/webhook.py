# backend/models/webhook.py
from pydantic import BaseModel
from typing import Optional

class WebhookBase(BaseModel):
    assistant_id: str
    whatsapp_number: str
    webhook_url: str
    enabled: bool

class WebhookCreate(WebhookBase):
    pass

class WebhookUpdate(BaseModel):
    whatsapp_number: Optional[str] = None
    webhook_url: Optional[str] = None
    enabled: Optional[bool] = None

class WebhookInDB(WebhookBase):
    webhook_id: str
    created_by: str
    created_date: str