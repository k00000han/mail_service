import celery

celery_service = celery.Celery('mailing tasks', broker='redis://localhost:6379', backend='redis://localhost:6379')
