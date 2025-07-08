FROM python:3.13.5-slim-bookworm AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir pipenv==2025.0.3


COPY Pipfile Pipfile.lock ./

ENV PIPENV_VENV_IN_PROJECT=1
RUN pipenv install --deploy --ignore-pipfile


FROM python:3.13.5-slim-bookworm AS runtime

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PYTHONIOENCODING=utf-8 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

COPY --from=builder /app/.venv /app/.venv

ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PATH="/app/.venv/bin:$PATH"


COPY conf/ ./conf/
COPY dependencies/ ./dependencies/
COPY src/ ./src/


EXPOSE 8001
