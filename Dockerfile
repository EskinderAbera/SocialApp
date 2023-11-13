FROM ubuntu:latest
LABEL authors="Eskinder Abera"

ENTRYPOINT ["top", "-b"]

FROM python:3.11.2
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
