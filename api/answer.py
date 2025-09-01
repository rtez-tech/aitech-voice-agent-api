import base64

@app.post("/api/answer")
async def answer(request: Request):
    try:
        body = await request.json()
        question = body.get("question")
        voice = body.get("voice", "alloy")

        if not question:
            return JSONResponse({"error": "Missing question"}, status_code=400)

        context = build_kb()

        # Chat response
        chat = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are the AI Tech Disruptors assistant. Use ONLY this context:\n" + context},
                {"role": "user", "content": question}
            ]
        )
        answer_text = chat.choices[0].message.content

        # ✅ Correct way to capture audio as base64
        with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice=voice,
            input=answer_text
        ) as response:
            audio_bytes = response.read()

        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

        return JSONResponse({
            "answer": answer_text,
            "audioUrl": "data:audio/mp3;base64," + audio_base64
        })

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
