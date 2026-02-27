import json
import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import settings
from app.telegram_bot import download_voice_file, send_message, set_webhook
from app.transcriber import transcribe_audio
from app.parser import extract_student_data

# ─── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-8s │ %(message)s",
)
logger = logging.getLogger(__name__)


# ─── Lifespan (startup / shutdown) ────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Register the Telegram webhook on startup if WEBHOOK_URL is set."""
    if settings.WEBHOOK_URL:
        result = await set_webhook(settings.WEBHOOK_URL)
        logger.info(f"✅ Webhook registered: {result}")
    else:
        logger.warning(
            "⚠️  WEBHOOK_URL not set. Set it in .env and restart, "
            "or manually POST to /set-webhook?url=<your-url>"
        )
    yield
    logger.info("🛑 Shutting down...")


# ─── FastAPI App ──────────────────────────────────────────────────────────────
app = FastAPI(
    title="Telegram Voice Transcriber",
    description="Transcribes Telegram voice messages and extracts structured student data.",
    version="1.0.0",
    lifespan=lifespan,
)


# ─── Health Check ─────────────────────────────────────────────────────────────
@app.get("/")
async def root():
    return {"status": "🟢 running", "app": "Telegram Voice Transcriber"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


# ─── Manual Webhook Setup ────────────────────────────────────────────────────
@app.post("/set-webhook")
async def register_webhook(url: str):
    """Manually set webhook URL. Useful if WEBHOOK_URL wasn't set at startup."""
    result = await set_webhook(url)
    return {"result": result}


# ─── Telegram Webhook Endpoint ───────────────────────────────────────────────
@app.post("/webhook")
async def telegram_webhook(request: Request):
    """
    Receives incoming updates from Telegram.

    Flow:
    1. Check if the message contains a voice note
    2. Download the voice file
    3. Transcribe with Whisper
    4. Extract structured data with GPT
    5. Send the result back to the user
    """
    update = await request.json()
    logger.info(f"📩 Incoming update: {json.dumps(update, indent=2)}")

    message = update.get("message", {})
    chat_id = message.get("chat", {}).get("id")

    if not chat_id:
        return JSONResponse({"ok": True})

    # ── Handle /start command ──────────────────────────────────────────────
    text = message.get("text", "")
    if text.startswith("/start"):
        await send_message(
            chat_id,
            "👋 *Welcome to the Voice Transcriber Bot!*\n\n"
            "Send me a voice message like:\n"
            '🎙️ _"Rahul studied 5 hours a day"_\n\n'
            "I'll transcribe it and extract the student's name and study hours.",
        )
        return JSONResponse({"ok": True})

    # ── Handle voice message ──────────────────────────────────────────────
    voice = message.get("voice")
    if not voice:
        await send_message(
            chat_id,
            "🎤 Please send a *voice message* so I can transcribe it.",
        )
        return JSONResponse({"ok": True})

    file_id = voice["file_id"]
    local_path = None

    try:
        # Step 1: Acknowledge
        await send_message(chat_id, "⏳ Processing your voice message...")

        # Step 2: Download voice file
        logger.info(f"⬇️  Downloading voice: {file_id}")
        local_path = await download_voice_file(file_id)
        logger.info(f"📁 Saved to: {local_path}")

        # Step 3: Transcribe with Whisper
        logger.info("🎙️ Transcribing audio...")
        transcribed_text = await transcribe_audio(local_path)
        logger.info(f"📝 Transcription: {transcribed_text}")

        # Step 4: Extract structured data with GPT
        logger.info("🧠 Extracting student data...")
        extracted_data = await extract_student_data(transcribed_text)
        logger.info(f"📊 Extracted: {extracted_data}")

        # Step 5: Send formatted response
        response_message = (
            f"📝 *Transcription:*\n_{transcribed_text}_\n\n"
            f"📊 *Extracted Data:*\n"
            f"```json\n{json.dumps(extracted_data, indent=2)}\n```"
        )
        await send_message(chat_id, response_message)

    except Exception as e:
        logger.error(f"❌ Error processing voice: {e}", exc_info=True)
        await send_message(
            chat_id,
            f"❌ Sorry, something went wrong:\n`{str(e)}`",
        )

    finally:
        # Cleanup: remove the downloaded file
        if local_path and os.path.exists(local_path):
            os.remove(local_path)
            logger.info(f"🗑️ Cleaned up: {local_path}")

    return JSONResponse({"ok": True})
