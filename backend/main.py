from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from app.core.config import settings
from app.core.database import engine, Base
from app.routers import auth, users, chats, messages, files, presence
from app.core.websocket_manager import manager
from app.websocket.connection import websocket_endpoint

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()

app = FastAPI(
    title="WhatsApp Clone API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket manager
app.state.websocket_manager = manager

@app.websocket("/ws")
async def websocket_route(websocket: WebSocket, token: str):
    await websocket_endpoint(websocket, token)

# Routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(chats.router, prefix="/api/v1/chats", tags=["chats"])
app.include_router(messages.router, prefix="/api/v1/chats", tags=["messages"])
app.include_router(files.router, prefix="/api/v1/files", tags=["files"])
app.include_router(presence.router, prefix="/api/v1/presence", tags=["presence"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
