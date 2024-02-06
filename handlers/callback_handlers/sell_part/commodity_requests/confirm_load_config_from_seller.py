import logging
from copy import copy

from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
import importlib

from handlers.state_handlers.seller_states_handler.load_new_car.get_output_configs import data_formatter, \
    get_output_string
from utils.custom_exceptions.database_exceptions import SellerWithoutTariffException

config_module = importlib.import_module('config_data.config')


async def check_match_adverts_the_sellers(callback, state: FSMContext):
    car_advert_requests_module = importlib.import_module('database.data_requests.car_advert_requests')

    memory_storage = await state.get_data()
    ic(memory_storage.get('color_for_load'))
    match_result = await car_advert_requests_module\
        .AdvertRequester.get_advert_by(state_id=memory_storage['state_for_load'],
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

async def create_notification_for_admins(callback, commodity_number):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    lexicon_module = importlib.import_module('utils.lexicon_utils.commodity_loader')
    get_seller_header_module = importlib.import_module('handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_chosen_search_config')
    person_requester_module = importlib.import_module('database.data_requests.person_requests')

    seller_model = await person_requester_module.PersonRequester.get_user_for_id(user_id=callback.from_user.id, seller=True)
    if seller_model:
        seller_model = seller_model[0]
        redis_key = f'{str(callback.from_user.id)}:structured_boot_data'

        structured_boot_data = await message_editor.redis_data.get_data(key=redis_key, use_json=True)

        output_string = await get_output_string(mode=None,
                                                boot_data=structured_boot_data, language='ru',
                                                advert_id=commodity_number)

        boot_config_string_startswith = f'''{copy(lexicon_module.commodity_loader_lexicon_ru['config_for_admins']).format(
            username=callback.from_user.username, 
            request_id=commodity_number)}{await get_seller_header_module.get_seller_header(seller=seller_model, language='ru')}'''

        message_for_admin_chat = output_string.split('\n')
        message_for_admin_chat[0] = boot_config_string_startswith
        message_for_admin_chat = '\n'.join(message_for_admin_chat)
        await message_editor.redis_data.delete_key(key=redis_key)
        return message_for_admin_chat

async def create_notification_for_seller(request_number) -> str:
    '''Плашка "Заявка №XXXX Создана"'''
    lexicon_module = importlib.import_module('utils.lexicon_utils.commodity_loader')


    create_request_notification = lexicon_module.LexiconCommodityLoader.seller_notification['message_text']
    create_request_notification = create_request_notification.format(request_number=request_number)
    # create_request_notification = create_request_notification.split('_')
    # create_request_notification = f'{request_number}'.join(create_request_notification)

    return create_request_notification


async def confirm_load_config_from_seller(callback: CallbackQuery, state: FSMContext):
    '''Обработчик одобрения собственных конфигураций загрузки нового авто от селлера.'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
    media_group_delete_module = importlib.import_module('utils.chat_cleaner.media_group_messages')
    tariff_to_seller_binder_module = importlib.import_module('database.data_requests.tariff_to_seller_requests')
    car_configurations_requests_module = importlib.import_module('database.data_requests.car_configurations_requests')

    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
    seller_without_tariff = False

    try:
        residue_of_simultaneous_announcements = await tariff_to_seller_binder_module.TariffToSellerBinder.check_simultaneous_announcements_residue(callback.from_user.id)
        ic(residue_of_simultaneous_announcements)
        if not isinstance(residue_of_simultaneous_announcements, bool):
            ic(residue_of_simultaneous_announcements-1)
            return await callback.answer(lexicon_module.LEXICON['simultaneous_announcements_was_over'].format(
                advert_count=residue_of_simultaneous_announcements
            ), show_alert=True)

    except SellerWithoutTariffException:
        seller_without_tariff = True

    if not await tariff_to_seller_binder_module.TariffToSellerBinder.tariff_is_actuality(seller_model=callback.from_user.id, bot=callback.bot):
        seller_without_tariff = True

    if seller_without_tariff:
        return await callback.answer(lexicon_module.LEXICON['tariff_non_actuallity'], show_alert=True)

    person_requester_module = importlib.import_module('database.data_requests.person_requests')

    if not await person_requester_module.PersonRequester.get_user_for_id(callback.from_user.id, seller=True):
        logging.debug(f'{callback.from_user.id} ::: Пытался выложить товар без регистрации.')
        await message_editor.travel_editor.edit_message(request=callback, lexicon_key='try_again_seller_registration',
                                                        delete_mode=True)
        return

    if await check_match_adverts_the_sellers(callback, state):
        logging.debug(f'{callback.from_user.id} ::: Попытался выложить товар, который уже имеет на витрине.')
        return await callback.answer(lexicon_module.LexiconSellerRequests.matched_advert)

    await message_editor.redis_data.delete_key(key=str(callback.from_user.id) + ':can_edit_seller_boot_commodity')

    boot_data = await data_formatter(request=callback, state=state, id_values=True)
    ic(boot_data)
    commodity_number = await car_configurations_requests_module\
        .CarConfigs.add_advert(callback.from_user.id, boot_data)

    message_for_admin_chat = await create_notification_for_admins(callback, commodity_number)

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
                                                    send_chat=config_module.ADMIN_ADVERTS_CHAT, media_group=photos)

    from database.data_requests.recomendations_request import RecommendationRequester
    ic()
    await RecommendationRequester.add_recommendation(advert=commodity_number)

    await callback.answer()
    await state.clear()


