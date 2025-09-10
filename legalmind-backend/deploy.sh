#!/bin/bash

# LegalMind Backend Deployment Script for Railway

echo "🚀 Deploying LegalMind Backend to Railway..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

# Login to Railway (this will open a browser)
echo "🔐 Please login to Railway in your browser..."
railway login

# Initialize Railway project if not already done
echo "📦 Initializing Railway project..."
railway init

# Deploy the application
echo "🚀 Deploying to Railway..."
railway up

echo "✅ Deployment complete!"
echo "🌐 Your app should be available at the Railway URL provided above."
echo ""
echo "📝 Don't forget to set your environment variables in Railway dashboard:"
echo "   - OPENAI_API_KEY: Your OpenAI API key"
echo "   - SECRET_KEY: A secure secret key for Flask"