#claude-opus-5 asking a question
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Client()

dream = input("What is your dream? ")

message = client.messages.create(
    model = "claude-opus-5",
    max_tokens = 300,
    messages = [
        {"role": "user", "content": dream}

    ],
)

for block in message.content:
    if block.type == "text":
        print(block.text)


print()
print("stop_reason:", message.stop_reason)
print("input tokens:", message.usage.input_tokens)
print("output tokens:", message.usage.output_tokens)