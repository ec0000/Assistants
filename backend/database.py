# app/database.py

import os
from contextlib import contextmanager
import sqlite3

# Get the current directory of the database.py file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create a 'data' directory if it doesn't exist
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# Set the database file path
DATABASE_PATH = os.path.join(DATA_DIR, 'assistants.db')

@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        conn.executescript('''
        -- Create the Assistant table
        CREATE TABLE IF NOT EXISTS assistants (
            assistant_id TEXT PRIMARY KEY,
            assistant_name TEXT NOT NULL UNIQUE,
            created_by TEXT NOT NULL,
            modified_by TEXT NOT NULL,
            role TEXT NOT NULL,
            system_prompt TEXT NOT NULL,
            created_date TEXT NOT NULL,
            last_modified_date TEXT NOT NULL
        );

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

        -- Create the webhook table
        CREATE TABLE IF NOT EXISTS webhooks (
            webhook_id TEXT PRIMARY KEY,
            assistant_id TEXT NOT NULL,
            whatsapp_number TEXT NOT NULL,
            webhook_url TEXT NOT NULL,
            enabled BOOLEAN NOT NULL, 
            created_by TEXT NOT NULL,
            created_date TEXT NOT NULL,
            FOREIGN KEY (assistant_id) REFERENCES assistants (assistant_id) ON DELETE CASCADE
        );

        -- Create an index on assistant_name for faster lookups
        CREATE INDEX IF NOT EXISTS idx_assistant_name ON assistants (assistant_name);

        -- Create an index on created_date for sorting
        CREATE INDEX IF NOT EXISTS idx_created_date ON assistants (created_date);

        -- Create an index on the assistant_id in the knowledge_base table for faster lookups
        CREATE INDEX IF NOT EXISTS idx_kb_assistant_id ON knowledge_base (assistant_id);

        -- Create a unique index on assistant_id and file_name in the knowledge_base table
        CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_kb_file_name ON knowledge_base (assistant_id, file_name);

        -- Create an index on the assistant_id in the webhooks table for faster lookups
        CREATE INDEX IF NOT EXISTS idx_webhook_assistant_id ON webhooks (assistant_id);
        ''')
        conn.commit()

# Call init_db() when the application starts
init_db()