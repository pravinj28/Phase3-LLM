from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

prompt = "Complete this sentence in one line: The sky is"

for temp in [0.0, 0.7, 1.5]:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=temp,
        max_tokens=30
    )
    print(f"Temperature {temp}: {response.choices[0].message.content}")
    print("---")


prompt = "What is 2 + 2? Answer with just the number."

for temp in [0.0, 1.5, 2.0]:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=temp,
        max_tokens=10
    )
    print(f"Temperature {temp}: {response.choices[0].message.content}")

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "user", "content": "My name is Pravin"},
        {"role": "assistant", "content": "Nice to meet you Pravin!"},
        {"role": "user", "content": "What is my name?"}
    ],
    max_tokens=50
)
print(response.choices[0].message.content)

for top_p in [0.1, 0.5, 1.0]:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "Name a random animal"}],
        temperature=1.0,
        top_p=top_p,
        max_tokens=10
    )
    print(f"top_p {top_p}: {response.choices[0].message.content}")