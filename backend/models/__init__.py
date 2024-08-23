# backend/models/__init__.py
from .assistant import AssistantBase, AssistantCreate, AssistantUpdate, AssistantInDB
from .knowledge_base import KnowledgeBaseBase, KnowledgeBaseCreate, KnowledgeBaseInDB
from .webhook import WebhookBase, WebhookCreate, WebhookUpdate, WebhookInDB