# users/user_123456789.py
# MATCH — user_id (int)
MATCH = 123456789  # замените на реальный id пользователя

# Можно определить async/sync handle(client, message)
# Пример простого handle, который использует client для отправки медиа и возвращает None
async def handle(client, message):
    text = message.text or ""
    if "привет" in text.lower():
        await message.reply_text("Привет! Это ответ из кастомного handler.", quote=True)
        return None
    # Если вернуть строку — main отправит её автоматически
    if text.strip().lower() == "ping":
        return "pong"
    return None

# Или альтернативно — определить RULES (не используйте handle и RULES одновременно обычно)
RULES = [
    {"type": "contains", "value": "спроси", "reply": "Я получил ваш запрос и скоро отвечу."},
    {"type": "equals", "value": "ping", "reply": "pong"},
    {"type": "any", "value": None, "reply": "Автоответ от пользователя 123456789"},
]
