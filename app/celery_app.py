from celery import Celery
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
celery_app = Celery("cloudcrm", broker=REDIS_URL, backend=REDIS_URL)

@celery_app.task
def send_notification(client_name):
    print(f"Notification sent to {client_name}")
