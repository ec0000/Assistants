# tests/test_webhooks.py

import pytest
import sqlite3
from contextlib import contextmanager
from backend.models.webhook import WebhookBase, WebhookCreate, WebhookUpdate, WebhookInDB
from backend.crud import webhooks

# Setup a test database
@pytest.fixture(scope="module")
def test_db():
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    
    conn.execute('''
    CREATE TABLE webhooks (
        webhook_id TEXT PRIMARY KEY,
        assistant_id TEXT NOT NULL,
        whatsapp_number TEXT NOT NULL,
        webhook_url TEXT NOT NULL,
        enabled BOOLEAN NOT NULL,
        created_by TEXT NOT NULL,
        created_date TEXT NOT NULL
    )
    ''')
    
    yield conn
    conn.close()

# Mock the get_db function
@pytest.fixture(autouse=True)
def mock_get_db(test_db, monkeypatch):
    @contextmanager
    def mock_get_db():
        yield test_db
    monkeypatch.setattr("backend.crud.webhooks.get_db", mock_get_db)

# Test creating a webhook
def test_create_webhook():
    webhook = WebhookCreate(
        assistant_id="test_assistant_id",
        whatsapp_number="+1234567890",
        webhook_url="https://example.com/webhook",
        enabled=True
    )
    created = webhooks.create_webhook(webhook)
    assert created.assistant_id == "test_assistant_id"
    assert created.whatsapp_number == "+1234567890"
    assert created.webhook_url == "https://example.com/webhook"
    assert created.enabled == True

# Test getting all webhooks for an assistant
def test_get_webhooks():
    all_webhooks = webhooks.get_webhooks("test_assistant_id")
    assert len(all_webhooks) == 1
    assert all_webhooks[0].assistant_id == "test_assistant_id"

# Test getting a specific webhook
def test_get_webhook():
    all_webhooks = webhooks.get_webhooks("test_assistant_id")
    webhook_id = all_webhooks[0].webhook_id
    webhook = webhooks.get_webhook(webhook_id)
    assert webhook.assistant_id == "test_assistant_id"
    assert webhook.whatsapp_number == "+1234567890"

# Test updating a webhook
def test_update_webhook():
    all_webhooks = webhooks.get_webhooks("test_assistant_id")
    webhook_id = all_webhooks[0].webhook_id
    update_data = WebhookUpdate(
        whatsapp_number="+9876543210",
        webhook_url="https://example.com/updated",
        enabled=False
    )
    updated = webhooks.update_webhook(webhook_id, update_data)
    assert updated.whatsapp_number == "+9876543210"
    assert updated.webhook_url == "https://example.com/updated"
    assert updated.enabled == False

# Test deleting a webhook
def test_delete_webhook():
    all_webhooks = webhooks.get_webhooks("test_assistant_id")
    webhook_id = all_webhooks[0].webhook_id
    deleted = webhooks.delete_webhook(webhook_id)
    assert deleted == True
    remaining = webhooks.get_webhooks("test_assistant_id")
    assert len(remaining) == 0

# Test getting a non-existent webhook
def test_get_non_existent_webhook():
    non_existent_id = "non_existent_id"
    webhook = webhooks.get_webhook(non_existent_id)
    assert webhook is None

# Test updating a non-existent webhook
def test_update_non_existent_webhook():
    non_existent_id = "non_existent_id"
    update_data = WebhookUpdate(
        whatsapp_number="+1111111111",
        webhook_url="https://example.com/nonexistent",
        enabled=True
    )
    updated = webhooks.update_webhook(non_existent_id, update_data)
    assert updated is None

# Test deleting a non-existent webhook
def test_delete_non_existent_webhook():
    non_existent_id = "non_existent_id"
    deleted = webhooks.delete_webhook(non_existent_id)
    assert deleted == False