import importlib
import logging
import traceback

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from icecream import ic

from database.data_requests.commodity_requests import CommodityRequester
from handlers.callback_handlers.buy_part.show_cached_requests import get_cached_requests__chose_brand
from handlers.callback_handlers.hybrid_part import return_main_menu
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_cars_pagination_system.pagination_system_for_buyer import \
    BuyerCarsPagination
from utils.Lexicon import LEXICON
from database.data_requests.person_requests import PersonRequester
from utils.user_notification import send_notification_for_seller

# ic.disable()

async def output_for_seller_formater(callback: CallbackQuery, almost_done_card) -> dict:
    '''Формирование строки для вывода запроса в чат селлера'''
    redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    for_seller_lexicon_part = LEXICON['confirm_from_seller']['message_text']
    person_model = await PersonRequester.get_user_for_id(user_id=callback.from_user.id, user=True)
    if not person_model:
        await message_editor.travel_editor.edit_message(request=callback,
                                                        lexicon_key='buy_configuration_non_registration')
        return
    person_model = person_model[0]
    contact_number = person_model.phone_number

    card_text = almost_done_card['message_text']
    card_text = card_text.split('\n')
    del card_text[0]
    card_text[0] = f'''{for_seller_lexicon_part['from_user']} @{callback.from_user.username}\n{for_seller_lexicon_part['tendered'].replace('X', str(almost_done_card['car_id']))}\n{for_seller_lexicon_part['contacts']} {contact_number}'''
    almost_done_card['message_text'] = '\n'.join(card_text)

    return almost_done_card


async def confirm_settings_handler(callback: CallbackQuery, state: FSMContext):
    '''Обработка подтверждения(от пользователя) поисковых настроек на покупку автомобиля'''
    cached_requests_module = importlib.import_module('database.data_requests.offers_requests')
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    # redis_data = importlib.import_module('utils.redis_for_language')
    car_dont_exists = False
    ic(callback.data)
    car_id = callback.data.split(':')[-1]

    car_model = CommodityRequester.get_where_id(car_id)
    cached_data = None
    if car_model:

        cached_data = await cached_requests_module.CachedOrderRequests.get_cache(buyer_id=callback.from_user.id, car_id=car_id)
        if cached_data:
            cached_data = cached_data[0]
            ic(cached_data)
            await cached_requests_module.CachedOrderRequests.remove_cache(buyer_id=callback.from_user.id, car_id=car_id)
            cached_data = {'car_id': cached_data.car_id.car_id,
                           'message_text': cached_data.message_text,
                           'album': CommodityRequester.get_photo_album_by_car_id(cached_data.car_id)}

            data_for_seller = await output_for_seller_formater(callback, cached_data)

            # commodity_model = CommodityRequester.get_where_id(car_id=data_for_seller['car_id'])

            try:
                insert_response = await cached_requests_module.OffersRequester.set_offer_model(buyer_id=callback.from_user.id, car_id=car_id, seller_id = car_model.seller_id)
                if not insert_response:
                    await callback.answer(text=LEXICON['buy_configuration_error']['message_text'], show_alert=True)
                if car_model:
                    media_mode = True if data_for_seller.get('album') else False
                    await send_notification_for_seller(callback, data_for_seller, media_mode=media_mode)
                    callback_answer_text = LEXICON['order_was_created']
                else:
                    callback_answer_text = LEXICON['seller_dont_exists']

                await callback.answer(text=callback_answer_text, show_alert=True)
            except BufferError as ex:
                print(ex)
                insert_response = None
                await callback.answer(text=LEXICON['buy_configuration_error']['message_text'], show_alert=True)
            except Exception as ex:
                ic(ex)
                traceback.print_exc()

        else:
            car_dont_exists = True
            commodity_exists = CommodityRequester.get_where_id(car_id)
            if not commodity_exists:
                await callback.answer(text=LEXICON['car_was_withdrawn_from_sale'], show_alert=True)
            else:
                await callback.answer(text=LEXICON['buy_configuration_error']['message_text'], show_alert=True)

        pagination_data = await message_editor.redis_data.get_data(key=f'{str(callback.from_user.id)}:buyer_cars_pagination',
                                                 use_json=True)
        ic(len(pagination_data['data']), cached_data, car_dont_exists)
        if (len(pagination_data['data']) <= 1 or not cached_data) and not car_dont_exists:
            await message_editor.redis_data.delete_key(key=f'{str(callback.from_user.id)}:buyer_cars_pagination')

            # state_name = await state.get_state()
            # if state_name == 'HybridChooseStates:config_output':
            return await return_main_menu.return_main_menu_callback_handler(callback=callback, state=state)
            # elif state_name == 'CheckNonConfirmRequestsStates:brand_flipping_process':
            #     await get_cached_requests__chose_brand(callback, state)
        else:
            # data_part_to_delete = [data_part for data_part in pagination_data['data'] if int(data_part['car_id']) == int(car_id)]
            ic(pagination_data['data'])
            pagination_data['data'].pop(pagination_data['current_page']-1)
            ic(pagination_data)


        await message_editor.redis_data.set_data(
            key=f'{str(callback.from_user.id)}:buyer_cars_pagination',
            value=pagination_data)

        pagination = BuyerCarsPagination(**pagination_data)
        ic(pagination_data['data'])
        await pagination.send_page(callback, state, '+')




    # await redis_data.redis_data.set_data(key=f'{str(callback.from_user.id)}:buyer_nonconfirm_cars_cache',
    #                                        value=formatted_config_output)

    await callback.answer()
