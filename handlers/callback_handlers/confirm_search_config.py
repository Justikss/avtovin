import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from config_data.config import DEAL_CHAT
from utils.Lexicon import LEXICON



async def confirm_settings_handler(callback: CallbackQuery, state: FSMContext):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    redis_data = importlib.import_module('utils.redis_for_language')

    memory_data = await state.get_data()
    cars_id_range = memory_data.get('offer_cars_range')
    buyer_id = memory_data.get('buyer_id')
    await state.clear()
    await message_editor.travel_editor.edit_message(lexicon_key='confirm_buy_configuration', request=callback, delete_mode=True)

    cars_id_range = ':'.join(cars_id_range)

    callback_data = 'confirm_from_seller:' + cars_id_range + ':to_buyer:' + buyer_id
    print(callback_data)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
        text=LEXICON.get('button_confirm_from_seller'),
        callback_data=callback_data)
    ]])

    message_for_dealers = await callback.message.bot.send_message(chat_id=DEAL_CHAT, text='Заявка на мази', reply_markup=keyboard)

    active_non_confirm_offers = await redis_data.redis_data.get_data(
        key=str(callback.from_user.id) + ':active_non_confirm_offers',
        use_json=True
    )
    print(message_for_dealers.message_id, 'MES DEL')
    if active_non_confirm_offers:
        active_non_confirm_offers[message_for_dealers.message_id] = cars_id_range
    else:
        active_non_confirm_offers = {message_for_dealers.message_id: cars_id_range}
    await redis_data.redis_data.set_data(
        key=str(callback.from_user.id) + ':active_non_confirm_offers',
        value=active_non_confirm_offers
    )
    #await redis_data.redis_data.delete_key(key=str(callback.from_user.id) + ':active_non_confirm_offers')


    await callback.answer()
