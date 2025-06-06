import os

# Frontend configuration
FRONTEND_HOST = os.getenv("FRONTEND_HOST", "localhost")
FRONTEND_PORT = os.getenv("FRONTEND_PORT", "4100")
BASE_URL = f"http://{FRONTEND_HOST}:{FRONTEND_PORT}"

# API configuration
API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = os.getenv("API_PORT", "3000")
API_URL = f"http://{API_HOST}:{API_PORT}"
