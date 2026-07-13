FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir uv
WORKDIR /app
COPY pyproject.toml ./
RUN uv sync --no-dev
COPY app/ ./app/
RUN useradd -m app && chown -R app /app
USER app
# repo is bind-mounted read-only from the host; ownership rarely matches the container
# user, which trips git's "dubious ownership" guard (CVE-2022-24765) — this container
# only ever runs `git ls-files` read-only against a mount the user chose, so trust it.
RUN git config --global --add safe.directory '*'
CMD ["uv", "run", "python", "-m", "app.mcp_server"]
