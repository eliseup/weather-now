from celery import Celery
from celery.signals import after_setup_task_logger

from logging.config import dictConfig


app = Celery('weather_api')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


def extra_celery_logging(**kwargs):
    from django.conf import settings
    dictConfig(settings.LOGGING)


after_setup_task_logger.connect(extra_celery_logging)
