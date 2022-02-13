FROM python:3.7

WORKDIR /app
COPY ["requirements.txt", "/app/"]
RUN python3 -m pip install -r requirements.txt
ADD . /app
EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]

# CMD ["gunicorn", "api:app", "--log-file=-", "--bind=0.0.0.0:5000"]