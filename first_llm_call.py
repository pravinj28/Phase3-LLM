from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
    model = "llama-3.1-8b-instant",
    messages=[
        {"role": "system", "content": "You are a helpful assistance"},
        {"role": "user", "content" :"What is a large language model in 2 sentences?"}
    ],
    temperature = 0.7,
    max_tokens = 100
)

print(response.choices[0].message.content)
print(f"Tokens used: {response.usage.total_tokens}")

