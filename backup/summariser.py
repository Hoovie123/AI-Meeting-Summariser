from ollama import chat

print("Reading transcript.txt...")

with open("transcript.txt", "r", encoding="utf-8") as file:
    transcript = file.read()

print("received")
print("loading ai model...\n")

stream = chat(
    model='qwen3:0.6b',
    think=False,
    messages=[
        {
            'role': 'user',
            'content': (
                "Summarize this transcript into concise, factual bullet points "
                "(only include updates, deadlines, or decisions if they are actually mentioned). "
                "Stop once all main points are covered. Do not invent placeholders:\n\n"
                f"{transcript}\n\n/no_think\n\n"
                "Key Takeaways:\n"
            ),
        },
    ],
    options={
        'temperature': 0.1,
        'num_ctx': 2048,
        'num_thread': 4,
        'num_predict': 200,
        'repeat_penalty': 1.15,
    },
    stream=True,
    keep_alive=0,
)

for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)

print()

