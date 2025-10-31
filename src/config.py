import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(__file__)) 
DOTENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(dotenv_path=DOTENV_PATH)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
