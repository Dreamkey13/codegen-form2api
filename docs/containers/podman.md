# Podman Container Management

This guide explains how to build and manage containers for the ART Code Generation System using Podman.

## Prerequisites
- Podman 4.0 or later
- Podman Compose (optional, for multi-container setup)

## Building the Container

1. Build the container image:
```bash
# Build using Containerfile
podman build -t art-code-gen:latest .

# Build with specific platform (if needed)
podman build --platform linux/amd64 -t art-code-gen:latest .
```

2. Build with custom build arguments:
```bash
podman build \
  --build-arg PYTHON_VERSION=3.9 \
  --build-arg NODE_VERSION=18 \
  -t art-code-gen:latest .
```

## Running the Container

1. Run in detached mode:
```bash
podman run -d \
  --name art-code-gen \
  -p 8000:8000 \
  -p 3000:3000 \
  --env-file .env \
  art-code-gen:latest
```

2. Run with volume mounts for development:
```bash
podman run -d \
  --name art-code-gen-dev \
  -p 8000:8000 \
  -p 3000:3000 \
  --env-file .env \
  -v ./src:/app/src:Z \
  -v ./ui:/app/ui:Z \
  -v ./templates:/app/templates:Z \
  art-code-gen:latest
```

3. Run with custom resource limits:
```bash
podman run -d \
  --name art-code-gen \
  -p 8000:8000 \
  -p 3000:3000 \
  --env-file .env \
  --memory=2g \
  --cpus=2 \
  art-code-gen:latest
```

## Container Management

1. View running containers:
```bash
podman ps
```

2. View container logs:
```bash
# View logs
podman logs art-code-gen

# Follow logs
podman logs -f art-code-gen

# View last N lines
podman logs --tail 100 art-code-gen
```

3. Execute commands in container:
```bash
# Open shell
podman exec -it art-code-gen /bin/bash

# Run specific command
podman exec art-code-gen python -m pytest
```

4. Stop and remove container:
```bash
# Stop container
podman stop art-code-gen

# Remove container
podman rm art-code-gen

# Force remove running container
podman rm -f art-code-gen
```

## Using Podman Compose

1. Create a `podman-compose.yml` file:
```yaml
version: '3'
services:
  app:
    build: .
    ports:
      - "8000:8000"
      - "3000:3000"
    env_file: .env
    volumes:
      - ./src:/app/src:Z
      - ./ui:/app/ui:Z
      - ./templates:/app/templates:Z
```

2. Start services:
```bash
podman-compose up -d
```

3. Stop services:
```bash
podman-compose down
```

## Container Health Checks

1. View container health:
```bash
podman healthcheck run art-code-gen
```

2. View container stats:
```bash
podman stats art-code-gen
```

## Troubleshooting

1. Container fails to start:
```bash
# Check container logs
podman logs art-code-gen

# Check container status
podman inspect art-code-gen
```

2. Permission issues:
```bash
# Fix SELinux context
chcon -R system_u:object_r:container_file_t:s0 ./src
chcon -R system_u:object_r:container_file_t:s0 ./ui
```

3. Network issues:
```bash
# Check container network
podman network ls
podman network inspect art-code-gen_default
```

## Additional Resources

- [Podman Documentation](https://docs.podman.io/en/latest/)
- [Podman Compose Documentation](https://github.com/containers/podman-compose)
- [Project Documentation](../README.md) 