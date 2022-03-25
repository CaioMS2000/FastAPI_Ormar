#web: uvicorn main:app --host=0.0.0.0 --port=${PORT:-500}
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker