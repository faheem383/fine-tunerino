FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl gzip && rm -rf /var/lib/apt/lists/*

# Install Argo CLI
RUN curl -sLO https://github.com/argoproj/argo-workflows/releases/latest/download/argo-linux-amd64.gz \
 && gunzip argo-linux-amd64.gz \
 && chmod +x argo-linux-amd64 \
 && mv argo-linux-amd64 /usr/local/bin/argo

WORKDIR /app

COPY app.py .

RUN pip install fastapi uvicorn

EXPOSE 9080

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9080"]