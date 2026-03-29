"""
ASGI entrypoint — used by `uvicorn app.server:app`.

This file exists so the ASGI server has a simple import target
while the actual app construction lives in main.py.
"""

from app.main import create_app

app = create_app()
