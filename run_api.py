"""Run the REST API server."""

import uvicorn
from src.config import config

if __name__ == '__main__':
    print(f"\nStarting API server on http://{config.API_HOST}:{config.API_PORT}\n")
    uvicorn.run(
        "src.api:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True
    )
