from dicts import words
import re
import requests
import json
from func.neiro_punch_vr import neiro_punch
KNOWN = set(w.lower() for w in words.words)  # быстрее, чем list
async def handle_message(client, message):
    
    text = (message.text or "").lower()

    words = re.findall(r"[а-яё]+", text)  # достаём только русские слова

    for word in words:
        if word not in KNOWN:
            await message.reply_text(f'Это что за слово {word}')
            await message.reply_text(neiro_punch(word))
    if "погода" in message.text.lower():
        await message.reply_text("Погода сегодня отличная!")


