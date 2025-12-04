# Uvicorn Server Commands

Quick reference for running the OCR API server with uvicorn.

## Basic Commands

### Development (with auto-reload)
```bash
# Using Python script
python run_server.py --reload

# Direct uvicorn command
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### Production
```bash
# Using Python script
python run_server.py --host 0.0.0.0 --port 8000

# Direct uvicorn command
uvicorn api:app --host 0.0.0.0 --port 8000
```

### Custom Port
```bash
# Using Python script
python run_server.py --port 8080

# Direct uvicorn command
uvicorn api:app --host 0.0.0.0 --port 8080
```

### Localhost Only
```bash
# Using Python script
python run_server.py --host 127.0.0.1

# Direct uvicorn command
uvicorn api:app --host 127.0.0.1 --port 8000
```

## Advanced Options

### Debug Mode (verbose logging)
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --log-level debug --reload
```

### Production with Multiple Workers
**Note:** OCR models are memory-intensive. Use 1 worker unless you have sufficient GPU/RAM.

```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --workers 1
```

### Using Python Script with All Options
```bash
python run_server.py --host 0.0.0.0 --port 8000 --reload --log-level debug
```

## Quick Start (Recommended)

### For Development:
```bash
python run_server.py --reload
```

### For Production:
```bash
python run_server.py
```

## Environment Variables

You can also set these via environment variables:
```bash
# Windows PowerShell
$env:PORT=8080
$env:HOST="127.0.0.1"
python run_server.py

# Linux/Mac
export PORT=8080
export HOST=127.0.0.1
python run_server.py
```

## Common Use Cases

### 1. Local Development
```bash
uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

### 2. Testing from Other Devices (Same Network)
```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

### 3. Production Deployment
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --workers 1 --log-level info
```

### 4. Docker/Container
```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

## Troubleshooting

### Port Already in Use
```bash
# Use a different port
uvicorn api:app --port 8001
```

### Permission Denied (Linux/Mac)
```bash
# Use a port above 1024, or run with sudo
uvicorn api:app --port 8000
```

### Models Not Loading
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check that models initialize on startup (check server logs)

## Access Points

Once running, access:
- **API Root**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **Models Status**: http://localhost:8000/models
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

