from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

histories = {}

SYSTEM_PROMPT = """Kamu adalah asisten ai yang galak suka toxic dan sarkas serta tak kenal ampun, klo orang aneh dikit kamu kata katain dan marahin, kata kata kasar pasti keluar dalam tiap percakapan, seperti anjing kontol ngentot dan bangsat. tapi tetep, jawab yang masuk akal jangan jawab asal asalan."""

def chat(user_id: int, message: str) -> str:
    if user_id not in histories:
        histories[user_id] = []

    histories[user_id].append({"role": "user", "content": message})

    recent = histories[user_id][-20:]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + recent,
        max_tokens=1024,
    )

    reply = response.choices[0].message.content
    histories[user_id].append({"role": "assistant", "content": reply})
    return reply

def clear_history(user_id: int):
    histories.pop(user_id, None)
