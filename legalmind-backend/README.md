# LegalMind Backend

A Flask-based backend service for legal document analysis and AI-powered legal assistance.

## Features

- **Document Analysis**: Extract key information from legal documents
- **Document Summarization**: Generate concise or detailed summaries
- **Legal Research**: RAG-powered legal research using vector database
- **Document Drafting**: Generate legal documents from templates
- **User Management**: Basic user CRUD operations

## Tech Stack

- **Backend**: Flask, Python 3.11
- **Database**: SQLite (with SQLAlchemy ORM)
- **AI/ML**: OpenAI GPT-4, ChromaDB for vector storage
- **Text Processing**: LangChain text splitters
- **Deployment**: Railway (Docker)

## Quick Start

### Local Development

1. **Clone and setup**:
   ```bash
   cd legalmind-backend
   pip install -r requirements.txt
   ```

2. **Set environment variables**:
   ```bash
   export OPENAI_API_KEY="your_openai_api_key_here"
   export SECRET_KEY="your_secret_key_here"
   ```

3. **Run the application**:
   ```bash
   python src/main.py
   ```

4. **Access the API**:
   - API Base URL: `http://localhost:5000`
   - Health Check: `http://localhost:5000/api/legalmind/health`

### Railway Deployment

#### Option 1: Using Railway CLI

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**:
   ```bash
   railway login
   ```

3. **Deploy**:
   ```bash
   railway up
   ```

#### Option 2: Using Railway Dashboard

1. **Connect your GitHub repository** to Railway
2. **Set environment variables** in Railway dashboard:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `SECRET_KEY`: A secure secret key for Flask
3. **Deploy** from the Railway dashboard

## API Endpoints

### User Management
- `GET /api/users` - Get all users
- `POST /api/users` - Create a new user
- `GET /api/users/{id}` - Get user by ID
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Delete user

### Legal Analysis
- `POST /api/legalmind/analyze-document` - Analyze legal document
- `POST /api/legalmind/summarize-document` - Summarize document
- `POST /api/legalmind/legal-research` - Perform legal research
- `POST /api/legalmind/draft-document` - Draft legal document
- `POST /api/legalmind/ingest-sample-data` - Ingest sample data
- `GET /api/legalmind/health` - Health check

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for AI features | Yes |
| `SECRET_KEY` | Flask secret key | Yes |
| `PORT` | Port number (Railway sets this) | No |
| `DATABASE_URL` | Database connection string | No |

## Project Structure

```
legalmind-backend/
├── src/
│   ├── main.py              # Flask application entry point
│   ├── models/
│   │   └── user.py          # User model
│   ├── routes/
│   │   ├── user.py          # User API routes
│   │   └── legalmind.py     # Legal analysis API routes
│   ├── static/
│   │   └── index.html       # Frontend (if any)
│   └── database/
│       └── app.db           # SQLite database
├── legal_vector_db/         # ChromaDB vector database
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── railway.json            # Railway deployment config
└── README.md               # This file
```

## Development Notes

- The application uses ChromaDB for vector storage of legal documents
- OpenAI GPT-4 is used for document analysis and generation
- CORS is enabled for frontend integration
- The app serves static files from the `static` directory

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure you're running from the project root directory
2. **OpenAI API errors**: Verify your API key is set correctly
3. **Database errors**: The SQLite database will be created automatically
4. **Port issues**: Railway will set the PORT environment variable automatically

### Logs

Check Railway logs for deployment issues:
```bash
railway logs
```

## License

This project is for educational and demonstration purposes.