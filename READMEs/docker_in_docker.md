To modify your devcontainer.json file so that it can include Docker functionality within your existing setup, follow these steps:

# STEP 1 - Add Docker Installation Steps to Your Dockerfile

```Dockerfile
FROM python:3.12-slim
# Install dependencies for Docker and Google Cloud SDK
RUN apt-get update && \
    apt-get install -y apt-transport-https ca-certificates gnupg curl
# Add Google Cloud SDK repository and install the CLI
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" \
    | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN apt-get update && \
    apt-get install -y git vim net-tools build-essential google-cloud-cli=498.0.0-0
# Install dependencies for Docker and general packages
RUN apt-get update && \
    apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release sudo && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" \
    | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && \
    apt-get install -y docker-ce-cli

# Check if the 'docker' group exists, and create it if not
RUN if ! getent group docker; then groupadd docker; fi

# Create a 'vscode' user and use the existing GID 1000 if it exists
RUN if ! id -u vscode 2>/dev/null; then \
        if getent group 1000; then \
            useradd -m -s /bin/bash -u 1000 -g 1000 vscode; \
        else \
            groupadd -g 1000 vscode && \
            useradd -m -s /bin/bash -u 1000 -g vscode vscode; \
        fi; \
    fi

# Add 'vscode' to the 'docker' group if it exists
RUN usermod -aG docker vscode || true

# Allow 'vscode' user to run sudo without a password
RUN echo "vscode ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Set 'vscode' as the default user
USER vscode

WORKDIR /code
ENV PYTHONPATH=/code
```

# STEP 2 - Update Your DevContainer Configuration

Now, update the .devcontainer/devcontainer.json to enable Docker-in-Docker:

```json
{
  "name": "Devcontainer with Python, gcloud, & Docker installed",
  "build": {
    "dockerfile": "../Dockerfile.dev"
  },
  "customizations": {
    "vscode": {
        "extensions": [
            "ms-python.python",
            "ms-python.vscode-pylance",
            "ms-python.black-formatter",
            "ms-python.debugpy",
            "ms-azuretools.vscode-docker"
        ],
        "settings": {}
    }
  },
  "forwardPorts": [
    "5678:5678"
  ],
  "workspaceMount": "source=${localWorkspaceFolder},target=/code,type=bind,consistency=delegated",
  "workspaceFolder": "/code",
  "runArgs": [
    "--privileged",  // Allows the container to use Docker functionalities
    "-v", "/var/run/docker.sock:/var/run/docker.sock" // Mount Docker socket
  ],
  "postCreateCommand": "sudo chown root:docker /var/run/docker.sock && sudo chmod 660 /var/run/docker.sock && sudo usermod -aG docker $(whoami)"
}
```

# STEP 3 - Rebuild the Dev Container

Open the Command Palette in VSCode (Ctrl + Shift + P or Cmd + Shift + P).

# STEP 4 - Verify Docker Setup Inside the Container

Once the container is rebuilt, open a terminal inside it and check Docker’s functionality...

```bash
docker --version
docker ps
```