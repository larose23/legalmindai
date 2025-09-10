# Railway Deployment Guide

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **OpenAI API Key**: Get your API key from [OpenAI Platform](https://platform.openai.com)

## Deployment Steps

### Method 1: Railway Dashboard (Recommended)

1. **Connect Repository**:
   - Go to [Railway Dashboard](https://railway.app/dashboard)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

2. **Configure Environment Variables**:
   - Go to your project settings
   - Add the following environment variables:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     SECRET_KEY=your_secure_secret_key_here
     ```

3. **Deploy**:
   - Railway will automatically detect the Dockerfile
   - Click "Deploy" to start the deployment process

### Method 2: Railway CLI

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login**:
   ```bash
   railway login
   ```

3. **Initialize Project**:
   ```bash
   railway init
   ```

4. **Set Environment Variables**:
   ```bash
   railway variables set OPENAI_API_KEY=your_openai_api_key_here
   railway variables set SECRET_KEY=your_secure_secret_key_here
   ```

5. **Deploy**:
   ```bash
   railway up
   ```

## Post-Deployment

1. **Test the API**:
   - Visit your Railway URL + `/api/legalmind/health`
   - Should return: `{"status": "healthy", "service": "LegalMind AI"}`

2. **Ingest Sample Data** (Optional):
   ```bash
   curl -X POST https://your-app.railway.app/api/legalmind/ingest-sample-data
   ```

## Troubleshooting

### Common Issues

1. **Build Failures**:
   - Check that all dependencies are in `requirements.txt`
   - Verify Dockerfile syntax

2. **Runtime Errors**:
   - Check Railway logs: `railway logs`
   - Verify environment variables are set

3. **API Not Responding**:
   - Ensure `PORT` environment variable is used in the app
   - Check that the app binds to `0.0.0.0`

### Useful Commands

```bash
# View logs
railway logs

# Check status
railway status

# View environment variables
railway variables

# Connect to project
railway link
```

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for AI features | `sk-...` |
| `SECRET_KEY` | Flask secret key | `your-secret-key` |
| `PORT` | Port number (set by Railway) | `5000` |

## Next Steps

After successful deployment:

1. **Test all endpoints** using the Railway URL
2. **Set up monitoring** in Railway dashboard
3. **Configure custom domain** if needed
4. **Set up CI/CD** for automatic deployments