# tests/test_api_knowledge_base.py

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import get_db
import io

client = TestClient(app)

TEST_PREFIX = "TEST_API_KB_"

@pytest.fixture(scope="module", autouse=True)

def cleanup_database():
    # Clean up before tests
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM knowledge_base WHERE file_name LIKE '{TEST_PREFIX}%'")
        conn.commit()
    yield
    # Clean up after tests
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM knowledge_base WHERE file_name LIKE '{TEST_PREFIX}%'")
        conn.commit() 


def create_test_assistant():
    response = client.post(
        "/assistants/",
        json={"assistant_name": f"{TEST_PREFIX}Assistant", "role": "Test Role", "system_prompt": "Test Prompt"}
    )
    assert response.status_code == 200
    return response.json()["assistant_id"]

def create_test_knowledge_base(assistant_id, name_suffix=""):
    file_content = f"This is a test content for {name_suffix}".encode()
    file = io.BytesIO(file_content)
    response = client.post(
        "/knowledge-base/",
        data={"assistant_id": assistant_id},
        files={"file": (f"{TEST_PREFIX}test_file{name_suffix}.txt", file, "text/plain")}
    )
    assert response.status_code == 200, f"Failed to create knowledge base entry. Response: {response.content}"
    data = response.json()
    assert "kb_id" in data, f"kb_id not found in response: {data}"
    return data["kb_id"]

def test_1_create_knowledge_base():
    assistant_id = create_test_assistant()
    kb_id = create_test_knowledge_base(assistant_id, "1")
    assert kb_id is not None

def test_2_read_knowledge_base():
    assistant_id = create_test_assistant()
    create_test_knowledge_base(assistant_id, "2a")
    create_test_knowledge_base(assistant_id, "2b")
    
    response = client.get(f"/knowledge-base/{assistant_id}")
    assert response.status_code == 200, f"Failed to get knowledge base entries. Response: {response.content}"
    data = response.json()
    assert isinstance(data, list), f"Expected a list, got: {type(data)}"
    test_entries = [kb for kb in data if kb["file_name"].startswith(TEST_PREFIX)]
    assert len(test_entries) >= 2, f"Expected at least 2 test entries, found: {len(test_entries)}"

def test_3_read_knowledge_base_content():
    assistant_id = create_test_assistant()
    kb_id = create_test_knowledge_base(assistant_id, "3")
    
    response = client.get(f"/knowledge-base/content/{kb_id}")
    assert response.status_code == 200, f"Failed to get knowledge base content. Response: {response.content}"
    assert response.content.startswith(b"This is a test content for 3")

def test_4_delete_knowledge_base():
    assistant_id = create_test_assistant()
    kb_id = create_test_knowledge_base(assistant_id, "4")
    
    response = client.delete(f"/knowledge-base/{kb_id}")
    assert response.status_code == 200, f"Failed to delete knowledge base entry. Response: {response.content}"
    assert response.json() == {"detail": "Knowledge Base entry deleted"}
    
    # Verify that the entry is deleted
    get_response = client.get(f"/knowledge-base/content/{kb_id}")
    assert get_response.status_code == 404, f"Knowledge base entry not deleted. Response: {get_response.content}"

def test_5_create_duplicate_knowledge_base():
    assistant_id = create_test_assistant()
    file_name = f"{TEST_PREFIX}duplicate_test_file.txt"
    file_content = "This is a test content".encode()
    file = io.BytesIO(file_content)
    
    # Create first entry
    response1 = client.post(
        "/knowledge-base/",
        data={"assistant_id": assistant_id},
        files={"file": (file_name, file, "text/plain")}
    )
    assert response1.status_code == 200

    # Try to create duplicate
    file.seek(0)  # Reset file pointer
    response2 = client.post(
        "/knowledge-base/",
        data={"assistant_id": assistant_id},
        files={"file": (file_name, file, "text/plain")}
    )
    assert response2.status_code == 400
    assert "already exists" in response2.json()["detail"]

def test_6_read_non_existent_knowledge_base():
    response = client.get("/knowledge-base/content/non_existent_id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Knowledge Base entry not found"}

def test_7_delete_non_existent_knowledge_base():
    response = client.delete("/knowledge-base/non_existent_id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Knowledge Base entry not found"}