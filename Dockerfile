FROM ghcr.io/virtool/workflow:5.4.2
WORKDIR /app
COPY fixtures.py workflow.py ./
