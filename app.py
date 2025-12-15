import os
from pyrogram import Client, filters
#  main
#  29446725 
#   f5d7ac4c7b94db8cb960b0ee97b28179 
#   twink
#   24215758
#   72558d64d89a02305632568149806d15
# main.py
# main.py
# main.py
import importlib
import logging
import pkgutil
import re
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from pyrogram import Client, filters
from pyrogram.types import Message
import config

api_id = getattr(config, "API_ID", None)
api_hash = getattr(config, "API_HASH", None)
if api_id is None or api_hash is None:
    raise RuntimeError("Не указаны API_ID/API_HASH в config.py")

session_string = getattr(config, "SESSION_STRING", None)
session_name = getattr(config, "SESSION_NAME", "userbot_session")

if session_string:
    app = Client(SESSION_NAME=session_string, api_id=api_id, api_hash=api_hash)
else:
    app = Client(SESSION_NAME=session_name, api_id=api_id, api_hash=api_hash)
# Конфигурация модулей пользователей загружается из пакета users
USER_MODULES: List[Dict[str, Any]] = []

def load_user_modules():
    """
    Загружает все модули users.user_*.py и собирает их MATCH / handle / RULES.
    """
    USER_MODULES.clear()
    import users  # пакет users
    package = users
    prefix = package.__name__ + "."
    for finder, name, ispkg in pkgutil.iter_modules(package.__path__, prefix):
        # ищем только модули, начинающиеся с users.user_
        if not name.split(".")[-1].startswith("user_"):
            continue
        try:
            module = importlib.import_module(name)
            importlib.reload(module)
        except Exception as e:
            log.exception("Не удалось импортировать %s: %s", name, e)
            continue

        match = getattr(module, "MATCH", None)
        handle = getattr(module, "handle", None)
        rules = getattr(module, "RULES", None)

        if match is None:
            log.warning("Модуль %s пропущен: нет MATCH", name)
            continue

        USER_MODULES.append({"match": match, "module": module, "handle": handle, "rules": rules})
        log.info("Загружен модуль %s (MATCH=%s)", name, match)

def sender_matches_key(sender, key) -> bool:
    """
Сравнение sender (User) и ключа (int id или str username).
    """
    try:
        if isinstance(key, int):
            return getattr(sender, "id", None) == key
        if isinstance(key, str):
            uname = getattr(sender, "username", None)
            if uname:
                return uname.lower() == key.lower().lstrip("@")
    except Exception:
        return False
    return False

async def apply_rules_and_get_reply(rules, message: Message) -> Optional[str]:
    """
    Проверяет список правил и возвращает строку-ответ или None.
    Поддерживает reply как строку или callable (sync/async) returning string or None.
    """
    text = message.text or ""
    for rule in rules:
        typ = rule.get("type")
        val = rule.get("value")
        reply = rule.get("reply")
        matched = False

        if typ == "any":
            matched = True
        elif typ == "contains" and val and val.lower() in text.lower():
            matched = True
        elif typ == "equals" and val and text.strip().lower() == str(val).strip().lower():
            matched = True
        elif typ == "regex" and val:
            try:
                if re.search(val, text, re.IGNORECASE):
                    matched = True
            except re.error:
                log.warning("Неверный regex в правиле: %s", val)
                matched = False

        if matched:
            if callable(reply):
                # поддержка sync/async callable
                try:
                    result = reply(message)
                    if hasattr(result, "__await__"):
                        result = await result
                    return result
                except Exception:
                    log.exception("Ошибка при вызове callable reply")
                    return None
            else:
                return str(reply) if reply is not None else None
    return None

@app.on_message(filters.private | filters.group | filters.channel)
async def auto_reply(client: Client, message: Message):
    # пропускаем свои сообщения
    me = await client.get_me()
    if not message.from_user or message.from_user.id == me.id:
        return

    # Найти модуль для отправителя
    target_module = None
    for entry in USER_MODULES:
        if sender_matches_key(message.from_user, entry["match"]):
            target_module = entry
            break

    if not target_module:
        return  # не на нужного пользователя

    module = target_module["module"]
    # Если есть handle — вызываем его.
    handle = target_module.get("handle")
    if handle:
        try:
            result = handle(client, message)
            if hasattr(result, "__await__"):
                result = await result
            # Если handle сам отправил ответ — он может вернуть None/False
            # Если handle вернул строку — отправим её как ответ
            if isinstance(result, str):
                await message.reply_text(result, quote=True)
        except Exception:
            log.exception("Ошибка в handle модуля %s", module.__name__)
        return

    # Иначе используем RULES, если есть
    rules = target_module.get("rules")
    if rules:
        try:
            reply_text = await apply_rules_and_get_reply(rules, message)
            if reply_text:await message.reply_text(reply_text, quote=True)
        except Exception:
            log.exception("Ошибка при применении RULES в модуле %s", module.__name__)

if __name__ == "__main__":
    # Загрузка модулей пользователей и запуск
    load_user_modules()
    print("Starting userbot...")
    app.run()


