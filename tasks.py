import celery

celery_service = celery.Celery('mailing tasks', broker='redis://redis:6379', backend='redis://redis:6379')

celery_service.autodiscover_tasks([
    'services.mail_sender',
])
