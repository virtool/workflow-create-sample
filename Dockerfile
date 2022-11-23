FROM ghcr.io/virtool/workflow:5.0.1
WORKDIR /app
COPY workflow.py /app/workflow.py
COPY fixtures.py /app/fixtures.py
