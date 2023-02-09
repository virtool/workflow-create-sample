FROM ghcr.io/virtool/workflow:5.3.0
WORKDIR /app
COPY workflow.py /app/workflow.py
COPY fixtures.py /app/fixtures.py
