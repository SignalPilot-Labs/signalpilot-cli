# SignalPilot CLI - Development & Testing Docker Image
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv (Python package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:${PATH}"

# Create working directory
WORKDIR /workspace

# Copy the CLI source code
COPY . /app/sp-cli

# Install sp-cli in development mode
WORKDIR /app/sp-cli
RUN uv venv .venv && \
    .venv/bin/pip install -e ".[dev]"

# Add sp to PATH for easy access
ENV PATH="/app/sp-cli/.venv/bin:${PATH}"

# Create a test project directory
WORKDIR /root/SignalPilotHome

# Expose Jupyter Lab port
EXPOSE 9999

# Default command: open a bash shell
CMD ["/bin/bash"]
