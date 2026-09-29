"""Backend configuration loaded from the local environment."""
import os
from dotenv import load_dotenv

load_dotenv()

data = {
    "deepseek_api_key": os.environ.get("DEEPSEEK_API_KEY", ""),
}
