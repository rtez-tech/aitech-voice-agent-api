import OpenAI from "openai";

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export default async function handler(req, res) {
  try {
    // In production you may need a file parser like multer
    const transcript = await client.audio.transcriptions.create({
      model: "whisper-1",
      file: req.body.file
    });
    res.status(200).json({ text: transcript.text });
  } catch (error) {
    console.error("STT Error:", error);
    res.status(500).json({ error: "STT Failed" });
  }
}