FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY .env .env

EXPOSE 8000

CMD ["python3", "manage.py", "makemigrations"]
CMD ["python3", "manage.py", "migrate"]

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
