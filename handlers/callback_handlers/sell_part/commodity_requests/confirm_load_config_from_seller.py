import logging
from copy import copy

from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
import importlib

from config_data.config import ADMIN_CHAT
from database.data_requests.car_advert_requests import AdvertRequester
from database.data_requests.car_configurations_requests import CarConfigs
from database.data_requests.recomendations_request import RecommendationRequester
from handlers.state_handlers.seller_states_handler.load_new_car.get_output_configs import data_formatter

# async def recommendation_notifications(callback: CallbackQuery, store_query):
#     if store_query:
#         for recommendation_model in store_query:
#             buyer_model = recommendation_model.buyer
#             user_recommendations = await RecommendationRequester.retrieve_by_buyer_id(buyer_model)
#             if len(user_recommendations) > 5:
#                 user_id = buyer_model.telegram_id
#
#

async def check_match_adverts_the_sellers(callback, state: FSMContext):
    memory_storage = await state.get_data()
    ic(memory_storage.get('color_for_load'))
    match_result = await AdvertRequester.get_advert_by(state_id=memory_storage['state_for_load'],
                                                 engine_type_id=memory_storage['engine_for_load'],
                                                 brand_id=memory_storage['brand_for_load'],
                                                 model_id=memory_storage['model_for_load'],
                                                 complectation_id=memory_storage['complectation_for_load'],
                                                 year_of_release_id=memory_storage.get('year_for_load'),
                                                 mileage_id=memory_storage.get('mileage_for_load'),
                                                 color_id=memory_storage.get('color_for_load'),
                                                 seller_id=callback.from_user.id)
    ic(match_result)

    if match_result:
        return match_result

async def create_notification_for_admins(callback):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    lexicon_module = importlib.import_module('utils.lexicon_utils.commodity_loader')
    get_seller_header_module = importlib.import_module('handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_chosen_search_config')
    person_requester_module = importlib.import_module('database.data_requests.person_requests')

    seller_model = await person_requester_module.PersonRequester.get_user_for_id(user_id=callback.from_user.id, seller=True)
    if seller_model:
        seller_model = seller_model[0]

        last_output_boot_config_string = await message_editor.redis_data.get_data(key=str(callback.from_user.id) + ':boot_config')
        boot_config_string_startswith = f'''{copy(lexicon_module.LexiconCommodityLoader.config_for_admins).replace('X', callback.from_user.username)}{await get_seller_header_module.get_seller_header(seller=seller_model)}'''

        message_for_admin_chat = last_output_boot_config_string.split('\n')[:-2]
        message_for_admin_chat[0] = boot_config_string_startswith
        message_for_admin_chat = '\n'.join(message_for_admin_chat)
        return message_for_admin_chat

async def create_notification_for_seller(request_number) -> str:
    '''Плашка "Заявка №XXXX Создана"'''
    lexicon_module = importlib.import_module('utils.lexicon_utils.commodity_loader')


    create_request_notification = lexicon_module.LexiconCommodityLoader.seller_notification['message_text']
    create_request_notification = create_request_notification.split('_')
    create_request_notification = f'{request_number}'.join(create_request_notification)

    return create_request_notification


async def confirm_load_config_from_seller(callback: CallbackQuery, state: FSMContext):
    '''Обработчик одобрения собственных конфигураций загрузки нового авто от селлера.'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
    media_group_delete_module = importlib.import_module('utils.chat_cleaner.media_group_messages')
    tariff_to_seller_binder_module = importlib.import_module('database.data_requests.tariff_to_seller_requests')

    if not await tariff_to_seller_binder_module.TariffToSellerBinder.tariff_is_actuality(seller_model=callback.from_user.id, bot=callback.bot):
        lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

        await callback.answer(lexicon_module.LEXICON['tariff_non_actuallity'], show_alert=True)
        return
    message_for_admin_chat = await create_notification_for_admins(callback)

    if not message_for_admin_chat:
        logging.info(f'{callback.from_user.id} ::: Пытался выложить товар без регистрации.')
        await message_editor.travel_editor.edit_message(request=callback, lexicon_key='try_again_seller_registration',
                                                        delete_mode=True)
        return

    if await check_match_adverts_the_sellers(callback, state):
        logging.info(f'{callback.from_user.id} ::: Попытался выложить товар, который уже имеет на витрине.')
        return await callback.answer(lexicon_module.LexiconSellerRequests.matched_advert)

    await message_editor.redis_data.delete_key(key=str(callback.from_user.id) + ':can_edit_seller_boot_commodity')

    boot_data = await data_formatter(request=callback, state=state, id_values=True)
    ic(boot_data)
    print('load_photos??: ', boot_data.get('photos'))
    commodity_number = await CarConfigs.add_advert(callback.from_user.id, boot_data)

    notification_string = await create_notification_for_seller(request_number=commodity_number)
    mock_lexicon_part = {'message_text': notification_string}
    lexicon_part = lexicon_module.LEXICON['seller_load_notification_button']
    for key, value in lexicon_part.items():
        mock_lexicon_part[key] = value
    mock_lexicon_part['width'] = 1

    await media_group_delete_module.delete_media_groups(request=callback)
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=mock_lexicon_part, delete_mode=True)

    photos = boot_data.get('photos')
    if not photos:
        memory_data = await state.get_data()
        photos = memory_data.get('load_photo')

    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
                                                    lexicon_part={'message_text': message_for_admin_chat},
                                                    send_chat=ADMIN_CHAT, media_group=photos)

    store_query_in_recommendations = await RecommendationRequester.add_recommendation(advert=commodity_number)

    # await recommendation_notifications(callback, store_query_in_recommendations)

    await callback.answer()
    await state.clear()


