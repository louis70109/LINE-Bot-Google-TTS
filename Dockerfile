FROM python:3.9

WORKDIR /app
COPY ["requirements.txt", "/app/"]

RUN python3 -m pip install -r requirements.txt

ENV FIREBASE_CREDENTIALS=$pwd/app/firebase-adminsdk.json
ADD . /app
EXPOSE 8080
CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 8 app.main:app

# CMD ["gunicorn", "api:app", "--log-file=-", "--bind=0.0.0.0:5000"]