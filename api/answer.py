from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests, os
from openai import OpenAI

# Load key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# Enable CORS for your site
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.aitechdisruptors.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

site_pages = [
    "https://www.aitechdisruptors.com",
    "https://www.aitechdisruptors.com/news",
    "https://www.aitechdisruptors.com/playbook",
    "https://www.aitechdisruptors.com/blog"
]

site_kb = ""

def build_kb():
    global site_kb
    if site_kb:
        return site_kb
    kb = ""
    for url in site_pages:
        try:
            html = requests.get(url, timeout=10).text
            text = html.replace("<", " ").replace(">", " ")
            kb += f"\n\n### Source: {url}\n{text[:2000]}"
        except Exception as e:
            kb += f"\n\n### Source: {url}\n[Could not fetch: {e}]"
    site_kb = kb
    return kb

@app.post("/api/answer")
async def answer(request: Request):
    try:
        body = await request.json()
        question = body.get("question")
        voice = body.get("voice", "alloy")

        if not question:
            return JSONResponse({"error": "Missing question"}, status_code=400)

        context = build_kb()

        # 🆕 Compatible with OpenAI Python 1.x
        chat = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are the AI Tech Disruptors assistant. Use ONLY this context:\n" + context},
                {"role": "user", "content": question}
            ]
        )
        answer_text = chat.choices[0].message.content

        # 🆕 TTS syntax for new client
        speech = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice=voice,
            input=answer_text
        )

        return JSONResponse({
            "answer": answer_text,
            "audioUrl": "data:audio/mp3;base64," + speech.to_dict()["data"]
        })

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
