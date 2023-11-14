FROM python:3.11.2
LABEL authors="Eskinder Abera"

WORKDIR /app

# COPY requirements.txt requirements.txt

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
# # Command to run the application
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
