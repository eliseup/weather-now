### Builder stage
FROM python:3.13.3-slim-bookworm AS builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev build-essential
COPY requirements.txt /tmp
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /tmp/wheels -r /tmp/requirements.txt


### Final stage.
FROM python:3.13.3-slim-bookworm

RUN apt-get update && \
    apt-get install -y locales libpq-dev sudo supervisor

RUN echo 'app ALL=(ALL) NOPASSWD:ALL' >/etc/sudoers.d/90-users

# Python deps.
COPY --from=builder /tmp/wheels /tmp/wheels
RUN pip install --upgrade pip
RUN pip install --no-cache /tmp/wheels/* && rm -rf /tmp/wheels

# User settings.
RUN addgroup --gid 1000 --system app && adduser --uid 1000 --system --group app
RUN usermod -aG sudo app
USER app

WORKDIR /usr/src/app
CMD ["tail", "-f", "/dev/null"]
