from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from app.db.database import engine, Base
from app.routers import telemetry, animals, auth, ingest, user
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from jose import jwt, JWTError
from app.core.security import SECRET_KEY, ALGORITHM
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.core.logging_config import setup_logging
from app.core.limiter import limiter
import os
from app.db.database import SessionLocal
from app.models.user import User
from app.core.security import hash_password

app = FastAPI(
    title="SmartFarm API",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

setup_logging()

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"}
    )

@app.on_event("startup")
def on_startup():
    # if os.getenv("ENV") != "production":      saco para crear tabla animals en produccion
        Base.metadata.create_all(bind=engine)
        create_admin_if_not_exists()

def create_admin_if_not_exists():
    db = SessionLocal()
    try:
        admin = db.query(User).filter(
            User.email == "admin@smartfarm.com"
        ).first()
        if not admin:
            admin = User(
                username="admin",
                email="admin@smartfarm.com",
                password_hash=hash_password("admin123"),
                role="admin"
            )
            db.add(admin)
            db.commit()
            print("✅ Admin creado")
        else:
            print("ℹ️ Admin ya existe")
    finally:
        db.close()



templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    token = request.cookies.get("access_token")
    if token:
        try:
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )
            role = payload.get("role")
            if role == "admin":
                return RedirectResponse("/telemetry/dashboard", status_code=303)
            elif role == "tecnico":
                return RedirectResponse("/telemetry/dashboard", status_code=303)
            elif role == "operario":
                return RedirectResponse("/animals", status_code=303)
        except JWTError:
            pass  # token inválido → mostrar login
    return templates.TemplateResponse(
        "home_login.html",
        {"request": request}
    )

app.include_router(telemetry.router, prefix="/api/v1")
app.include_router(animals.router, prefix="/api/v1")
app.include_router(user.router, prefix="/api/v1")
app.include_router(telemetry.router)
app.include_router(animals.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(ingest.router)






