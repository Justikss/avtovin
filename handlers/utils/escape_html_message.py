from aiogram.types import Message


async def escape_html(message: Message):
    if "<" in message.text or ">" in message.text:
        modified_text = message.text.replace("<", "&lt;").replace(">", "&gt;")
    else:
        modified_text = message.text

    return modified_text