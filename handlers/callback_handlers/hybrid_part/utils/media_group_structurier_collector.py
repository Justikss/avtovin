from aiogram import types
from aiogram.fsm.context import FSMContext
from collections import defaultdict
import asyncio

from handlers.callback_handlers.admin_part.admin_panel_ui.advertisement_actions.mailing.input_mailing_data.input_date import \
    request_mailing_date_time

mediagroups = defaultdict(list)
last_media_message_id = defaultdict(int)

async def handle_media(message: types.Message, state: FSMContext):
    try:
        await message.delete()
    except:
        pass

    album_id = message.media_group_id
    media_info = {
        'media_type': message.content_type,
        'id': get_file_id(message),
        'unique_id': get_unique_id(message),
        'album_id': album_id
    }

    if album_id:
        mediagroups[album_id].append(media_info)
        last_media_message_id[album_id] = max(last_media_message_id[album_id], message.message_id)

        # Задержка для обработки всех сообщений группы
        await asyncio.sleep(1)  # Дает время для получения всех сообщений группы

        if message.message_id == last_media_message_id[album_id]:
            if album_id in mediagroups:
                await request_mailing_date_time(message, state, mediagroups[album_id])
                del mediagroups[album_id]
                del last_media_message_id[album_id]
    else:
        # Обработка единичного медиа
        await request_mailing_date_time(message, state, [media_info])

# await request_mailing_date_time(message, state, mediagroups[album_id])


def get_file_id(message):
    """ Получение file_id медиа из сообщения """
    if message.photo:
        return message.photo[-1].file_id
    elif message.video:
        return message.video.file_id
    # Добавьте условия для других типов медиа
    return None

def get_unique_id(message):
    """ Получение unique_id медиа из сообщения """
    if message.photo:
        return message.photo[-1].file_unique_id
    elif message.video:
        return message.video.file_unique_id
    # Добавьте условия для других типов медиа
    return None