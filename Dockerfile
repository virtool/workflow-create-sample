FROM python:3.10-buster as jre
RUN apt-get update && \
    apt-get install -y --no-install-recommends default-jre && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

FROM python:3.10-buster as poetry
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:${PATH}"
COPY pyproject.toml poetry.lock workflow.py ./
RUN poetry install

FROM jre as base
COPY --from=ghcr.io/virtool/workflow-tools:2.0.1 /opt/fastqc /opt/fastqc
RUN chmod ugo+x /opt/fastqc/fastqc && \
    ln -fs /opt/fastqc/fastqc /usr/local/bin/fastqc
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:${PATH}"
COPY pyproject.toml poetry.lock workflow.py VERSION* ./
RUN poetry install
RUN poetry export > requirements.txt
RUN pip install -r requirements.txt
