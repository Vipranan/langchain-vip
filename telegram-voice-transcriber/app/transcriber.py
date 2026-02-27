from openai import AsyncOpenAI
from app.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def transcribe_audio(file_path: str) -> str:
    """
    Transcribe an audio file using OpenAI Whisper API.

    Args:
        file_path: Local path to the audio file (.ogg, .mp3, .wav, etc.)

    Returns:
        Transcribed text string.
    """
    with open(file_path, "rb") as audio_file:
        transcript = await client.audio.transcriptions.create(
            model=settings.WHISPER_MODEL,
            file=audio_file,
            language="en",  # Optimize for English; remove for auto-detect
        )

    return transcript.text
