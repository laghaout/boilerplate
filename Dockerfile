FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy metadata that the backend expects (README is often referenced in pyproject)
COPY pyproject.toml uv.lock README.md README.txt ./

# Ensure the package exists before install (src-layout)
COPY src ./src

# Install deps + project from the lockfile
RUN uv sync --locked

# Make the venv active for runtime
ENV PATH="/app/.venv/bin:$PATH"

# Bring the rest (configs, data, scripts)
COPY config ./config
COPY data ./data
COPY run.sh ./run.sh
COPY tests ./tests

CMD ["python", "-m", "boilerplate.main"]

# EXPOSE 8000
# CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
# docker run -p 8000:8000 boilerplate
