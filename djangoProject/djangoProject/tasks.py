import os

from django.utils.module_loading import import_string

from djmoney import settings

from djangoProject.djangoProject.celery import app


@app.task
def update_rates(backend=settings.EXCHANGE_BACKEND, **kwargs):
    backend = import_string(backend)()
    backend.update_rates(**kwargs)
