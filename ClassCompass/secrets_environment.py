import environ
from pathlib import Path

# Create an environment reader object
# This object knows how to load key=value pairs from .env
# and expose them as OS environment variables.
env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env from project root
environ.Env.read_env(BASE_DIR / ".env")