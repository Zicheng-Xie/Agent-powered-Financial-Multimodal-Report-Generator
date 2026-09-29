"""DeepSeek credentials for the local LLM requester."""
import os
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_CODE = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_URL = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
