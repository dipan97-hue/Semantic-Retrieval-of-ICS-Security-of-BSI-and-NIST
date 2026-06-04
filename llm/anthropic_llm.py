import os 
from anthropic import Anthropic
from config.config import ANTHROPIC_API_KEY
## Get the Key
client = Anthropic(api_key = ANTHROPIC_API_KEY)

def claude(prompt):
    model_name = "claude-sonnet-4-6"
    response = client.messages.create(
        model=model_name,
        max_tokens=1024,
        system="You are a cybersecurity expert in industrial control systems (ICS).",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    return response.content[0].text