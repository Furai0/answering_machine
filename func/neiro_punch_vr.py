# import re
# import requests
# import json
# def neiro_punch(text):
#                         # First API call with reasoning
#             response = requests.post(
#             url="https://openrouter.ai/api/v1/chat/completions",
#             headers={
#                 "Authorization": "Bearer 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",
#                 "Content-Type": "application/json",
#             },
#             data=json.dumps({
#                 "model": "deepseek/deepseek-v3.2",
#                 "messages": [
#                     {
#                     "role": "user",
#                     "content": f"Ты вписан в код моего личного автоответчика для друзей. В случае их опечатки я хочу чтобы им автоматически приходил ответ. Напиши нудное гневное сообщение-упрек из-за опечатки в слове. Ошибочно написанное слово {text}, по возможности обыграй это в ответе. Напиши только само сообщение-упрек и ничего больше"
#                     }
#                 ],
#                 "reasoning": {"enabled": True}
#             })
#             )

#             # Extract the assistant message with reasoning_details
#             response = response.json()
#             response = response['choices'][0]['message']

#             for i, item in enumerate(response.get('reasoning_details', [])):
#                 text = item.get('text')
#                 return text


# ##################################
import requests
from decouple import config

# читаем из .env
OPENROUTER_URL = config('OPENROUTER_URL', default=None)
OPENROUTER_KEY = config('OPENROUTER_KEY', default=None)

if not OPENROUTER_URL or not OPENROUTER_KEY:
    raise RuntimeError("Не найдены OPENROUTER_URL или OPENROUTER_KEY в .env")

def neiro_punch(text):
    payload = {
        "model": "deepseek/deepseek-v3.2",
        "messages": [
            {
                "role": "user",
                "content": (
                    "Ты вписан в код моего личного автоответчика для друзей. "
                    "В случае их опечатки я хочу чтобы им автоматически приходил ответ. "
                    "Напиши нудное гневное сообщение-упрек из-за опечатки в слове. "
                    f"Ошибочно написанное слово {text}, по возможности обыграй это в ответе. "
                    "Напиши только само сообщение-упрек и ничего больше"
                )
            }
        ],
        "reasoning": {"enabled": True}
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }

    resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=15)
    resp.raise_for_status()
    j = resp.json()

    choice = j.get("choices", [{}])[0]
    message = choice.get("message", {}) or {}

    content = ""

    mc = message.get("content")
    if isinstance(mc, str):
        content = mc
    elif isinstance(mc, dict):
        if isinstance(mc.get("parts"), list) and mc["parts"]:
            content = mc["parts"][0]
        else:
            for k in ("text", "raw", "output_text", "content"):
                if isinstance(mc.get(k), str) and mc.get(k).strip():
                    content = mc[k]
                    break

    if not content:
        for item in reversed(message.get("reasoning_details", []) or []):
            if item.get("role") in ("assistant", None) and item.get("text"):
                content = item["text"]
                break

    if not content:
        content = choice.get("content") or choice.get("text") or ""

    return content.strip()
