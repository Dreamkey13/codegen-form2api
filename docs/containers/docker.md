# Docker Container Management

This guide explains how to build and manage containers for the ART Code Generation System using Docker.

## Prerequisites
- Docker 20.10 or later
- Docker Compose (optional, for multi-container setup)

## Building the Container

1. Build the container image:
```bash
# Build using Dockerfile
docker build -t art-code-gen:latest .

# Build with specific platform (if needed)
docker build --platform linux/amd64 -t art-code-gen:latest .
```

2. Build with custom build arguments:
```bash
docker build \
  --build-arg PYTHON_VERSION=3.9 \
  --build-arg NODE_VERSION=18 \
  -t art-code-gen:latest .
```

## Running the Container

1. Run in detached mode:
```bash
docker run -d \
  --name art-code-gen \
  -p 8000:8000 \
  -p 3000:3000 \
  --env-file .env \
  art-code-gen:latest
```

2. Run with volume mounts for development:
```bash
docker run -d \
  --name art-code-gen-dev \
  -p 8000:8000 \
  -p 3000:3000 \
  --env-file .env \
  -v ./src:/app/src \
  -v ./ui:/app/ui \
  -v ./templates:/app/templates \
  art-code-gen:latest
```

3. Run with custom resource limits:
```bash
docker run -d \
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
docker ps
```

2. View container logs:
```bash
# View logs
docker logs art-code-gen

# Follow logs
docker logs -f art-code-gen

# View last N lines
docker logs --tail 100 art-code-gen
```

3. Execute commands in container:
```bash
# Open shell
docker exec -it art-code-gen /bin/bash

# Run specific command
docker exec art-code-gen python -m pytest
```

4. Stop and remove container:
```bash
# Stop container
docker stop art-code-gen

# Remove container
docker rm art-code-gen

# Force remove running container
docker rm -f art-code-gen
```

## Using Docker Compose

1. Create a `docker-compose.yml` file:
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
      - ./src:/app/src
      - ./ui:/app/ui
      - ./templates:/app/templates
```

2. Start services:
```bash
docker-compose up -d
```

3. Stop services:
```bash
docker-compose down
```

## Container Health Checks

1. View container health:
```bash
docker inspect --format='{{.State.Health.Status}}' art-code-gen
```

2. View container stats:
```bash
docker stats art-code-gen
```

## Troubleshooting

1. Container fails to start:
```bash
# Check container logs
docker logs art-code-gen

# Check container status
docker inspect art-code-gen
```

2. Permission issues:
```bash
# Fix permissions
chmod -R 755 ./src
chmod -R 755 ./ui
```

3. Network issues:
```bash
# Check container network
docker network ls
docker network inspect art-code-gen_default
```

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Project Documentation](../README.md) 