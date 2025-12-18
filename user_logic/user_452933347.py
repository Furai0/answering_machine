from dicts import words
import re
import requests
import json
from func.neiro_punch_vr import neiro_punch
from func.neiro_check import neiro_check
from func.mat_search import mat_search
from func.mat_search import mats
from func.bug_report import bug_report

KNOWN = set(w.lower() for w in words.words)  # быстрее, чем list
async def handle_message(client, message):
    
    text = (message.text or "").lower()

    words = re.findall(r"[а-яё]+", text)  # достаём только русские слова

    for word in words:
        if word not in KNOWN:
            if mat_search(word) == True:
                print('mat_search(word)[0]')
                await message.reply_text(f'матернулась хехе ({word})')    
            else:
                await message.reply_text(f'Слово "{word}" не найдено в базе в 150 000 слов, из-за чего сообщение не будет доставлено.\nЕсли слова ошибочно нет в базе, пропиши /bug_report и в том же сообщении напиши об ошибке.\nЕсли это просто опечатка ебаная - напиши блять по человечески')
                await message.reply_text(neiro_punch(word))
    if len(words) > 20:
        await message.reply_text('Обрати внимание, что в твоем сообщении больше 20 слов. Нейросеть его проанализирует и подскажет, как его подправить, чтобы оно стало более читабельным')
        await message.reply_text(neiro_check(message.text))


    if "/bug_report" in message.text.lower():
        await message.reply_text("Сообщение об ошибке записано и я постараюсь учесть его в дальнейшем")

    if "погода" in message.text.lower():
        await message.reply_text("Погода сегодня отличная!")


