# backend/api/webhooks.py
from fastapi import APIRouter, HTTPException
from ..models.webhook import WebhookCreate, WebhookUpdate, WebhookInDB
from ..crud import webhooks
from typing import List

router = APIRouter()

@router.post("/", response_model=WebhookInDB)
def create_webhook(webhook: WebhookCreate):
    return webhooks.create_webhook(webhook)

@router.get("/{assistant_id}", response_model=List[WebhookInDB])
def read_webhooks(assistant_id: str):
    return webhooks.get_webhooks(assistant_id)

@router.get("/{webhook_id}", response_model=WebhookInDB)
def read_webhook(webhook_id: str):
    webhook = webhooks.get_webhook(webhook_id)
    if webhook is None:
        raise HTTPException(status_code=404, detail="Webhook not found")
    return webhook

@router.put("/{webhook_id}", response_model=WebhookInDB)
def update_webhook(webhook_id: str, webhook: WebhookUpdate):
    updated_webhook = webhooks.update_webhook(webhook_id, webhook)
    if updated_webhook is None:
        raise HTTPException(status_code=404, detail="Webhook not found")
    return updated_webhook

@router.delete("/{webhook_id}")
def delete_webhook(webhook_id: str):
    if not webhooks.delete_webhook(webhook_id):
        raise HTTPException(status_code=404, detail="Webhook not found")
    return {"detail": "Webhook deleted"}