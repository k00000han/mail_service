from fastapi import FastAPI

app = FastAPI(title='Mail Service')


@app.get('/')
def index():
    return {"status": "ok"}

