import asyncio
import importlib
import traceback
from copy import copy

from aiogram import Bot
from aiogram.exceptions import TelegramServerError, TelegramForbiddenError
from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile

from config_data.config import anti_spam_duration
from keyboards.inline.kb_creator import InlineCreator

from utils.lexicon_utils.admin_lexicon.admin_lexicon_utils import get_ban_notification_lexicon_part

context_managers_module = importlib.import_module('utils.context_managers')

async def try_delete_notification(callback: CallbackQuery, user_status: str=None, non_callback_answer_mode=False):
    redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт

    redis_sub_key = None
    callback_data = callback.data
    ic(callback.data)
    if ':' in callback_data:
        user_status = callback_data.split(':')[1]

    if user_status == 'seller':
        redis_sub_key = ':seller_registration_notification'
    elif user_status == 'buyer':
        redis_sub_key = ':buyer_offer_notification'
    elif user_status == 'lose_tariff':
        redis_sub_key = ':seller_without_tariff_notification'
    elif user_status == 'delete_tariff':
        redis_sub_key = ':seller_lose_self_tariff'
    elif user_status in ('sales', 'purchases'):
        redis_sub_key = f':{user_status}_notification'
    elif user_status == 'close_advert':
        redis_sub_key = ':close_advert_notification'
    if redis_sub_key:
        notification_message_id = await redis_module.redis_data.get_data(key=str(callback.from_user.id) + redis_sub_key)
        if notification_message_id:
            try:
                await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=notification_message_id)
            except:
                pass

        await redis_module.redis_data.delete_key(key=str(callback.from_user.id) + redis_sub_key)

        if not non_callback_answer_mode:
            await callback.answer()


async def send_notification(callback: CallbackQuery | None, user_status: str, chat_id=None, bot: Bot = None, ban_reason=None, advert_block_data=None):
    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
    lexicon_part = None
    current_id = None
    lexicon_key = ''
    ic(user_status)
    if user_status == 'seller':
        redis_sub_key = ':seller_registration_notification'
        lexicon_key = 'confirm_seller_profile_notification'
        current_id = chat_id
    # elif user_status == 'buyer':
    #     redis_sub_key = ':buyer_offer_notification'
    #     lexicon_key = 'buyer_offer_notification'
    elif user_status in ('seller_without_tariff', 'seller_lose_self_tariff'):
        lexicon_key = f'{user_status}_notification'
        redis_sub_key = f':{lexicon_key}'
        current_id = str(chat_id)
    elif user_status in ('seller_ban', 'buyer_ban'):
        if user_status == 'seller_ban':
            ic()
            lexicon_caption_key = 'sales'
        elif user_status == 'buyer_ban':
            ic()
            lexicon_caption_key = 'purchases'
        redis_sub_key = f':{lexicon_caption_key}_notification'
        ic(lexicon_caption_key)

    elif user_status == 'close_advert':

        redis_sub_key = f':close_advert_notification'
        current_id = chat_id

        ic(lexicon_part, redis_sub_key, current_id, advert_block_data)


    if not current_id:
        current_id = str(callback.from_user.id)

    if not chat_id:
        chat_id = await redis_module.redis_data.get_data(key=current_id + ':chat_id')

    language = await redis_module.redis_data.get_data(f'{chat_id}:language')
    if not language:
        language = 'ru'
    lexicon = copy(lexicon_module.LEXICON)._data[language]
    if user_status == 'close_advert':
        lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
        lexicon_part = lexicon_module\
            .CATALOG_LEXICON._data[language]['close_advert_seller_notification']
        lexicon_part['message_text'] = lexicon_part['message_text'].format(**advert_block_data)
    elif user_status in ('seller_ban', 'buyer_ban'):
        lexicon_part = await get_ban_notification_lexicon_part(lexicon_caption_key, ban_reason, language)

    notification_message_id = await redis_module.redis_data.get_data(key=f'{current_id}{redis_sub_key}')
    if notification_message_id:
        #return
        pass

    if not lexicon_part and lexicon_key:
        lexicon_part = lexicon[lexicon_key]
    message_text = lexicon_part['message_text']
    keyboard = await InlineCreator.create_markup(input_data=lexicon_part)
    ic(message_text, callback, bot)
    notification_message = None
    if callback:
        await callback.answer(lexicon_module.LEXICON['success_notification'])
        async with context_managers_module.ignore_exceptions():
            notification_message = await callback.message.bot.send_message(chat_id=chat_id, text=message_text,
                                                    reply_markup=keyboard)

    elif bot:
        async with context_managers_module.ignore_exceptions():
            notification_message = await bot.send_message(chat_id=chat_id, text=message_text, reply_markup=keyboard)

    ic(notification_message)
    if notification_message:
        await redis_module.redis_data.set_data(key=str(chat_id) + redis_sub_key,
                                                value=notification_message.message_id)

