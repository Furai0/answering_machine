import user_1488
import re
KNOWN = set(w.lower() for w in user_1488.words)  # быстрее, чем list
async def handle_message(client, message):
    
    text = (message.text or "").lower()

    words = re.findall(r"[а-яё]+", text)  # достаём только русские слова

    for word in words:
        if word not in KNOWN:
            await message.reply_text(f'Это что за слово {word}')
    
    if "погода" in message.text.lower():
        await message.reply_text("Погода сегодня отличная!")
    