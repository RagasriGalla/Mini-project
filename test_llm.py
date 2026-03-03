import ollama

response = ollama.chat(
    model="llama3",
    messages=[
        {
            "role": "user",
            "content": "Hello AI, are you working?"
        }
    ]
)

print(response["message"]["content"])
