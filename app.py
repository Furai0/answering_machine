import os
import pkgutil
import importlib
from pyrogram import Client, filters

API_ID = int(os.getenv("API_ID") or 0)
API_HASH = os.getenv("API_HASH")

if not API_ID or not API_HASH:
    raise RuntimeError("Set API_ID and API_HASH environment variables")

app = Client("asduserasdbot", api_id=API_ID, api_hash=API_HASH)

# Динамически загружаем все модули из папки handlers
handlers = {}  # ключ: USER (int id или string username), значение: модуль

for finder, name, ispkg in pkgutil.iter_modules(["handlers"]):
    module = importlib.import_module(f"handlers.{name}")
    if hasattr(module, "USER") and hasattr(module, "handle"):
        handlers[module.USER] = module

# Список пользователей для фильтрации (pyrogram фильтр принимает int/str)
user_list = list(handlers.keys())

@app.on_message(filters.private & filters.incoming & filters.user(user_list))
async def _on_message(client, message):
    sender = message.from_user
    if sender is None:
        return

    # Попробуем найти обработчик по id или по username (без @)
    handler = handlers.get(sender.id)
    if handler is None and sender.username:
        handler = handlers.get(sender.username) or handlers.get("@" + sender.username)

    if handler is None:
        # защищённый случай — ничего не делать
        return

    try:
        # каждый handler реализует async def handle(client, message)
        await handler.handle(client, message)
    except Exception as e:
        # простая обработка ошибок — лог в чат админа или в stdout
        print(f"Error in handler {handler}: {e}")
        # можно отправить уведомление себе:
        # await client.send_message("me", f"Handler error: {e}")

if __name__ == "__main__":
    print("Starting userbot...")
    app.run()
