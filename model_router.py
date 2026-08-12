from litellm import completion
import os
from dotenv import load_dotenv

load_dotenv()

def call_model(prompt, model="groq/llama-3.1-8b-instant", temperature=0.7):
    response = completion(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    return {
        "content": response.choices[0].message.content,
        "tokens": response.usage.total_tokens,
        "model": model
    }

# Test with Groq
result = call_model("What is RAG in AI?")
print(result)

# Test with OpenAI if you have credits
# result = call_model("What is RAG in AI?", model="gpt-3.5-turbo")
# print(result)