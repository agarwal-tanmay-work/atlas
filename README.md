<div align="center">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDBkZ3EzYTdzazE4Zm1yZnU3MmxxdWFzOXkxaHZzOXoxZjB1czU0dyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/L8K62iDadb2Bq/giphy.gif" alt="Atlas Globe" width="200"/>

  # 🌍 ATLAS 
  ### AI-Powered Cross-Domain Failure Knowledge Base

  [![Made with FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
  [![Built with React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
  [![Vite](https://img.shields.io/badge/Vite-B73BFE?style=for-the-badge&logo=vite&logoColor=FFD62E)](https://vitejs.dev/)
  [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
  [![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

  *Learning from the past to secure the future.*
</div>

---

## 🚀 The Vision

**Atlas** is an intelligent, scalable platform designed to aggregate, map, and analyze structural, software, and systemic failures across history. By leveraging modern Large Language Models and mathematically mapping root causes using vector embeddings, Atlas connects the dots between a bridge collapse and a software outage, teaching us the universal warning signs of disaster.

## 🛠️ The Tech Stack (Hackathon Ready)

Atlas is built on a production-grade, modern, and lightning-fast architecture:

* **Frontend:** React + Vite + TailwindCSS (Dynamic, fluid UI with a dark-glassmorphism aesthetic)
* **Backend:** Python + FastAPI (Blazing fast asynchronous API)
* **Database:** PostgreSQL + `pgvector` (Unified relational data and high-dimensional semantic vector search)
* **AI engine:** Google Gemini 2.5 Flash (Extracting structured schemas from mountains of unstructured text)
* **Embeddings:** `sentence-transformers` (`all-MiniLM-L6-v2`) inside Python
* **Infrastructure:** Fully Containerized with Docker Compose

## ⚡ Getting Started (Run it in seconds)

Just have Docker installed and an API key ready.

1. **Clone the Repo**
   ```bash
   git clone https://github.com/agarwal-tanmay-work/atlas.git
   cd atlas
   ```

2. **Set your Environment Variables**
   Create a `.env` file referencing `.env.example` and place your Gemini key inside:
   ```env
   GEMINI_API_KEY=your_key_here
   DATABASE_URL=postgresql://atlas:atlas_password@db:5432/atlas
   ```

3. **Launch the Stack!**
   ```bash
   docker compose up -d --build
   ```
   > 🧨 *Boom. Your database, backend, and frontend are linked and live.*

4. **Access the Application**
   * Interface: `http://localhost:5173`
   * API Docs: `http://localhost:8000/docs`

## 🧠 Data Ingestion Pipeline

Atlas comes with an automated AI scraper capable of analyzing the famous [Dan Luu Post-Mortem repository](https://github.com/danluu/post-mortems).
Once Docker is running, you can seed the entire PostgreSQL database natively:

```bash
docker exec -it atlas-backend python -m ingestion.run_ingestion
docker exec -it atlas-backend python -m ingestion.ingest_danluu
```
*Note: Due to rate-limits on the free AI models safely reading 100+ pages of crash sites, this background ingest takes about 15 minutes.*

---
<div align="center">
  <i>Built with 💻 and ☕ for the hackathon prototype.</i>
</div>
