import json
from openai import AsyncOpenAI
from app.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

SYSTEM_PROMPT = """You are an intelligent assistant that extracts structured data from student study voice messages.

The input will be a transcribed sentence from a voice message.

The sentence format is usually:
"{student name} studied {hours} hours a day"

Extract:
- student_name (string)
- hours_per_day (number)

Return output strictly in JSON format like this:

{
  "student_name": "Rahul",
  "hours_per_day": 5
}

If the format is unclear, still try your best to infer.
Do not return anything except JSON."""


async def extract_student_data(transcribed_text: str) -> dict:
    """
    Extract structured student data from transcribed text using GPT.

    Args:
        transcribed_text: The text output from Whisper transcription.

    Returns:
        Dictionary with 'student_name' and 'hours_per_day' keys.
    """
    response = await client.chat.completions.create(
        model=settings.GPT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": transcribed_text},
        ],
        response_format={"type": "json_object"},
        temperature=0,  # Deterministic output for structured extraction
    )

    result = json.loads(response.choices[0].message.content)
    return result
