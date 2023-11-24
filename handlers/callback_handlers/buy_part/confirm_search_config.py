import importlib
import traceback

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from database.data_requests.commodity_requests import CommodityRequester
from handlers.callback_handlers.hybrid_part import return_main_menu
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_cars_pagination_system.pagination_system_for_buyer import \
    BuyerCarsPagination
from utils.Lexicon import LEXICON
from database.data_requests.person_requests import PersonRequester
from database.data_requests.offers_requests import OffersRequester
from utils.user_notification import send_notification_for_seller


async def output_for_seller_formater(callback: CallbackQuery, almost_done_card) -> dict:
    '''Формирование строки для вывода запроса в чат селлера'''
    redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    for_seller_lexicon_part = LEXICON['confirm_from_seller']['message_text']
    ic(almost_done_card)
    person_model = PersonRequester.get_user_for_id(user_id=callback.from_user.id, user=True)
    if not person_model:
        await message_editor.travel_editor.edit_message(request=callback,
                                                        lexicon_key='buy_configuration_non_registration')
        return
    person_model = person_model[0]
    contact_number = person_model.phone_number

    card_text = almost_done_card['message_text']
    card_text = card_text.split('\n')
    ic(card_text)
    del card_text[0]
    card_text[0] = f'''{for_seller_lexicon_part['from_user']} @{callback.from_user.username}\n{for_seller_lexicon_part['tendered'].replace('X', str(almost_done_card['car_id']))}\n{for_seller_lexicon_part['contacts']} {contact_number}'''
    almost_done_card['message_text'] = '\n'.join(card_text)
    ic(almost_done_card)

    return almost_done_card




async def confirm_settings_handler(callback: CallbackQuery, state: FSMContext):
    '''Обработка подтверждения(от пользователя) поисковых настроек на покупку автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    redis_data = importlib.import_module('utils.redis_for_language')
    ic(callback.data)
    car_id = callback.data.split(':')[-1]

    car_model = CommodityRequester.get_where_id(car_id)

    redis_key_substring = f'|{car_model.state}|{car_model.brand}|{car_model.model}|{car_model.engine_type}|{car_model.year_of_release}|{car_model.mileage}|{car_model.color}|{car_model.complectation}'

    redis_cache_requests_key = f'{str(callback.from_user.id)}:buyer_nonconfirm_cars_cache{redis_key_substring}'

    cached_data = await redis_data.redis_data.get_data(key=redis_cache_requests_key,
                                           use_json=True)


    #
    # cached_data = await redis_data.redis_data.get_data(key=f'{str(callback.from_user.id)}:buyer_nonconfirm_cars_cache',
    #                                        use_json=True)
    ic(cached_data)
    index = -1
    for cached_part in cached_data:
        index += 1
        ic(car_id)
        if cached_part['car_id'] == int(car_id):
            current_offer = cached_data[index]
            del cached_data[index]
            ic(cached_data)
            try:
                insert_response = await OffersRequester.set_offer_model(buyer_id=callback.from_user.id, car_id=car_id)
            except BufferError as ex:
                print(ex)
                insert_response = None
                await callback.answer(text=LEXICON['buy_configuration_error']['message_text'], show_alert=True)
            except Exception as ex:
                ic(ex)
                traceback.print_exc()

            finally:

                data_for_seller = await output_for_seller_formater(callback, current_offer)

                # lexicon_part = {'message_text': data_for_seller['message_text'],
                #                 'buttons': LEXICON['notification_from_seller_by_buyer_buttons']}
                commodity_model = CommodityRequester.get_where_id(car_id=data_for_seller['car_id'])
                if commodity_model:
                    media_mode = True if data_for_seller.get('album') else False
                    await send_notification_for_seller(callback, data_for_seller, media_mode=media_mode)
                    # seller_chat = commodity_model.seller_id.telegram_id
                    # await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
                    #                                                 media_group=data_for_seller['album'],
                    #                                                 lexicon_part=lexicon_part, send_chat=seller_chat)
                    callback_answer_text = LEXICON['order_was_created']
                else:
                    callback_answer_text = LEXICON['seller_dont_exists']

                await callback.answer(text=callback_answer_text, show_alert=True)


                pagination_data = await message_editor.redis_data.get_data(key=f'{str(callback.from_user.id)}:buyer_cars_pagination',
                                                         use_json=True)

                if len(pagination_data['data']) == 1:
                    await message_editor.redis_data.delete_key(key=f'{str(callback.from_user.id)}:buyer_cars_pagination')
                    await redis_data.redis_data.delete_key(
                        key=redis_cache_requests_key)
                    return await return_main_menu.return_main_menu_callback_handler(callback=callback, state=state)
                else:
                    pagination_data['data'] = cached_data
                    await redis_data.redis_data.getset_data(
                        key=redis_cache_requests_key,
                        value=cached_data)

                    await message_editor.redis_data.set_data(
                        key=f'{str(callback.from_user.id)}:buyer_cars_pagination',
                        value=pagination_data)

                    pagination = BuyerCarsPagination(**pagination_data)
                    ic()
                    await pagination.send_page(callback, '-')




    # await redis_data.redis_data.set_data(key=f'{str(callback.from_user.id)}:buyer_nonconfirm_cars_cache',
    #                                        value=formatted_config_output)

    await callback.answer()
