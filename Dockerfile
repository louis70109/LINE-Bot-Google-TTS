FROM python:3.9

WORKDIR /app
COPY ["requirements.txt", "/app/"]
CMD ["pwd"]

RUN python3 -m pip install -r requirements.txt
ENV GOOGLE_APPLICATION_CREDENTIALS=$pwd/app/google-service-key.json
ENV FIREBASE_CREDENTIALS=$pwd/app/firebase-adminsdk.json
ADD . /app
EXPOSE 5000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]

# CMD ["gunicorn", "api:app", "--log-file=-", "--bind=0.0.0.0:5000"]