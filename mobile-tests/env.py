import os

# Host configuration
HOST_CONFIG = {
    "API_HOST": "192.168.1.191",  # Your computer's IP address
    "FRONTEND_HOST": "192.168.1.191",  # Your computer's IP address
    "API_PORT": "3000",
    "FRONTEND_PORT": "4100"
}

def set_env_variables():
    """Set environment variables for the test run"""
    for key, value in HOST_CONFIG.items():
        os.environ[key] = value

# Set environment variables when this module is imported
set_env_variables() 