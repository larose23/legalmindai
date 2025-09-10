# COPY THESE FILES TO YOUR LOCAL DIRECTORY

## Step 1: Open Cursor on your desktop
Open Cursor and navigate to: `C:\Users\USER\Desktop\legalmind-backend`

## Step 2: Create these NEW files in your local directory:

### File 1: Create `nixpacks.toml`
Create a new file called `nixpacks.toml` and paste this content:
```toml
[phases.setup]
nixPkgs = ["python3", "gcc"]

[phases.install]
cmds = [
    "python -m venv --copies /opt/venv",
    ". /opt/venv/bin/activate && pip install -r requirements.txt"
]

[start]
cmd = "./start.sh"

[variables]
PORT = "5000"
```

### File 2: Create `Procfile`
Create a new file called `Procfile` and paste this content:
```
web: gunicorn --bind 0.0.0.0:$PORT src.main:app
```

### File 3: Create `start.sh`
Create a new file called `start.sh` and paste this content:
```bash
#!/bin/bash

# LegalMind Backend Startup Script for Railway

echo "🚀 Starting LegalMind Backend..."

# Set default port if not provided
export PORT=${PORT:-5000}

# Activate virtual environment if it exists
if [ -d "/opt/venv" ]; then
    source /opt/venv/bin/activate
fi

# Create necessary directories
mkdir -p src/database
mkdir -p legal_vector_db

# Start the application
echo "🌐 Starting Gunicorn on port $PORT..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 src.main:app
```

### File 4: Create `runtime.txt`
Create a new file called `runtime.txt` and paste this content:
```
python-3.11
```

## Step 3: Update existing files

### Update `requirements.txt`
Replace the entire content with:
```
blinker==1.9.0
click==8.2.1
Flask==3.1.1
flask-cors==6.0.0
Flask-SQLAlchemy==3.1.1
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.2
SQLAlchemy==2.0.41
typing_extensions==4.14.0
Werkzeug==3.1.3
gunicorn==21.2.0
openai==1.3.0
chromadb==0.4.15
langchain==0.0.350
langchain-text-splitters==0.0.1
numpy>=1.21.0
```

### Update `src/main.py`
Replace the first 8 lines (the import section) with:
```python
import os
import sys

# Add the project root to Python path for Railway deployment
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from flask import Flask, send_from_directory
```

## Step 4: Commit and Push to GitHub
1. In Cursor, open the terminal (Ctrl+`)
2. Run these commands:
```bash
git add .
git commit -m "Fix Railway deployment - add nixpacks config and start commands"
git push
```

## Step 5: Deploy to Railway
1. Go to your Railway project
2. It should automatically redeploy with the new changes
3. Set environment variables in Railway dashboard:
   - OPENAI_API_KEY=your_openai_api_key_here
   - SECRET_KEY=your_secure_secret_key_here

## That's it! Your deployment should work now! 🚀