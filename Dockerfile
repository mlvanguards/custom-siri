FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Set environment variables
ENV WORKSPACE_ROOT=custom-siri \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

RUN mkdir -p $WORKSPACE_ROOT

# Install OS dependencies
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends build-essential \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR $WORKSPACE_ROOT

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Installing separately from its dependencies allows optimal layer caching
ADD . ${WORKSPACE_ROOT}

ENV PATH="${WORKSPACE_ROOT}/.venv/Scripts:$PATH"

CMD ["streamlit", "run", "src/streamlit_siri_demo/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.runOnSave=True"]
