# tests/test_knowledge_base.py

import pytest
import sqlite3
from contextlib import contextmanager
from backend.models.knowledge_base import KnowledgeBaseCreate, KnowledgeBaseInDB
from backend.crud import knowledge_base

# Setup a test database
@pytest.fixture(scope="module")
def test_db():
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    
    conn.execute('''
        -- Create the KnowledgeBase table
        CREATE TABLE IF NOT EXISTS knowledge_base (
            kb_id TEXT PRIMARY KEY,
            assistant_id TEXT NOT NULL,
            file_name TEXT NOT NULL,
            content BLOB NOT NULL,
            created_by TEXT NOT NULL,
            created_date TEXT NOT NULL,
            FOREIGN KEY (assistant_id) REFERENCES assistants (assistant_id) ON DELETE CASCADE
        );
        ''')
    
    yield conn
    conn.close()

# Mock the get_db function
@pytest.fixture(autouse=True)
def mock_get_db(test_db, monkeypatch):
    @contextmanager
    def mock_get_db():
        yield test_db
    monkeypatch.setattr("backend.crud.knowledge_base.get_db", mock_get_db)

# Test creating a knowledge base entry
def test_create_knowledge_base():
    kb = KnowledgeBaseCreate(
        assistant_id="test_assistant_id",
        file_name="test_file.txt"
    )
    content = b"This is test content"
    created = knowledge_base.create_knowledge_base(kb, content)
    assert created.assistant_id == "test_assistant_id"
    assert created.file_name == "test_file.txt"

# Test getting all knowledge base entries for an assistant
def test_get_knowledge_base():
    kb_entries = knowledge_base.get_knowledge_base("test_assistant_id")
    assert len(kb_entries) == 1
    assert kb_entries[0].assistant_id == "test_assistant_id"
    assert kb_entries[0].file_name == "test_file.txt"

# Test getting content of a specific knowledge base entry
def test_get_knowledge_base_content():
    kb_entries = knowledge_base.get_knowledge_base("test_assistant_id")
    kb_id = kb_entries[0].kb_id
    content = knowledge_base.get_knowledge_base_content(kb_id)
    assert content == b"This is test content"

# Test deleting a knowledge base entry
def test_delete_knowledge_base():
    kb_entries = knowledge_base.get_knowledge_base("test_assistant_id")
    kb_id = kb_entries[0].kb_id
    deleted = knowledge_base.delete_knowledge_base(kb_id)
    assert deleted == True
    remaining = knowledge_base.get_knowledge_base("test_assistant_id")
    assert len(remaining) == 0

# Test getting content of a non-existent knowledge base entry
def test_get_non_existent_knowledge_base_content():
    non_existent_id = "non_existent_id"
    content = knowledge_base.get_knowledge_base_content(non_existent_id)
    assert content is None

# Test deleting a non-existent knowledge base entry
def test_delete_non_existent_knowledge_base():
    non_existent_id = "non_existent_id"
    deleted = knowledge_base.delete_knowledge_base(non_existent_id)
    assert deleted == False

# Test creating multiple knowledge base entries for the same assistant
def test_create_multiple_knowledge_base_entries():
    kb1 = KnowledgeBaseCreate(
        assistant_id="test_assistant_id_2",
        file_name="file1.txt"
    )
    kb2 = KnowledgeBaseCreate(
        assistant_id="test_assistant_id_2",
        file_name="file2.txt"
    )
    content1 = b"Content for file 1"
    content2 = b"Content for file 2"
    
    created1 = knowledge_base.create_knowledge_base(kb1, content1)
    created2 = knowledge_base.create_knowledge_base(kb2, content2)
    
    assert created1.file_name == "file1.txt"
    assert created2.file_name == "file2.txt"
    
    kb_entries = knowledge_base.get_knowledge_base("test_assistant_id_2")
    assert len(kb_entries) == 2