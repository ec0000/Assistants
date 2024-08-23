# tests/test_api_assistants.py

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import get_db

client = TestClient(app)

TEST_PREFIX = "TEST_API_"

@pytest.fixture(scope="module", autouse=True)
def cleanup_database():
    # Clean up before tests
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM assistants WHERE assistant_name LIKE '{TEST_PREFIX}%'")
        conn.commit()
    yield
    # Clean up after tests
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM assistants WHERE assistant_name LIKE '{TEST_PREFIX}%'")
        conn.commit()

def create_test_assistant(name_suffix=""):
    response = client.post(
        "/assistants/",
        json={"assistant_name": f"{TEST_PREFIX}Test Assistant API {name_suffix}", "role": "Test Role API", "system_prompt": "Test Prompt API"}
    )
    assert response.status_code == 200, f"Failed to create assistant. Response: {response.content}"
    data = response.json()
    assert "assistant_id" in data, f"assistant_id not found in response: {data}"
    return data["assistant_id"]

def test_1_create_assistant():
    assistant_id = create_test_assistant("1")
    assert assistant_id is not None

def test_2_read_single_assistant():
    assistant_id = create_test_assistant("2")
    response = client.get(f"/assistants/{assistant_id}")
    assert response.status_code == 200, f"Failed to get assistant. Response: {response.content}"
    data = response.json()
    assert data["assistant_name"].startswith(TEST_PREFIX), f"Unexpected assistant name: {data['assistant_name']}"
    assert data["role"] == "Test Role API", f"Unexpected role: {data['role']}"
    assert data["system_prompt"] == "Test Prompt API", f"Unexpected system prompt: {data['system_prompt']}"

def test_3_read_all_assistants():
    # Create two more assistants
    create_test_assistant("3a")
    create_test_assistant("3b")
    
    response = client.get("/assistants/")
    assert response.status_code == 200, f"Failed to get assistants. Response: {response.content}"
    data = response.json()
    assert isinstance(data, list), f"Expected a list, got: {type(data)}"
    test_assistants = [a for a in data if a["assistant_name"].startswith(TEST_PREFIX)]
    assert len(test_assistants) >= 3, f"Expected at least 3 test assistants, found: {len(test_assistants)}"

def test_4_update_assistant():
    assistant_id = create_test_assistant("4")
    update_data = {
        "assistant_name": f"{TEST_PREFIX}Updated Assistant API",
        "role": "Updated Role API",
        "system_prompt": "Updated Prompt API"
    }
    response = client.put(f"/assistants/{assistant_id}", json=update_data)
    assert response.status_code == 200, f"Failed to update assistant. Response: {response.content}"
    data = response.json()
    assert data["assistant_name"] == f"{TEST_PREFIX}Updated Assistant API", f"Name not updated: {data['assistant_name']}"
    assert data["role"] == "Updated Role API", f"Role not updated: {data['role']}"
    assert data["system_prompt"] == "Updated Prompt API", f"System prompt not updated: {data['system_prompt']}"

def test_5_delete_assistant():
    assistant_id = create_test_assistant("5")
    response = client.delete(f"/assistants/{assistant_id}")
    assert response.status_code == 200, f"Failed to delete assistant. Response: {response.content}"
    assert response.json() == {"detail": "Assistant deleted"}
    
    # Verify that the assistant is deleted
    get_response = client.get(f"/assistants/{assistant_id}")
    assert get_response.status_code == 404, f"Assistant not deleted. Response: {get_response.content}"

def test_6_create_duplicate_assistant():
    assistant_name = f"{TEST_PREFIX}Duplicate Assistant API"
    # Create first assistant
    response1 = client.post(
        "/assistants/",
        json={"assistant_name": assistant_name, "role": "Test Role API", "system_prompt": "Test Prompt API"}
    )
    assert response1.status_code == 200

    # Try to create duplicate
    response2 = client.post(
        "/assistants/",
        json={"assistant_name": assistant_name, "role": "Another Role API", "system_prompt": "Another Prompt API"}
    )
    assert response2.status_code == 400
    assert "already exists" in response2.json()["detail"]

def test_7_read_non_existent_assistant():
    response = client.get("/assistants/non_existent_id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Assistant not found"}

def test_8_update_non_existent_assistant():
    response = client.put(
        "/assistants/non_existent_id",
        json={"assistant_name": f"{TEST_PREFIX}Non-existent Assistant", "role": "Non-existent Role", "system_prompt": "Non-existent Prompt"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Assistant not found"}

def test_9_delete_non_existent_assistant():
    response = client.delete("/assistants/non_existent_id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Assistant not found"}