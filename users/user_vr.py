# users/user_alex.py
# MATCH — username (без @)
MATCH = "alex"  # отвечает пользователю с username @alex

# Пример reply = callable (sync)
import datetime
def time_reply(message):
    return f"Текущее время сервера: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

RULES = [
    {"type": "equals", "value": "время", "reply": time reply},
    {"type": "contains", "value": "спасибо", "reply": "Пожалуйста! Рад помочь."},
]
