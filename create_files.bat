@echo off
echo Creating Railway deployment files...

REM Create nixpacks.toml
echo [phases.setup] > nixpacks.toml
echo nixPkgs = ["python3", "gcc"] >> nixpacks.toml
echo. >> nixpacks.toml
echo [phases.install] >> nixpacks.toml
echo cmds = [ >> nixpacks.toml
echo     "python -m venv --copies /opt/venv", >> nixpacks.toml
echo     ". /opt/venv/bin/activate && pip install -r requirements.txt" >> nixpacks.toml
echo ] >> nixpacks.toml
echo. >> nixpacks.toml
echo [start] >> nixpacks.toml
echo cmd = "./start.sh" >> nixpacks.toml
echo. >> nixpacks.toml
echo [variables] >> nixpacks.toml
echo PORT = "5000" >> nixpacks.toml

REM Create Procfile
echo web: gunicorn --bind 0.0.0.0:$PORT src.main:app > Procfile

REM Create start.sh
echo #!/bin/bash > start.sh
echo. >> start.sh
echo # LegalMind Backend Startup Script for Railway >> start.sh
echo. >> start.sh
echo echo "🚀 Starting LegalMind Backend..." >> start.sh
echo. >> start.sh
echo # Set default port if not provided >> start.sh
echo export PORT=${PORT:-5000} >> start.sh
echo. >> start.sh
echo # Activate virtual environment if it exists >> start.sh
echo if [ -d "/opt/venv" ]; then >> start.sh
echo     source /opt/venv/bin/activate >> start.sh
echo fi >> start.sh
echo. >> start.sh
echo # Create necessary directories >> start.sh
echo mkdir -p src/database >> start.sh
echo mkdir -p legal_vector_db >> start.sh
echo. >> start.sh
echo # Start the application >> start.sh
echo echo "🌐 Starting Gunicorn on port $PORT..." >> start.sh
echo exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 src.main:app >> start.sh

REM Create runtime.txt
echo python-3.11 > runtime.txt

REM Update requirements.txt
echo blinker==1.9.0 > requirements.txt
echo click==8.2.1 >> requirements.txt
echo Flask==3.1.1 >> requirements.txt
echo flask-cors==6.0.0 >> requirements.txt
echo Flask-SQLAlchemy==3.1.1 >> requirements.txt
echo itsdangerous==2.2.0 >> requirements.txt
echo Jinja2==3.1.6 >> requirements.txt
echo MarkupSafe==3.0.2 >> requirements.txt
echo SQLAlchemy==2.0.41 >> requirements.txt
echo typing_extensions==4.14.0 >> requirements.txt
echo Werkzeug==3.1.3 >> requirements.txt
echo gunicorn==21.2.0 >> requirements.txt
echo openai==1.3.0 >> requirements.txt
echo chromadb==0.4.15 >> requirements.txt
echo langchain==0.0.350 >> requirements.txt
echo langchain-text-splitters==0.0.1 >> requirements.txt
echo numpy>=1.21.0 >> requirements.txt

echo.
echo ✅ All files created successfully!
echo.
echo Next steps:
echo 1. Update src/main.py (replace first 8 lines with the import fix)
echo 2. Run: git add .
echo 3. Run: git commit -m "Fix Railway deployment"
echo 4. Run: git push
echo 5. Redeploy on Railway
echo.
pause