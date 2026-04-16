# Atlas — Cross-Domain Failure Knowledge Base

Atlas is the world's first AI-powered cross-domain failure knowledge base. It ingests real public post-mortems and incident reports from across software engineering, aviation, medicine, finance, and government, extracts structured failure data using an LLM, stores it in a vector database for semantic search, and lets users search by symptom, root cause, or project description to find historically analogous failures and the lessons learned from them.

## Tech Stack
- **Frontend**: React + Vite, Tailwind CSS, Framer Motion
- **Backend**: Python 3.11+, FastAPI, Uvicorn
- **AI / LLM**: Anthropic Claude API (`claude-sonnet-4-20250514`)
- **Database**: SQLite (relational) + ChromaDB (vector semantic search)
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`

## Features
- **Semantic Search**: Search across multiple failure scenarios by problem or scenario using ChromaDB.
- **Project Analyzer**: Enter your project's architecture or domain, and the AI will analyze it against historical failures to output a detailed risk summary and analogous incidents.
- **Cross-Domain Relationship Engine**: Finds and links analogous incidents across entirely different industries based on conceptual similarity (e.g. comparing the Challenger Disaster to the Enron Accounting Fraud by root cause).

## Getting Started

### 1. Configure the Environment
Copy the example environment file and insert your API keys:
```bash
cp .env.example .env
```
Inside `.env`, set your Anthropic API Key:
```env
ANTHROPIC_API_KEY=your_actual_anthropic_api_key
```

### 2. Backend Setup
1. Open a terminal to the `backend` directory: `cd backend`
2. Install the necessary Python packages: `pip install -r requirements.txt`
3. Run the ingestion pipeline to generate embeddings and seed the ChromaDB/SQLite tables with our dataset of 60 real world failures:
   ```bash
   python ingestion/run_ingestion.py
   ```
4. Start the backend API server:
   ```bash
   python -m uvicorn main:app --port 8000 --reload
   ```
The backend will run at `http://127.0.0.1:8000`.

### 3. Frontend Setup
1. Open a new terminal to the `frontend` directory: `cd frontend`
2. Install the frontend Node modules: `npm install`
3. Start the dev server:
   ```bash
   npm run dev
   ```
4. Access the application in your browser at `http://localhost:5173`.

## File Structure Highlights
- `/backend/chroma_store.py`: Interacts with ChromaDB to manage vector embeddings for semantic search.
- `/backend/database.py`: Handles structured data storage inside `atlas.db` SQLite database.
- `/backend/ingestion/seed_data.py`: Contains our core, carefully curated dataset of 60 historic failures.
- `/backend/ingestion/run_ingestion.py`: Inserts our curated dataset into SQLite and calculates LLM embeddings to ingest them into ChromaDB. Runs the Relationship Engine.
- `/backend/llm_extractor.py`: Utility functions connecting to the Claude API.
- `/backend/routers/`: FastAPI routes defining search, failures, and analysis controllers.
- `/frontend/src/pages/`: React views, including the homepage, deep-dive search interface, and Project Risk Analyzer. 
