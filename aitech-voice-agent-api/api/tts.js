import OpenAI from "openai";

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export default async function handler(req, res) {
  try {
    const { text } = req.body;

    const audio = await client.audio.speech.create({
      model: "gpt-4o-mini-tts",
      voice: "verse",
      input: text
    });

    res.setHeader("Content-Type", "audio/mpeg");
    audio.pipe(res);
  } catch (error) {
    console.error("TTS Error:", error);
    res.status(500).json({ error: "TTS Failed" });
  }
}