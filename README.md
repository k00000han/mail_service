Run FastAPI:

  uvicorn api.main:app --reload

Run Celery:

  celery -A tasks worker -l info
