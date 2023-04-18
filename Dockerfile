FROM python:3.10-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.10-slim
RUN adduser --home /home/appuser --shell /bin/bash --uid 1000 --gecos "app user" --disabled-password appuser
WORKDIR /app
COPY --chown=appuser:appuser --from=builder /root/.local/lib/python3.10/site-packages /home/appuser/.local/lib/python3.10/site-packages
COPY --chown=appuser:appuser *.py .
USER appuser
WORKDIR /workspace
ENTRYPOINT [ "python", "/app/main.py" ]
