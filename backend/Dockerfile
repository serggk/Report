FROM python:3.9-slim
COPY /app requirements.txt /app/
RUN pip install -r app/requirements.txt --no-cache-dir
EXPOSE 8000
CMD python -c 'from app.db import init_db; init_db()' && gunicorn --bind=0.0.0.0:8000 -w 4 -k uvicorn.workers.UvicornH11Worker app:app
