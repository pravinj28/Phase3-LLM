from litellm import completion
import os
from dotenv import load_dotenv
import time

load_dotenv()

# Model routing strategy
# Low complexity → fast cheap model
# High complexity → powerful model

MODELS = {
    "low": "groq/llama-3.1-8b-instant",
    "medium": "groq/llama-3.1-8b-instant",
    "high": "groq/llama-3.1-8b-instant"
}

def route_and_call(prompt: str, complexity: str = "low", temperature: float = 0.7):
    model = MODELS.get(complexity, MODELS["low"])
    
    start_time = time.time()
    
    response = completion(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=200
    )
    
    end_time = time.time()
    
    return {
        "content": response.choices[0].message.content,
        "model_used": model,
        "complexity": complexity,
        "tokens_used": response.usage.total_tokens,
        "latency_seconds": round(end_time - start_time, 2),
        "estimated_cost": response.usage.total_tokens * 0.000001
    }

# Test all 3 complexity levels
prompts = [
    ("What is 2 + 2?", "low"),
    ("Explain the difference between RAG and fine-tuning", "medium"),
    ("Design a production RAG system for a legal firm with 10000 employees", "high")
]

for prompt, complexity in prompts:
    print(f"\nComplexity: {complexity}")
    print(f"Prompt: {prompt}")
    result = route_and_call(prompt, complexity)
    print(f"Model: {result['model_used']}")
    print(f"Tokens: {result['tokens_used']}")
    print(f"Latency: {result['latency_seconds']}s")
    print(f"Response: {result['content'][:100]}...")
    print("---")