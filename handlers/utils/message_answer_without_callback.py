import asyncio
import importlib
from copy import copy
from datetime import datetime

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery

from config_data.config import anti_spam_duration
from handlers.utils.delete_message import delete_message

config_module = importlib.import_module('config_data.config')


async def send_message_answer(request: Message | CallbackQuery, text: str, sleep_time=None, show_alert=False,
                              message=False):
    await delete_message(request, from_redis=True)
    from handlers.custom_filters.message_is_photo import MessageIsPhoto
    await MessageIsPhoto().chat_cleaner(trash_redis_keys=(':last_message', ':last_media_group'),
                                        message=request if isinstance(request, Message) else request.message)
    ic(type(request))
    if isinstance(request, Message) or message:
        if message and isinstance(request, CallbackQuery):
            request = request.message
        ic()
        redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
        media_group_delete_module = importlib.import_module('handlers.callback_handlers.sell_part.seller_main_menu')

        last_message = await redis_module.redis_data.get_data(key=f'{request.from_user.id}:last_message')

        await delete_message(request, last_message)
        await media_group_delete_module.delete_media_groups(request=request)

        text = f'<blockquote><b>{copy(text)}</b></blockquote>'
        alert_message = await request.bot.send_message(chat_id=request.chat.id, text=text)
        ic(alert_message)
        for time_point in range(config_module.message_answer_awaited, 0, -1):
            await alert_message.edit_text(text=f'{text}{time_point}...')
            await asyncio.sleep(max(config_module.message_answer_awaited / 3, 1))

        await delete_message(request, alert_message.message_id)

    elif isinstance(request, CallbackQuery):
        ic(text)
        ic()
        ic(await request.answer(text, show_alert=show_alert))


    await asyncio.sleep(anti_spam_duration)
