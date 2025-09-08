import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

export default async function handler(req, res) {
  if (req.method === "POST") {
    try {
      const { messages } = req.body;

      const response = await client.chat.completions.create({
        model: "gpt-4o-mini",
        messages,
        temperature: 0.7
      });

      res.status(200).json({
        reply: response.choices[0].message.content
      });
    } catch (error) {
      console.error("Agent Error:", error);
      res.status(500).json({ error: "AI Agent Error" });
    }
  } else {
    res.status(405).json({ error: "Method Not Allowed" });
  }
}