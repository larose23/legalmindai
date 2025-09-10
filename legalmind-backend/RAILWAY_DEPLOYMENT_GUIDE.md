# Railway Deployment Guide for LegalMind Backend

## Your Railway Project
- **Project ID**: `7475be7e-e5d0-4bc7-802d-8059cfdf88fd`
- **Environment ID**: `a2dd7da3-8e39-4443-a26d-9ff0af5a980e`
- **Project URL**: https://railway.com/project/7475be7e-e5d0-4bc7-802d-8059cfdf88fd?environmentId=a2dd7da3-8e39-4443-a26d-9ff0af5a980e

## Quick Deployment Steps

### 1. Connect Your Repository
1. Go to your Railway project dashboard
2. Click "Connect GitHub" or "Deploy from GitHub repo"
3. Select your repository containing the LegalMind backend code

### 2. Set Environment Variables
In your Railway project dashboard, go to Variables and add:

```
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secure_secret_key_here
```

### 3. Deploy
Railway will automatically detect the Dockerfile and deploy your application.

## What's Been Fixed

✅ **Dockerfile**: Fixed PORT environment variable usage for Railway
✅ **Dependencies**: Added all required packages (OpenAI, ChromaDB, LangChain, Gunicorn)
✅ **Import Paths**: Fixed Python path issues for Railway deployment
✅ **Configuration**: Added railway.json for proper deployment settings
✅ **Documentation**: Created comprehensive README and deployment guides

## API Endpoints Available

Once deployed, your API will be available at:
- **Base URL**: `https://your-app-name.railway.app`
- **Health Check**: `https://your-app-name.railway.app/api/legalmind/health`
- **Document Analysis**: `https://your-app-name.railway.app/api/legalmind/analyze-document`
- **Document Summarization**: `https://your-app-name.railway.app/api/legalmind/summarize-document`
- **Legal Research**: `https://your-app-name.railway.app/api/legalmind/legal-research`
- **Document Drafting**: `https://your-app-name.railway.app/api/legalmind/draft-document`

## Testing Your Deployment

1. **Health Check**:
   ```bash
   curl https://your-app-name.railway.app/api/legalmind/health
   ```

2. **Ingest Sample Data**:
   ```bash
   curl -X POST https://your-app-name.railway.app/api/legalmind/ingest-sample-data
   ```

3. **Test Document Analysis**:
   ```bash
   curl -X POST https://your-app-name.railway.app/api/legalmind/analyze-document \
     -H "Content-Type: application/json" \
     -d '{"text": "This is a sample contract between Company A and Company B..."}'
   ```

## Troubleshooting

If you encounter issues:

1. **Check Railway Logs**: Go to your project dashboard → Deployments → View logs
2. **Verify Environment Variables**: Ensure OPENAI_API_KEY is set correctly
3. **Check Build Logs**: Look for any dependency installation errors

## Files Modified for Railway Deployment

- `Dockerfile`: Fixed PORT environment variable
- `requirements.txt`: Added missing dependencies
- `src/main.py`: Fixed import paths
- `railway.json`: Added Railway-specific configuration
- `README.md`: Comprehensive documentation
- `DEPLOYMENT.md`: Detailed deployment instructions

Your application is now ready for Railway deployment! 🚀