FROM python:3.12-slim
RUN pip install --no-cache-dir uv
WORKDIR /app
COPY pyproject.toml ./
RUN uv sync --no-dev
COPY app/ ./app/
RUN useradd -m app && chown -R app /app
USER app
CMD ["uv", "run", "python", "-m", "app.mcp_server"]
