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
import os
import importlib
import runpy
import types

user_handlers = {}

def load_user_logic():
    user_logic_dir = "user_logic"
    if not os.path.exists(user_logic_dir):
        os.makedirs(user_logic_dir)

    for filename in os.listdir(user_logic_dir):
        if not filename.endswith(".py"):
            continue

        user_id_str = filename.replace("user_", "").replace(".py", "")
        try:
            user_id = int(user_id_str)
        except ValueError:
            print(f"Некорректное имя файла логики: {filename}")
            continue

        module_name = f"user_logic.{user_id_str}"
        filepath = os.path.join(user_logic_dir, filename)
        module = None

        # Попытка 1: стандартный импорт через importlib.util
        try:
            # импортируем submodule явно — может выбросить AttributeError, если importlib "затенён"
            import importlib.util as importlib_util
            spec = importlib_util.spec_from_file_location(module_name, filepath)
            module = importlib_util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except Exception as e_util:
            # Попытка 2: fallback через runpy
            try:
                module = types.ModuleType(module_name)
                module.__dict__.update(runpy.run_path(filepath))
            except Exception as e_runpy:
                print(f"Ошибка при загрузке логики из {filename}: {e_util}; fallback также упал: {e_runpy}")
                continue

        # Проверяем наличие handle_message
        if hasattr(module, "handle_message"):
            user_handlers[user_id] = module.handle_message
            print(f"Загружена логика для пользователя ID: {user_id}")
        else:
            print(f"Файл {filename} не содержит функцию handle_message.")

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
