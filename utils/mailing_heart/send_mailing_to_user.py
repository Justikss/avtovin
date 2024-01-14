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
    if media_group:
        message_ids = await send_media(bot, media_group, chat_id=chat_id, caption=caption)
    else:
        message_ids = []

    if message_ids:
        result = {chat_id: message_ids}
        return result
    #
    # lexicon_part = ADVERT_LEXICON['sent_mailing']
    #
    # if caption:
    #     lexicon_part['message_text'] = caption
    #
    # text_message = await bot.send_message(chat_id=chat_id,
    #                            reply_markup=await message_editor_module.InlineCreator.create_markup(lexicon_part),
    #                            text=lexicon_part['message_text'])
    #
    # message_ids.append(text_message.message_id)
    #
    # edited_lexicon_part = await add_message_id_in_inline_markup(lexicon_part, text_message.message_id)
    #
    # await bot.edit_message_reply_markup(message_id=text_message.message_id, chat_id=chat_id,
    #                                     reply_markup=await message_editor_module.InlineCreator.create_markup(edited_lexicon_part))
    #
    # await message_editor_module.redis_data.set_data(key=f'{chat_id}:mailing:{text_message.message_id}',
    #                                                 value=message_ids)
