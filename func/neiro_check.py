
# ##################################
import requests
from decouple import config

# читаем из .env
OPENROUTER_URL = config('OPENROUTER_URL', default=None)
OPENROUTER_KEY = config('OPENROUTER_KEY', default=None)

if not OPENROUTER_URL or not OPENROUTER_KEY:
    raise RuntimeError("Не найдены OPENROUTER_URL или OPENROUTER_KEY в .env")

def neiro_check(text):
    payload = {
        "model": "deepseek/deepseek-v3.2",
        "messages": [
            {
                "role": "user",
                "content": (
                    f"Ты выполняешь роль помощника-ассистента по работе с текстом. Прочитай предложенный текст, укажи на ошибки и не понятности в тексте. Если смысл текста не ясен опиши, что не обходимо уточнить. В конце разбора можешь предложить переделанный финальный вариант текста '{text}'"
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
