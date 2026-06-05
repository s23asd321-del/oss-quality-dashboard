FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY oss_quality_dashboard ./oss_quality_dashboard

RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir .

EXPOSE 8000

CMD ["python", "-m", "oss_quality_dashboard.app", "--host", "127.0.0.1", "--port", "8000"]

