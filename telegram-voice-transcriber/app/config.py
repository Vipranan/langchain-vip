import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    WEBHOOK_URL: str = os.getenv("WEBHOOK_URL", "")

    # Directory to store downloaded voice files temporarily
    DOWNLOADS_DIR: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "downloads"
    )

    # OpenAI models
    WHISPER_MODEL: str = "whisper-1"
    GPT_MODEL: str = "gpt-4o-mini"


settings = Settings()

# Ensure downloads directory exists
os.makedirs(settings.DOWNLOADS_DIR, exist_ok=True)
