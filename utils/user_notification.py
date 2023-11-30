import importlib

from aiogram.types import CallbackQuery, InputMediaPhoto

from database.data_requests.car_advert_requests import AdvertRequester
from keyboards.inline.kb_creator import InlineCreator
from utils.Lexicon import LEXICON


async def try_delete_notification(callback: CallbackQuery, user_status: str=None, non_callback_answer_mode=False):
    redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт

    callback_data = callback.data
    if ':' in callback_data:
        user_status = callback_data.split(':')[1]

    if user_status == 'seller':
        redis_sub_key = ':seller_registration_notification'
    elif user_status == 'buyer':
        redis_sub_key = ':buyer_offer_notification'

    notification_message_id = await redis_module.redis_data.get_data(key=str(callback.from_user.id) + redis_sub_key)
    if notification_message_id:
        try:
            await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=notification_message_id)
            await redis_module.redis_data.delete_key(key=str(callback.from_user.id) + redis_sub_key)
        except:
            pass

    if not non_callback_answer_mode:
        await callback.answer()


async def send_notification(callback: CallbackQuery, user_status: str, chat_id=None):
    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт

    if user_status == 'seller':
        redis_sub_key = ':seller_registration_notification'
        lexicon_key = 'confirm_seller_profile_notification'
    elif user_status == 'buyer':
        redis_sub_key = ':buyer_offer_notification'
        lexicon_key = 'buyer_offer_notification'

    notification_message_id = await redis_module.redis_data.get_data(key=str(callback.from_user.id) + redis_sub_key)
    if notification_message_id:
        #return
        pass

    await callback.answer()


    await callback.answer(LEXICON['success_notification'])
    if not chat_id:
        chat_id = await redis_module.redis_data.get_data(key=str(callback.from_user.id) + ':chat_id')
    lexicon_part = LEXICON[lexicon_key]
    keyboard = await InlineCreator.create_markup(input_data=lexicon_part)
    notification_message = await callback.message.bot.send_message(chat_id=chat_id, text=lexicon_part['message_text'],
                                            reply_markup=keyboard)

    await redis_module.redis_data.set_data(key=str(callback.from_user.id) + redis_sub_key,
                                            value=notification_message.message_id)

async def send_notification_for_seller(callback: CallbackQuery, data_for_seller, media_mode=False):
    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт

    commodity_model = await AdvertRequester.get_where_id(data_for_seller['car_id'])
    seller_id = commodity_model.seller.telegram_id
    ic(seller_id)
    seller_offers = await redis_module.redis_data.get_data(key=f'{str(seller_id)}:seller__new_active_offers', use_json=True)
    if not seller_offers:
        seller_offers = []
    seller_offers.append(data_for_seller)
    # await redis_module.redis_data.delete_key(key=f'{str(seller_id)}:seller__new_active_offers')

    await redis_module.redis_data.set_data(key=f'{str(seller_id)}:seller__new_active_offers', value=seller_offers)


    # active_seller_notifications = await redis_module.redis_data.get_data(key=f'{seller_id}:active_notifications', use_json=True)
    # if not active_seller_notifications:
    active_seller_notifications = []
    reply_media_message_id = None
    if media_mode:
        [active_seller_notifications.append(media.message_id)
         for media in await callback.bot.send_media_group(chat_id=seller_id,
                                                          media=[InputMediaPhoto(media=file_data['id'])
                                                                 for file_data in data_for_seller['album']]
                                                          )]
        reply_media_message_id = active_seller_notifications[0]
        # active_seller_notifications.append(notification_media_part)

    lexicon_part = {'message_text': data_for_seller['message_text'],
                    'buttons': LEXICON['notification_from_seller_by_buyer_buttons']}

    notification_message_part = await callback.bot.send_message(chat_id=seller_id,
                                                                text=lexicon_part['message_text'],
                                                                reply_markup=await InlineCreator.create_markup(
                                                                    input_data=lexicon_part['buttons']),
                                                                reply_to_message_id=reply_media_message_id)
    lexicon_part['buttons'] = {}
    active_seller_notifications.append(notification_message_part.message_id)

    for key, value in LEXICON['notification_from_seller_by_buyer_buttons'].items():
        if key in ('close_seller_notification:', 'my_sell_feedbacks:'):
            key = key + '-'.join([str(media_message_id) for media_message_id in active_seller_notifications])

        lexicon_part['buttons'][key] = value

    await callback.bot.edit_message_reply_markup(
        chat_id=seller_id,
        message_id=notification_message_part.message_id,
        reply_markup=await InlineCreator.create_markup(input_data=lexicon_part['buttons'])
    )
        # await redis_module.redis_data.set_data(key=f'{seller_id}:active_notifications', value=active_seller_notifications)


async def delete_notification_for_seller(callback: CallbackQuery):

    messages_to_delete = callback.data.split(':')[-1].split('-')

    for message_id in messages_to_delete:
        try:
            await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=int(message_id))
        except:
            pass