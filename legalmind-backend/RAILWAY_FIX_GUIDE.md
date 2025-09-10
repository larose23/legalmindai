# Railway Deployment Fix Guide

## Problem Identified
Railway was using Nixpacks instead of Docker and couldn't find a start command. The error was:
```
No start command could be found
```

## Solution Applied

I've created the following files to fix the Railway deployment:

### 1. `nixpacks.toml` - Nixpacks Configuration
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

### 2. `Procfile` - Alternative Start Command
```
web: gunicorn --bind 0.0.0.0:$PORT src.main:app
```

### 3. `start.sh` - Startup Script
- Handles port configuration
- Creates necessary directories
- Starts Gunicorn with proper settings

### 4. `runtime.txt` - Python Version
```
python-3.11
```

### 5. Updated `requirements.txt`
- Added numpy dependency for ChromaDB compatibility
- Ensured all versions are compatible

## Next Steps

1. **Commit and push these changes** to your repository
2. **Redeploy** in Railway - it should now detect the start command
3. **Set environment variables** in Railway dashboard:
   - `OPENAI_API_KEY=your_openai_api_key_here`
   - `SECRET_KEY=your_secure_secret_key_here`

## What These Files Do

- **nixpacks.toml**: Tells Railway how to build and run your Python app
- **Procfile**: Alternative start command (Railway will use this if nixpacks.toml doesn't work)
- **start.sh**: Robust startup script that handles environment setup
- **runtime.txt**: Specifies Python 3.11 for Railway
- **requirements.txt**: Updated with all necessary dependencies

## Expected Result

After pushing these changes, Railway should:
1. ✅ Detect Python as the language
2. ✅ Install dependencies from requirements.txt
3. ✅ Find the start command from nixpacks.toml
4. ✅ Successfully deploy your application

## Testing

Once deployed, test with:
```bash
curl https://your-app-name.railway.app/api/legalmind/health
```

Should return: `{"status": "healthy", "service": "LegalMind AI"}`

## Troubleshooting

If it still fails:
1. Check Railway logs for specific error messages
2. Ensure all files are committed and pushed
3. Try redeploying from Railway dashboard
4. Check that environment variables are set correctly