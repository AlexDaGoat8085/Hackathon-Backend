import json
import logging
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Configure logging to stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("hackathon_backend")

# Global config state
app_config: Dict[str, Any] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load configuration on startup
    try:
        with open("config.json", "r") as f:
            global app_config
            app_config = json.load(f)
            logger.info("Configuration loaded successfully. System ready.")
    except FileNotFoundError:
        logger.warning("config.json missing! Some services may fail to authenticate.")
    yield
    logger.info("Shutting down connections...")

app = FastAPI(title="Core Backend API", lifespan=lifespan)

# Restrict CORS in production!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

@app.get("/api/v1/health")
async def health_check() -> Dict[str, str]:
    return {"status": "operational", "version": "1.0.4-beta"}

@app.post("/api/v1/ingest")
async def ingest_telemetry_data(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not payload:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty payload")
    
    # Mock processing delay
    logger.info(f"Processing telemetry from node: {payload.get('node_id', 'unknown')}")
    return {"status": "success", "processed_bytes": len(str(payload))}
