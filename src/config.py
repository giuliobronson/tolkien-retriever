import os

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DOTENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(dotenv_path=DOTENV_PATH)

PROVIDER = "ON_PREMISE"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MINIO_ENDPOINT_URL = os.getenv("MINIO_ENDPOINT_URL", "")
MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER", "")
MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD", "")
MINIO_BUCKET_DOCUMENTS = "rulebooks"
MONGODB_URL = os.getenv(
    "MONGODB_URL", "mongodb://tokenrtvr:development-tokenrtvr@localhost:27017"
)
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "tolkien-retriever")
