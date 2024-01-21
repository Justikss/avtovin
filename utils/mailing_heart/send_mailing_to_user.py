import importlib

from aiogram import Bot

from handlers.utils.send_any_medias import send_media

message_editor_module = importlib.import_module('handlers.message_editor')

async def add_message_id_in_inline_markup(lexicon_part, message_id):
    good_lexicon_part = {'buttons': {}}
    for key, value in lexicon_part['buttons']:
        if key == 'close_mailing_message:':
            key = f'{key}{message_id}'

        good_lexicon_part['buttons'][key] = value
    ic(good_lexicon_part)
    return good_lexicon_part


async def send_mailing(bot: Bot, media_group, caption, chat_id):
    from utils.context_managers import ignore_exceptions

    if media_group:
        async with ignore_exceptions():
            message_ids = await send_media(bot, media_group, chat_id=chat_id, caption=caption)
    else:
        message_ids = []

    if message_ids:
        result = {chat_id: message_ids}
        return result
