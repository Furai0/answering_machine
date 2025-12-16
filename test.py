import requests
import json

# First API call with reasoning
response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": "Bearer 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",
    "Content-Type": "application/json",
  },
  data=json.dumps({
    "model": "deepseek/deepseek-v3.2",
    "messages": [
        {
          "role": "user",
          "content": "How many r's are in the word 'strawberry'?"
        }
      ],
    "reasoning": {"enabled": True}
  })
)

# Extract the assistant message with reasoning_details
response = response.json()
response = response['choices'][0]['message']

for i, item in enumerate(response.get('reasoning_details', [])):
    text = item.get('text')
    if text:
        print(f"[{i}] {text}")
    else:
        print(f"[{i}] (no 'text' field)")