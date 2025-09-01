from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests, openai, os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

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
            html = requests.get(url).text
            text = html.replace("<"," ").replace(">"," ")
            kb += f"\n\n### Source: {url}\n{text[:2000]}"
        except:
            kb += f"\n\n### Source: {url}\n[Could not fetch]"
    site_kb = kb
    return kb

@app.post("/api/answer")
async def answer(request: Request):
    body = await request.json()
    question = body.get("question")
    voice = body.get("voice","alloy")

    context = build_kb()

    chat = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are the AI Tech Disruptors assistant. Answer ONLY using this context:\n"+context},
            {"role": "user", "content": question}
        ]
    )
    answer_text = chat.choices[0].message.content

    # TTS
    speech = openai.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=answer_text
    )

    return JSONResponse({
        "answer": answer_text,
        "audioUrl": "data:audio/mp3;base64,"+speech["data"]
    })
