import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()



def ask(question, model = "claude-opus-5", max_tokens = 500):
    """ Send one question to the model and return the reply text."""
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages = [{"role": "user", "content": question}]
    )
    answer = "" 
    for block in message.content:
        if block.type == "text":
            answer = answer + block.text
    return answer

print(ask("Name three reasons for learning AI engineering."))
print(ask("say hello in binary if possibe", max_tokens = 35))