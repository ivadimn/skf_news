import os
from celery import Celery
from celery.schedules import crontab
from .settings import EMAIL_HOST_PASSWORD

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_paper.settings')
pickup = os.environ.get("PICKUP")


app = Celery('news_paper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
   'inform_about_last_news_weekly': {
        'task': 'news.tasks.inform_weekly',
        'schedule': crontab(minute=0, hour='*'), #crontab(hour=5, minute=0, day_of_week='friday'),
        'args': ("jLwvW31eWxFaf4XEGyhV", )
   }
}
