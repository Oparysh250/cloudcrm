import time
from app.database import engine, Base, SessionLocal
from app import models
import hashlib

time.sleep(5) # Ждем запуска Postgres
Base.metadata.create_all(bind=engine)
db = SessionLocal()
if not db.query(models.User).first():
    admin = models.User(username="admin", password=hashlib.sha256(b"admin").hexdigest(), role="admin")
    db.add(admin)
    db.commit()
    print("Admin created!")
