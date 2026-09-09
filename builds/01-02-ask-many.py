# Asks a model several questions in a row and reports on the batch.
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

questions = [
    "In one sentence, what is an API rate limit?",
    "In one sentence, what is a token?",
    "",
    "In one sentence, why do API keys go in .env files?",
]

results = []
skipped = 0
total_output_tokens = 0

for i, question in enumerate(questions, start=1):
    print(f"Question {i} of {len(questions)}")

    if not question.strip():
        print("  (blank - skipped, no API call)\n")
        skipped = skipped + 1
        continue

    message = client.messages.create(
        model="claude-opus-5",
        max_tokens=150,
        messages=[{"role": "user", "content": question}],
    )

    answer = ""
    for block in message.content:
        if block.type == "text":
            answer = answer + block.text

    print(f"  Q: {question}")
    print(f"  A: {answer}\n")

    results.append(answer)
    total_output_tokens = total_output_tokens + message.usage.output_tokens

print("---")
print(f"Asked:   {len(results)}")
print(f"Skipped: {skipped}")
print(f"Total output tokens: {total_output_tokens}")

