import os
import httpx
from app.config import settings

TELEGRAM_API_BASE = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}"
TELEGRAM_FILE_BASE = (
    f"https://api.telegram.org/file/bot{settings.TELEGRAM_BOT_TOKEN}"
)


async def download_voice_file(file_id: str) -> str:
    """
    Download a voice message from Telegram servers.

    1. Call getFile to get the file_path on Telegram's servers.
    2. Download the actual file bytes.
    3. Save locally to /downloads/{file_id}.ogg

    Returns the local file path.
    """
    async with httpx.AsyncClient() as client:
        # Step 1: Get file metadata from Telegram
        response = await client.get(
            f"{TELEGRAM_API_BASE}/getFile", params={"file_id": file_id}
        )
        response.raise_for_status()
        file_path = response.json()["result"]["file_path"]

        # Step 2: Download the actual file
        file_url = f"{TELEGRAM_FILE_BASE}/{file_path}"
        file_response = await client.get(file_url)
        file_response.raise_for_status()

        # Step 3: Save to local downloads directory
        local_path = os.path.join(settings.DOWNLOADS_DIR, f"{file_id}.ogg")
        with open(local_path, "wb") as f:
            f.write(file_response.content)

    return local_path


async def send_message(chat_id: int, text: str, parse_mode: str = "Markdown") -> dict:
    """Send a text message to a Telegram chat."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{TELEGRAM_API_BASE}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": parse_mode,
            },
        )
        response.raise_for_status()
        return response.json()


async def set_webhook(webhook_url: str) -> dict:
    """Register a webhook URL with Telegram."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{TELEGRAM_API_BASE}/setWebhook",
            json={"url": f"{webhook_url}/webhook"},
        )
        response.raise_for_status()
        return response.json()


async def delete_webhook() -> dict:
    """Remove the current webhook from Telegram."""
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{TELEGRAM_API_BASE}/deleteWebhook")
        response.raise_for_status()
        return response.json()
