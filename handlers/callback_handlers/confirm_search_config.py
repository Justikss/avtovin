from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from handlers.state_handlers.choose_car_for_buy.new_car_handlers import travel_editor
from config_data.config import DEAL_CHAT
from utils.Lexicon import LEXICON



async def confirm_settings_handler(callback: CallbackQuery, state: FSMContext):
    memory_data = await state.get_data()
    cars_id_range = memory_data.get('offer_cars_range')
    buyer_id = memory_data.get('buyer_id')
    await state.clear()
    await travel_editor.edit_message(lexicon_key='confirm_buy_configuration', request=callback, delete_mode=True)


    cars_id_range = ':'.join(cars_id_range)

    callback_data = 'confirm_from_seller:' + cars_id_range + ':to_buyer:' + buyer_id
    print(callback_data)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
        text=LEXICON.get('button_confirm_from_seller'),
        callback_data=callback_data)
    ]])

    await callback.message.bot.send_message(chat_id=DEAL_CHAT, text='Заявка на мази', reply_markup=keyboard)

    await callback.answer()