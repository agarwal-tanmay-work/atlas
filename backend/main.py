from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routers import search, failures, analyze
from database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Atlas API",
    description="Cross-domain failure knowledge base powered by AI",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router, prefix="/api/search", tags=["search"])
app.include_router(failures.router, prefix="/api/failures", tags=["failures"])
app.include_router(analyze.router, prefix="/api/analyze", tags=["analyze"])

@app.get("/api/health")
def health():
    from database import count_failures
    return {"status": "ok", "message": "Atlas is running", "total_failures": count_failures()}
