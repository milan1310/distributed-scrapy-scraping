from celery import Celery

app = Celery('scrapy_tasks', broker='redis://:irro6HsquxkoE2S@localhost:6379/0')

app.conf.update(
    result_backend='redis://:irro6HsquxkoE2S@localhost:6379/0',
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    task_track_started=True,
    task_annotations={
        'tasks.run_spider': {'rate_limit': '10/m'}
    },
)
