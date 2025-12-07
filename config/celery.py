"""Celery configuration for async tasks and broadcasting."""
import os

from celery import Celery
from celery.schedules import crontab
from decouple import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

app = Celery("uniland")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Periodic tasks configuration
app.conf.beat_schedule = {
    "cleanup-old-sessions": {
        "task": "apps.bot.tasks.cleanup_old_sessions",
        "schedule": crontab(hour=3, minute=0),  # Run daily at 3 AM
    },
    "update-statistics": {
        "task": "apps.analytics.tasks.update_statistics",
        "schedule": crontab(minute="*/30"),  # Every 30 minutes
    },
    "sync-search-index": {
        "task": "apps.submissions.tasks.sync_search_index",
        "schedule": crontab(minute="*/15"),  # Every 15 minutes
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
