USER = "6442579367"  # замените на user_id пользователя

async def handle(client, message):
    # простое эхо: отвечает тем же текстом
    text = message.text or message.caption or ""
    if not text:
        await message.reply_text("Получил сообщение (нет текста).")
    else:
        await message.reply_text(f"Echo: {text}")
