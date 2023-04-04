FROM cgr.dev/chainguard/python:3.10-dev as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM cgr.dev/chainguard/python:3.10
WORKDIR /app
COPY --from=builder /home/nonroot/.local/lib/python3.10/site-packages /home/nonroot/.local/lib/python3.10/site-packages
COPY *.py .
ENTRYPOINT [ "python", "/app/main.py" ]
