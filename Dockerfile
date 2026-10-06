FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create runtime directories required by the ETL pipeline
RUN mkdir -p data/raw data/processed data/archive logs

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]