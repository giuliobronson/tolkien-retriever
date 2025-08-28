import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Exporta as variáveis de ambiente
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY", "")
LANGSMITH_API_URL = os.getenv("LANGSMITH_API_URL", "https://api.smith.langchain.com")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MINIO_ENDPOINT_URL = os.getenv("MINIO_ENDPOINT_URL", "http://localhost:9000")
MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER", "")
MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD", "")