import os
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.constants import APP_NAME, APP_VERSION, APP_DESCRIPTION, API_PREFIX
from app.core.logger import logger
from app.api import upload, chat, health

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
)

# CORS — allow Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(health.router, prefix=API_PREFIX, tags=["Health"])
app.include_router(upload.router, prefix=API_PREFIX, tags=["Documents"])
app.include_router(chat.router, prefix=API_PREFIX, tags=["Chat"])


@app.on_event("startup")
async def startup():
    logger.info(f"{APP_NAME} v{APP_VERSION} starting up")


@app.on_event("shutdown")
async def shutdown():
    logger.info(f"{APP_NAME} shutting down")
