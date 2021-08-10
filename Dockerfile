FROM virtool/workflow:latest

RUN pip install coloredlogs

WORKDIR /app

COPY vt_workflow_create_sample /app/workflow

WORKDIR /app/workflow