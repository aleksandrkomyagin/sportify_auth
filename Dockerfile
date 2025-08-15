FROM python:3.12

RUN apt-get update && \
    apt-get install -y --no-install-recommends gettext curl && \
    rm -rf /var/lib/apt/lists/* \
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONPATH=/app

RUN poetry config virtualenvs.create false

COPY pyproject.toml ./
COPY poetry.lock ./
RUN poetry install --no-root

COPY entrypoint.sh ./

COPY src/ .

CMD ["/bin/bash", "entrypoint.sh"]