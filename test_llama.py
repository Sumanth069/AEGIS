import ollama

response = ollama.chat(
    model="llama3",
    messages=[
        {"role": "user", "content": "Explain financial fraud risk in banking"}
    ]
)

print(response["message"]["content"])