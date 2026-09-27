import anthropic
from dotenv import load_dotenv

load_dotenv()  # reads .env and sets env vars for this process

client = anthropic.Anthropic()
# The SDK automatically reads ANTHROPIC_API_KEY from the environment
# No need to pass the key manually

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=100,
    messages=[
        {"role": "user", "content": "Say hello in one word."}
    ]
)

print(response.content[0].text)  # Should print: Hello