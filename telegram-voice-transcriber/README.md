# 🎙️ Telegram Voice Transcriber

A FastAPI-powered Telegram bot that transcribes voice messages and extracts structured student study data using OpenAI Whisper + GPT.

## 🔄 How It Works

```
User sends voice message → Telegram Webhook → FastAPI
                                                  │
                                    ┌─────────────┼─────────────┐
                                    ▼             ▼             ▼
                               Download      Transcribe     Extract
                              (.ogg file)   (Whisper API)  (GPT-4o-mini)
                                                              │
                                                              ▼
                                                   JSON response sent
                                                   back to Telegram
```

**Example:**
- 🎤 Voice: *"Rahul studied 5 hours a day"*
- 📝 Transcription: `Rahul studied 5 hours a day`
- 📊 Extracted:
```json
{
  "student_name": "Rahul",
  "hours_per_day": 5
}
```

---

## 📦 Tech Stack

| Technology | Purpose |
|---|---|
| **FastAPI** | Web framework (webhook server) |
| **Uvicorn** | ASGI server |
| **OpenAI Whisper API** | Speech-to-text transcription |
| **OpenAI GPT-4o-mini** | Structured data extraction |
| **httpx** | Async HTTP client for Telegram API |
| **python-dotenv** | Environment variable management |

---

## 🚀 Setup & Run

### 1. Install dependencies

```bash
cd telegram-voice-transcriber
pip install -r requirements.txt
```

### 2. Configure environment variables

Edit the `.env` file:

```env
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
OPENAI_API_KEY=your-openai-api-key
WEBHOOK_URL=https://your-public-url.ngrok-free.app
```

**Getting your tokens:**
- **Telegram Bot Token**: Message [@BotFather](https://t.me/BotFather) on Telegram → `/newbot`
- **OpenAI API Key**: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### 3. Start the server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Expose locally with ngrok (for development)

```bash
ngrok http 8000
```

Copy the `https://xxxx.ngrok-free.app` URL and either:
- Set it in `.env` as `WEBHOOK_URL` and restart the server, OR
- Call the manual endpoint:
```bash
curl -X POST "http://localhost:8000/set-webhook?url=https://xxxx.ngrok-free.app"
```

### 5. Test it!

Open your bot in Telegram and send a voice message. 🎤

---

## 📁 Project Structure

```
telegram-voice-transcriber/
├── app/
│   ├── main.py            # FastAPI app + webhook endpoint
│   ├── telegram_bot.py    # Telegram API interactions (download, send)
│   ├── transcriber.py     # OpenAI Whisper transcription
│   ├── parser.py          # GPT-4o-mini data extraction
│   └── config.py          # Settings & environment variables
├── downloads/             # Temporary voice file storage
├── requirements.txt
├── .env                   # API keys (not committed to git)
└── README.md
```

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check / status |
| `GET` | `/health` | Health check |
| `POST` | `/webhook` | Telegram webhook (receives updates) |
| `POST` | `/set-webhook?url=<URL>` | Manually register webhook with Telegram |
