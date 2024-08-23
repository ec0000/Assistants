# tests/test_assistants.py

import pytest
import sqlite3
from contextlib import contextmanager
from backend.models.assistant import AssistantBase, AssistantCreate, AssistantUpdate, AssistantInDB
from backend.crud import assistants
from backend.crud.assistants import DuplicateAssistantError

# Setup a test database
@pytest.fixture(scope="module")
def test_db():
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    
    conn.execute('''
    CREATE TABLE assistants (
        assistant_id TEXT PRIMARY KEY,
        assistant_name TEXT NOT NULL UNIQUE,
        created_by TEXT NOT NULL,
        modified_by TEXT NOT NULL,
        role TEXT NOT NULL,
        system_prompt TEXT NOT NULL,
        created_date TEXT NOT NULL,
        last_modified_date TEXT NOT NULL
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
    monkeypatch.setattr("backend.crud.assistants.get_db", mock_get_db)

# 1. Empty the database (this is implicitly done by using a new in-memory database for each test run)

# 2. Add one record
def test_create_assistant():
    assistant = AssistantCreate(
        assistant_name="Test Assistant 1",
        role="Test Role 1",
        system_prompt="Test Prompt 1"
    )
    created = assistants.create_assistant(assistant)
    assert created.assistant_name == "Test Assistant 1"
    assert created.role == "Test Role 1"
    assert created.system_prompt == "Test Prompt 1"

# 3. Retrieve one record
def test_get_one_assistant():
    all_assistants = assistants.get_assistants()
    assert len(all_assistants) == 1
    assert all_assistants[0].assistant_name == "Test Assistant 1"

# 4. Add another record
def test_create_another_assistant():
    assistant = AssistantCreate(
        assistant_name="Test Assistant 2",
        role="Test Role 2",
        system_prompt="Test Prompt 2"
    )
    created = assistants.create_assistant(assistant)
    assert created.assistant_name == "Test Assistant 2"

# 5. Retrieve all records
def test_get_all_assistants():
    all_assistants = assistants.get_assistants()
    assert len(all_assistants) == 2
    assert any(a.assistant_name == "Test Assistant 1" for a in all_assistants)
    assert any(a.assistant_name == "Test Assistant 2" for a in all_assistants)

# 6. Delete one record
def test_delete_assistant():
    all_assistants = assistants.get_assistants()
    assistant_to_delete = next(a for a in all_assistants if a.assistant_name == "Test Assistant 1")
    deleted = assistants.delete_assistant(assistant_to_delete.assistant_id)
    assert deleted == True

# 7. Retrieve the records, there should only be one
def test_get_remaining_assistant():
    remaining = assistants.get_assistants()
    assert len(remaining) == 1
    assert remaining[0].assistant_name == "Test Assistant 2"

# Additional tests for edge cases

def test_create_duplicate_assistant():
    assistant = AssistantCreate(
        assistant_name="Test Assistant 2",  # This name already exists
        role="Duplicate Role",
        system_prompt="Duplicate Prompt"
    )
    with pytest.raises(DuplicateAssistantError) as exc_info:
        assistants.create_assistant(assistant)
    assert "already exists" in str(exc_info.value)

def test_get_non_existent_assistant():
    non_existent_id = "non_existent_id"
    assistant = assistants.get_assistant(non_existent_id)
    assert assistant is None

def test_update_assistant():
    all_assistants = assistants.get_assistants()
    assistant_id = all_assistants[0].assistant_id
    update_data = AssistantUpdate(
        assistant_name="Updated Assistant",
        role="Updated Role",
        system_prompt="Updated Prompt"
    )
    updated = assistants.update_assistant(assistant_id, update_data)
    assert updated.assistant_name == "Updated Assistant"
    assert updated.role == "Updated Role"
    assert updated.system_prompt == "Updated Prompt"

def test_update_non_existent_assistant():
    non_existent_id = "non_existent_id"
    update_data = AssistantUpdate(
        assistant_name="Non-existent Assistant",
        role="Non-existent Role",
        system_prompt="Non-existent Prompt"
    )
    updated = assistants.update_assistant(non_existent_id, update_data)
    assert updated is None

def test_delete_non_existent_assistant():
    non_existent_id = "non_existent_id"
    deleted = assistants.delete_assistant(non_existent_id)
    assert deleted == False