from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app import models, celery_app
import hashlib

Base.metadata.create_all(bind=engine)
app = FastAPI(title="CloudCRM")
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    user = db.query(models.User).filter(models.User.username == username, models.User.password == hashed_pw).first()
    if user:
        response = RedirectResponse(url="/dashboard", status_code=303)
        response.set_cookie(key="user_role", value=user.role)
        return response
    return templates.TemplateResponse("index.html", {"request": request, "error": "Неверный логин или пароль"})

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    role = request.cookies.get("user_role")
    if not role:
        return RedirectResponse(url="/")
    clients = db.query(models.Client).all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "clients": clients, "role": role})

@app.post("/add_client")
def add_client(name: str = Form(...), request: Request = None, db: Session = Depends(get_db)):
    new_client = models.Client(name=name)
    db.add(new_client)
    db.commit()
    celery_app.send_notification.delay(name)
    return RedirectResponse(url="/dashboard", status_code=303)

@app.get("/logout")
def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("user_role")
    return response
