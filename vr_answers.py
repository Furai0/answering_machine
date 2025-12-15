# reply_logic.py
import re
from typing import Iterable, Union

# Регулярка: допускает "привет" с ведущими/концевыми пробелами и простой пунктуацией
GREETING_RE = re.compile(r'^\s_привет\s_[!?.]_\s_$', re.IGNORECASE)

def normalize_allowed(allowed: Iterable[Union[int, str]]):
    """
    Приводит список разрешённых идентификаторов к виду:
      - целые числа (user_id) остаются числами
      - строки приводятся к lower() и без начального '@'
    """
    normalized = []
    for a in allowed:
        if isinstance(a, int):
            normalized.append(a)
        else:
            s = str(a).lstrip('@').lower()
            normalized.append(s)
    return normalized

def is_greeting_text(text: str) -> bool:
    """Проверяет, является ли текст простым 'привет' (с учётом регистра и пунктуации)."""
    if not isinstance(text, str):
        return False
    return bool(GREETING_RE.match(text))

def is_allowed_sender(from_user, allowed_normalized) -> bool:
    """
    Проверяет, разрешён ли отправитель.
    from_user: Telegram User object (или объект с атрибутами id и username)
    allowed_normalized: список, полученный из normalize_allowed()
    """
    if from_user is None:
        return False

    # Check by numeric id
    try:
        uid = int(getattr(from_user, "id"))
    except Exception:
        uid = None

    if uid is not None and uid in allowed_normalized:
        return True

    # Check by username (lowercase, no @)
    uname = getattr(from_user, "username", None)
    if uname:
        if uname.lstrip('@').lower() in allowed_normalized:
            return True

    return False

def should_respond(message, allowed):
    """
    Основная функция: возвращает True, если нужно ответить.
    message: pyrogram.types.Message
    allowed: iterable из id/username (int или str)
    """
    allowed_normalized = normalize_allowed(allowed)

    # Не отвечаем если нет пользователя (например, канал)
    if message.from_user is None:
        return False

    if not is_allowed_sender(message.from_user, allowed_normalized):
        return False

    if not message.text:
        return False

    if is_greeting_text(message.text):
        return True

    return False

def reply_text(message) -> str:
    """Формирует текст ответа. Можете расширить логику здесь."""
    return "Привет"
