import importlib

from aiogram import Bot, types
from aiogram.types import InputMediaPhoto, InputMediaVideo, InputMediaDocument, InputMediaAudio
import asyncio

redis_data_module = importlib.import_module('handlers.callback_handlers.buy_part.language_callback_handler')


async def send_media(request: types.Message | types.CallbackQuery, media_info_list: list, chat_id: int = None, caption=None):
    chat_id, bot = await take_aiogram_objects(request, chat_id)

    ic(caption)
    ic(media_info_list)

    if len(media_info_list) > 1:
        # Отправка медиа-группы
        await process_media_group(request, media_info_list, chat_id, caption, bot)
        # last_media_object = get_media_object(media_info_list[-1], caption)
        # media_objects = []
        # for media_info in media_info_list[:-1]:
        #     media_objects.append(get_media_object(media_info))
        # media_objects.append(last_media_object)
        #
        # media_message = await bot.send_media_group(chat_id=chat_id, media=media_objects)
    else:
        # Отправка единичного медиа
        media_info = media_info_list[0]
        media_info['caption'] = caption
        media_message = await send_single_media(bot, chat_id, media_info)

        redis_value = media_message.message_id
        await redis_data_module.redis_data.set_data(key=f'{request.from_user.id}:last_media_group', value=redis_value)



async def process_media_group(request, media_info_list, chat_id, caption, bot):
    # Сортировка медиа по типу
    photo_video_group = []
    other_media = []
    for media_info in media_info_list:
        if media_info['media_type'] in ['photo', 'video']:
            photo_video_group.append(media_info)
        else:
            other_media.append(media_info)

    if other_media:
        other_media[-1]['caption'] = caption
    else:
        photo_video_group[-1]['caption'] = caption

    redis_value = []

    # Отправка фото и видео медиагруппы
    if photo_video_group:
        media_objects = [get_media_object(media_info) for media_info in photo_video_group]
        media_message = await bot.send_media_group(chat_id=chat_id, media=media_objects)
        redis_value.extend([message.message_id for message in media_message])

    # Отправка аудио и документов отдельно
    for media_info in other_media:
        media_message = await send_single_media(bot, chat_id, media_info)
        redis_value.append(media_message.message_id)

    # Добавление в Redis
    await redis_data_module.redis_data.set_data(key=f'{request.from_user.id}:last_media_group', value=redis_value)


async def take_aiogram_objects(request: types.Message | types.CallbackQuery, chat_id):
    match request:
        case types.CallbackQuery():
            message = request.message
        case types.Message():
            message = request
    if not chat_id:
        chat_id = message.chat.id

    bot = request.bot

    return chat_id, bot


def get_media_object(media_info, caption=None):
    media_type = media_info['media_type']
    file_id = media_info['id']
    caption = media_info.get('caption')

    if media_type == 'photo':
        media_object = InputMediaPhoto

    elif media_type == 'video':
        media_object = InputMediaVideo

    elif media_type == 'audio':
        media_object = InputMediaAudio

    elif media_type == 'document':
        media_object = InputMediaDocument

    else:
        raise ValueError("Unsupported media type")

    if media_object:
        return media_object(media=file_id, caption=caption)

async def send_single_media(bot: Bot, chat_id: int, media_info, caption=None):
    caption = media_info.get('caption')
    media_type = media_info['media_type']
    file_id = media_info['id']

    if media_type == 'photo':
        callable_object = bot.send_photo

    elif media_type == 'video':
        callable_object = bot.send_video

    elif media_type == 'audio':
        callable_object = bot.send_audio

    elif media_type == 'document':
        callable_object = bot.send_document

    else:
        raise ValueError("Unsupported media type")

    if callable_object:
        return await callable_object(chat_id, file_id, caption=caption)
