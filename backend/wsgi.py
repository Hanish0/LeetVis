"""
WSGI configuration for PythonAnywhere deployment
"""
from main import app

# PythonAnywhere expects 'application' variable
application = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)