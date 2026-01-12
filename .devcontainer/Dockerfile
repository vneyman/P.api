FROM python:3.13-slim

# Install Node.js and common Linux utilities
RUN apt-get update && apt-get install -y \
    curl \
    sudo \
    git \
    openssh-client \
    apt-transport-https \
    ca-certificates \
    gnupg2 \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    && curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \
    && apt-get install -y nodejs \
    && npm i -g @openai/codex@latest \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install uv (Python package manager)
RUN pip install --no-cache-dir uv
    
# Create working directory
WORKDIR /app

# Copy Python dependencies and install
COPY requirements.txt .
RUN uv pip install --system -r requirements.txt

# Default shell
CMD ["/bin/bash"]
