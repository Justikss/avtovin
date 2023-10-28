import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from config_data.config import DEAL_CHAT
from utils.Lexicon import LEXICON
from database.data_requests.person_requests import PersonRequester
from database.data_requests.offers_requests import OffersRequester



async def output_for_seller_formater(callback: CallbackQuery, state: FSMContext) -> str:
    '''Формирование строки для вывода запроса в чат селлера'''
    redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт


    lexicon_part = LEXICON['chosen_configuration']['message_text']
    for_seller_lexicon_part = LEXICON['confirm_from_seller']['message_text']
    memory_storage = await redis_module.redis_data.get_data(key=str(callback.from_user.id) + ':selected_search_buy_config', use_json=True)
    print('mema', type(memory_storage), memory_storage)
    print('lexicon_part', type(lexicon_part))
    print(for_seller_lexicon_part)
    print(lexicon_part['cost'], memory_storage['average_cost'])
    person_model = PersonRequester.get_user_for_id(user_id=callback.from_user.id, user=True)
    if not person_model:
        await message_editor.travel_editor.edit_message(requet=callback, lexicon_key='buy_configuration_non_registration')
        return
    person_model = person_model[0]
    contact_number = person_model.phone_number
    redis_key = str(callback.from_user.id) + ':cars_type'
    cars_state = await redis_module.redis_data.get_data(redis_key)

    result_string =  f'''{for_seller_lexicon_part['from_user']} @{callback.from_user.username}\n{for_seller_lexicon_part['tendered']}\n{for_seller_lexicon_part['contacts']} {contact_number}\n{for_seller_lexicon_part['separator']}\n{lexicon_part['engine_type']} {memory_storage['cars_engine_type']}\n{lexicon_part['brand']} {memory_storage['cars_brand']}\n{lexicon_part['model']} {memory_storage['cars_model']}\n{lexicon_part['complectation']} {memory_storage['cars_complectation']}'''
    

    if cars_state == 'second_hand_cars':
        result_string += f'''\n{lexicon_part['year']} {memory_storage['cars_year_of_release']}\n{lexicon_part['mileage']} {memory_storage['cars_mileage']}\n{lexicon_part['color']} {memory_storage['cars_color']}
        '''

    result_string += f'''\n{lexicon_part['cost']} {memory_storage['average_cost']}'''

    return result_string




async def confirm_settings_handler(callback: CallbackQuery, state: FSMContext):
    '''Обработка подтверждения(от пользователя) поисковых настроек на покупку автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    redis_data = importlib.import_module('utils.redis_for_language')
    memory_data = await state.get_data()
    cars_id_range = memory_data.get('offer_cars_range')

    match_result = await OffersRequester.match_check(user_id=callback.from_user.id, cars_id_range=cars_id_range)

    if not match_result:
        print('match was be')
        lexicon_key = 'buy_configuration_error'
    else:
        lexicon_key = 'confirm_buy_configuration'
        cars_id_range = match_result

    buyer_id = memory_data.get('buyer_id')
    await state.clear()
    await message_editor.travel_editor.edit_message(lexicon_key=lexicon_key, request=callback, delete_mode=True)
    if not match_result:
        return

    cars_id_range = ':'.join(cars_id_range)
    lexicon_part = LEXICON['confirm_from_seller']

    callback_data = 'confirm_from_seller:' + cars_id_range + ':to_buyer:' + buyer_id
    print(callback_data)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
        text=lexicon_part['confirm_button'],
        callback_data=callback_data)
    ]])

    output_text = await output_for_seller_formater(callback=callback, state=state)

    message_for_dealers = await callback.message.bot.send_message(chat_id=DEAL_CHAT, text=output_text, reply_markup=keyboard)

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
