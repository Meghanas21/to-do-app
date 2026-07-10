"""
Application entrypoint.

THIS FILE IS WHERE THE ACTUAL CORS FIX LIVES.

Root causes this addresses:
1. Missing CORSMiddleware entirely (browser blocks every cross-origin call).
2. Using allow_origins=["*"] together with allow_credentials=True — the
   CORS spec explicitly forbids the wildcard when credentials (cookies or
   Authorization headers sent with credentials mode) are involved, and
   browsers will silently reject such a config. We list explicit origins
   from settings instead.
3. Not allowing the "Authorization" header — needed since the frontend
   sends "Authorization: Bearer <token>" on every authenticated request.
4. Not allowing all needed HTTP methods (GET/POST/PUT/DELETE/OPTIONS) —
   preflight OPTIONS requests fail if methods aren't explicitly permitted.
5. CORSMiddleware must be added so it wraps the whole app (including error
   handling) so that even error responses (validation errors, 500s) carry
   CORS headers — otherwise a server error looks like a "CORS error" in
   the browser console.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging_config import configure_logging, logger
from app.db.init_db import init_db
from app.exceptions.handlers import register_exception_handlers
from app.api.v1.routers import auth, knowledge, todos

configure_logging()

app = FastAPI(
    title=settings.APP_NAME,
    description="Production-ready Todo API with JWT auth, built to eliminate CORS errors.",
    version="1.0.0",
)

# --- CORS: must be added before/outside other middleware and route registration ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,   # explicit origins from .env, never "*"
    allow_credentials=True,                     # required because we send Authorization headers
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

# --- Global exception handling (keeps CORS headers on error responses too) ---
register_exception_handlers(app)

# --- Routers ---
app.include_router(auth.router)
app.include_router(knowledge.router)
app.include_router(todos.router)


@app.on_event("startup")
def on_startup():
    init_db()
    logger.info("Startup complete. Allowed CORS origins: %s", settings.cors_origins_list)


@app.get("/api/v1/health", tags=["health"])
def health_check():
    """Simple endpoint to verify the API is reachable — use this first when debugging CORS."""
    return {"status": "ok", "environment": settings.ENVIRONMENT}
