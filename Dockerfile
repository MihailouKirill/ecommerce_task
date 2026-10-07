FROM python:3.14-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY . .
RUN uv pip install --system -r pyproject.toml
RUN mkdir -p reports
CMD ["python", "main.py"]
