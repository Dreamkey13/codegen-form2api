# Environment Configuration

This guide explains how to configure the ART Code Generation System using environment variables.

## Configuration File

Create a `.env` file in the project root based on `.env.example`:

```bash
cp .env.example .env
```

## Configuration Sections

### LLM Configuration
```env
# OpenAI API key for LLM access
OPENAI_API_KEY=your_openai_api_key_here

# LLM model to use (e.g., gpt-4, gpt-3.5-turbo)
LLM_MODEL=gpt-4

# Maximum tokens for LLM responses
LLM_MAX_TOKENS=4096

# Temperature for LLM responses (0.0 to 1.0)
LLM_TEMPERATURE=0.7
```

### API Configuration
```env
# Host address for the API server
API_HOST=0.0.0.0

# Port for the API server
API_PORT=8000

# Number of worker processes
API_WORKERS=4

# Enable auto-reload for development
API_RELOAD=true
```

### Web Navigation Configuration
```env
# Run browser in headless mode
BROWSER_HEADLESS=true

# Timeout for browser operations (milliseconds)
BROWSER_TIMEOUT=30000

# Browser viewport dimensions
BROWSER_VIEWPORT_WIDTH=1280
BROWSER_VIEWPORT_HEIGHT=800
```

### Logging Configuration
```env
# Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO

# Log message format
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s

# Log file path
LOG_FILE=app.log
```

### Security Configuration
```env
# Allowed CORS origins
CORS_ORIGINS=["http://localhost:3000"]

# API key header name
API_KEY_HEADER=X-API-Key

# API key for authentication
API_KEY=your_api_key_here
```

### Memory Configuration
```env
# Type of memory store (file, redis, etc.)
MEMORY_STORE_TYPE=file

# Path for file-based memory store
MEMORY_STORE_PATH=./data/memory

# Maximum number of items in memory store
MEMORY_MAX_SIZE=1000
```

### Development Configuration
```env
# Enable debug mode
DEBUG=false

# Environment (development, production)
ENVIRONMENT=development
```

## Configuration Validation

The system validates the configuration on startup. Common validation errors include:

1. Missing required variables
2. Invalid values for numeric fields
3. Invalid boolean values
4. Invalid JSON arrays

## Environment-Specific Configuration

### Development
- Set `ENVIRONMENT=development`
- Enable `API_RELOAD=true`
- Set `DEBUG=true`
- Use local memory store

### Production
- Set `ENVIRONMENT=production`
- Disable `API_RELOAD`
- Set `DEBUG=false`
- Use persistent memory store
- Configure proper security settings

## Security Considerations

1. Never commit `.env` files to version control
2. Use strong API keys
3. Restrict CORS origins in production
4. Use secure memory store in production
5. Enable HTTPS in production

## Additional Resources

- [Project Documentation](../README.md)
- [API Documentation](api.md)
- [Deployment Guide](deployment.md) 