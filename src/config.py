import os

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DOTENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(dotenv_path=DOTENV_PATH)

# Cloud Provider
PROVIDER = "ON_PREMISE"

# MongoDB
MONGODB_URL = os.getenv(
    "MONGODB_URL", "mongodb://tokenrtvr:development-tokenrtvr@localhost:27017"
)
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "tolkien-retriever")

# MinIO
MINIO_ENDPOINT_URL = os.getenv("MINIO_ENDPOINT_URL", "localhost:9000")
MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER", "tokenrtvr")
MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD", "development-tokenrtvr")
MINIO_BUCKET_DOCUMENTS = os.getenv("MINIO_BUCKET_DOCUMENTS", "rulebooks")

# Qdrant
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
RULEBOOK_COLLETION = os.getenv("RULEBOOK_COLLETION", "rulebooks")

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
EMBEDDING_MODEL = os.getenv("EMBEDDINGS_MODEL", "text-embedding-3-small")

# LangSmith
os.environ.setdefault("LANGCHAIN_TRACING_V2", "false")
os.environ.setdefault("LANGCHAIN_API_KEY", "")
os.environ.setdefault("LANGCHAIN_PROJECT", "tolkien-retriever")
