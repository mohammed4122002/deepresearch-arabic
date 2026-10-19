import os

from dotenv import load_dotenv

load_dotenv()

LLM_MODEL = os.getenv("LLM_MODEL", "qwen2.5:1.5b")
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY", "")