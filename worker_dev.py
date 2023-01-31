# reload celery automaticaly on every save
from django.utils import autoreload


def run_celery():
    from similarity.celery import app as celery_app
    celery_app.worker_main(["worker", "-linfo", "-Psolo"])


autoreload.run_with_reloader(run_celery)
