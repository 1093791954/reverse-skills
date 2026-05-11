"""Tiny launcher.  Drop into each <site>/ directory.

Then either:
    python run.py
or double-click start.bat (which calls this).
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8888, reload=False)