async def send_notification_for_seller(callback: CallbackQuery, data_for_seller, media_mode=False):
    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
    car_advert_requests_module = importlib.import_module('database.data_requests.car_advert_requests')

    commodity_model = await car_advert_requests_module\
        .AdvertRequester.get_where_id(advert_id=data_for_seller['car_id'])
    seller_id = commodity_model.seller.telegram_id
    language = await redis_module.redis_data.get_data(f'{seller_id}:language')
    if not language:
        language = 'ru'
    lexicon = copy(lexicon_module.LEXICON)._data[language]
    ic(seller_id)
    media_message = None
    active_seller_notifications = []
    reply_media_message_id = None
    if media_mode:
        media_group = []
        media_message = None
        for file_data in data_for_seller['album']:
            if isinstance(file_data, dict):
                file_data = file_data['id']
            if '/' in file_data:
                file_data = FSInputFile(file_data)

            media_group.append(InputMediaPhoto(media=file_data))
        try:
            media_message = await callback.bot.send_media_group(chat_id=seller_id,
                                                              media=media_group)
        except TelegramServerError:
            # traceback.print_exc()
            async with context_managers_module.ignore_exceptions():
                media_message = await callback.bot.send_media_group(chat_id=seller_id,
                                                                        media=media_group)
        except TelegramForbiddenError:
            return

        for media in media_message:
            active_seller_notifications.append(media.message_id)

        reply_media_message_id = active_seller_notifications[0]
        # active_seller_notifications.append(notification_media_part)

    lexicon_part = {'message_text': data_for_seller['message_text'],
                    'buttons': lexicon['notification_from_seller_by_buyer_buttons']}


    if media_message:
        await asyncio.sleep(anti_spam_duration)
    async with context_managers_module.ignore_exceptions():
        notification_message_part = await callback.bot.send_message(chat_id=seller_id,
                                                                    text=lexicon_part['message_text'],
                                                                    reply_markup=await InlineCreator.create_markup(
                                                                        input_data=lexicon_part['buttons']),
                                                                    reply_to_message_id=reply_media_message_id)


    lexicon_part['buttons'] = {}
    if notification_message_part:
        head_message_id = notification_message_part.message_id
        active_seller_notifications.append(head_message_id)
    else:
        head_message_id = ''

    for key, value in lexicon['notification_from_seller_by_buyer_buttons'].items():
        if key in ('close_seller_notification:', 'my_sell_feedbacks:'):
            key = key + str(head_message_id)

        lexicon_part['buttons'][key] = value
    keyboard = await InlineCreator.create_markup(input_data=lexicon_part['buttons'])
    ic(keyboard)
    async with context_managers_module.ignore_exceptions():
        await callback.bot.edit_message_reply_markup(
            chat_id=seller_id,
            message_id=notification_message_part.message_id,
            reply_markup=keyboard)
    ic(lexicon_part['buttons'], active_seller_notifications)
    await redis_module.redis_data.set_data(key=f'{seller_id}:{head_message_id}:active_notifications',
                                           value=active_seller_notifications)


async def delete_notification_for_seller(callback: CallbackQuery):
    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт

    ic(callback.data)
    head_notification_message_id = callback.data.split(':')[-1]
    redis_key = f'{callback.from_user.id}:{head_notification_message_id}:active_notifications'

    messages_to_delete = await redis_module.redis_data.get_data(
        key=redis_key,
        use_json=True)
    ic(messages_to_delete)


    if messages_to_delete:
        try:
            await callback.bot.delete_messages(chat_id=callback.message.chat.id, message_ids=messages_to_delete)
        except:
            traceback.print_exc()
            pass

    await redis_module.redis_data.delete_key(redis_key)