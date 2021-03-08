import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

app = Celery('mysite')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'get_stocks_1h': {
        'task': 'tasks.get_stocks_data',
        'schedule': 3600.0
    }
}
app.autodiscover_tasks()