FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir \
        fastapi==0.115.0 uvicorn==0.30.6 pydantic==2.9.2 pandas==2.2.2 \
        google-cloud-bigquery google-cloud-storage google-cloud-pubsub \
        google-cloud-logging google-cloud-monitoring google-adk

COPY . .

# Cloud Run injects PORT; default to 8080 for local `docker run`.
ENV PORT=8080
EXPOSE 8080

# Seed the mock warehouse on first boot (no-op once real BigQuery is wired up
# via USE_MOCK_BACKEND=false) so the image is runnable with zero setup.
CMD ["sh", "-c", "test -f mock_warehouse.db || python synthetic/generate_data.py; exec uvicorn api:app --host 0.0.0.0 --port ${PORT}"]
