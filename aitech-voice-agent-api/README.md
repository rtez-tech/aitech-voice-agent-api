# AI Tech Voice Agent API

🚀 AI-powered conversational API with support for:

* Chat (GPT-)
* Speech → Text (Whisper)
* Text → Speech (gpt-4o-min)

### Deploy on Vercel

1. Fork/clone this repo
2. Add env var on Vercel:
   OPENAI\_API\_KEY=your\_api\_key
3. Deploy → your endpoints:

   * POST /api/index → chat agent
   * POST /api/stt → speech to text
   * POST /api/tts → text to speech
