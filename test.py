from decouple import config
from pyrogram import Client, filters

import os
import importlib

# Загрузка конфигурации из .env
api_id = config('API_ID')
api_hash = config('API_HASH')
phone = config('PHONE') # Может не использоваться напрямую, но полезно для первой авторизации
session_name = config('LOGIN') # Имя сессии

# Инициализация клиента Pyrogram
app = Client(session_name, api_id, api_hash)

# --- Логика ответов для разных пользователей ---

# Создадим папку для логики, если ее нет
if not os.path.exists("user_logic"):
    os.makedirs("user_logic")

# Пример файла user_logic/user_12345.py
# Содержимое user_logic/user_12345.py:
'''
async def handle_message(client, message):
    if "привет" in message.text.lower():
        await message.reply_text("Привет, пользователь 12345! Как дела?")
    elif "как зовут" in message.text.lower():
        await message.reply_text("Меня зовут Бот, а тебя?")
    else:
        await message.reply_text("Я получил твое сообщение, пользователь 12345.")
'''

# Словарь для хранения логики по ID пользователя
user_handlers = {}

# Загрузка логики из файлов
def load_user_logic():
    for filename in os.listdir("user_logic"):
        if filename.endswith(".py"):
            user_id_str = filename.replace("user_", "").replace(".py", "")
            try:
                user_id = int(user_id_str)
                module_name = f"user_logic.{user_id_str}"
                spec = importlib.util.spec_from_file_location(module_name, os.path.join("user_logic", filename))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, "handle_message"):
                    user_handlers[user_id] = module.handle_message
                    print(f"Загружена логика для пользователя ID: {user_id}")
                else:
                    print(f"Файл {filename} не содержит функцию handle_message.")
            except ValueError:
                print(f"Некорректное имя файла логики: {filename}")
            except Exception as e:
                print(f"Ошибка при загрузке логики из {filename}: {e}")

# Загружаем логику при старте
load_user_logic()


@app.on_message(filters.private & filters.text)
async def auto_reply_to_specific_users(client, message):
    user_id = message.from_user.id
    print(f"Получено сообщение от пользователя {user_id}: {message.text}")

    if user_id in user_handlers:
        # Если для этого пользователя есть специальная логика, используем ее
        await user_handlers[user_id](client, message)
    else:
        # Общая логика для всех остальных пользователей
        # await message.reply_text("Извините, я не настроен отвечать на ваши сообщения.")
        pass # Или ничего не отвечать

# Запуск бота
print("Бот запущен. Ожидание сообщений...")
app.run()
