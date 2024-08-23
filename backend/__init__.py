# backend/__init__.py
# This can be left empty or you can add version information
__version__ = "0.1.0"
from .database import init_db, get_db


# Revised project structure:
# /your_project
#   /backend
#     __init__.py  (new empty file)
#     main.py
#     database.py
#     /models
#       __init__.py
#     /crud
#       __init__.py
#     /api
#       __init__.py
#   /tests
#     __init__.py
#     test_assistants.py