import importlib
import traceback

from aiogram import Bot
from aiogram.exceptions import TelegramServerError
from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile

from database.data_requests.car_advert_requests import AdvertRequester
from keyboards.inline.kb_creator import InlineCreator
from utils.lexicon_utils.Lexicon import ADMIN_LEXICON
from utils.lexicon_utils.admin_lexicon.admin_lexicon_utils import get_ban_notification_lexicon_part


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
    if redis_sub_key:
        notification_message_id = await redis_module.redis_data.get_data(key=str(callback.from_user.id) + redis_sub_key)
        if notification_message_id:
            try:
                await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=notification_message_id)
                await redis_module.redis_data.delete_key(key=str(callback.from_user.id) + redis_sub_key)
            except:
                pass

        if not non_callback_answer_mode:
            await callback.answer()


async def send_notification(callback: CallbackQuery | None, user_status: str, chat_id=None, bot: Bot = None, ban_reason=None):
    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
    lexicon_part = None
    current_id = None
    ic(user_status)
    if user_status == 'seller':
        redis_sub_key = ':seller_registration_notification'
        lexicon_key = 'confirm_seller_profile_notification'
        current_id = chat_id
    elif user_status == 'buyer':
        redis_sub_key = ':buyer_offer_notification'
        lexicon_key = 'buyer_offer_notification'
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
        lexicon_part = await get_ban_notification_lexicon_part(lexicon_caption_key, ban_reason)

        ic(lexicon_part, redis_sub_key, lexicon_caption_key)

    if not current_id:
        current_id = str(callback.from_user.id)

    if not chat_id:
        chat_id = await redis_module.redis_data.get_data(key=current_id + ':chat_id')

    notification_message_id = await redis_module.redis_data.get_data(key=current_id + redis_sub_key)
    if notification_message_id:
        #return
        pass

    if not lexicon_part:
        lexicon_part = lexicon_module.LEXICON[lexicon_key]
    message_text = lexicon_part['message_text']
    keyboard = await InlineCreator.create_markup(input_data=lexicon_part)
    ic(message_text, callback, bot)
    if callback:
        await callback.answer(lexicon_module.LEXICON['success_notification'])
        notification_message = await callback.message.bot.send_message(chat_id=chat_id, text=message_text,
                                                reply_markup=keyboard)

    elif bot:
        notification_message = await bot.send_message(chat_id=chat_id, text=message_text, reply_markup=keyboard)


    await redis_module.redis_data.set_data(key=str(chat_id) + redis_sub_key,
                                            value=notification_message.message_id)

async def send_notification_for_seller(callback: CallbackQuery, data_for_seller, media_mode=False):
    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

    commodity_model = await AdvertRequester.get_where_id(data_for_seller['car_id'])
    seller_id = commodity_model.seller.telegram_id
    ic(seller_id)

    active_seller_notifications = []
    reply_media_message_id = None
    if media_mode:
        media_group = []
        data_for_seller['album'] = data_for_seller['album'][:5]
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
            traceback.print_exc()
            media_message = await callback.bot.send_media_group(chat_id=seller_id,
                                                                    media=media_group)

        for media in media_message:
            active_seller_notifications.append(media.message_id)

        reply_media_message_id = active_seller_notifications[0]
        # active_seller_notifications.append(notification_media_part)

    lexicon_part = {'message_text': data_for_seller['message_text'],
                    'buttons': lexicon_module.LEXICON['notification_from_seller_by_buyer_buttons']}



    notification_message_part = await callback.bot.send_message(chat_id=seller_id,
                                                                text=lexicon_part['message_text'],
                                                                reply_markup=await InlineCreator.create_markup(
                                                                    input_data=lexicon_part['buttons']),
                                                                reply_to_message_id=reply_media_message_id)

    lexicon_part['buttons'] = {}
    active_seller_notifications.append(notification_message_part.message_id)


    for key, value in lexicon_module.LEXICON['notification_from_seller_by_buyer_buttons'].items():
        if key in ('close_seller_notification:', 'my_sell_feedbacks:'):
            key = key + '-'.join([str(media_message_id) for media_message_id in active_seller_notifications])

        lexicon_part['buttons'][key] = value
    keyboard = await InlineCreator.create_markup(input_data=lexicon_part['buttons'])
    ic(keyboard)
    await callback.bot.edit_message_reply_markup(
        chat_id=seller_id,
        message_id=notification_message_part.message_id,
        reply_markup=keyboard)

        # await redis_module.redis_data.set_data(key=f'{seller_id}:active_notifications', value=active_seller_notifications)


async def delete_notification_for_seller(callback: CallbackQuery):

    messages_to_delete = callback.data.split(':')[-1].split('-')

    for message_id in messages_to_delete:
        try:
            await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=int(message_id))
        except:
            pass