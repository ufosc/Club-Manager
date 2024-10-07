FROM python:3.12.5-slim-bullseye AS base

LABEL maintainer="ikehunter.com"

# see logs immediately
ENV PYTHONUNBUFFERED 1
ENV PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

# default to production
ARG DEV=false

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apt-get update && \
    apt install -f && \
    apt-get install -y --no-install-recommends libpq-dev gcc g++

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
    
RUN /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp

COPY ./scripts /scripts

RUN adduser --no-create-home --system --disabled-password --disabled-login --group django-user && \
    mkdir -p /vol/static/media && \
    mkdir -p /vol/static/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol/static && \
    chmod -R +x /scripts


COPY ./app /app
ENV PATH="/scripts:/py/bin:/usr/bin:$PATH"
USER django-user

VOLUME /vol/web
CMD ["/scripts/entrypoint.sh"]
