import asyncio
import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputMediaPhoto

from database.data_requests.car_configurations_requests import CarConfigs
from database.data_requests.new_car_photo_requests import PhotoRequester
from database.db_connect import manager
from database.tables.car_configurations import CarComplectation, CarBrand, CarModel, CarEngine, CarColor
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.new_car_state_parameters_handler import \
    NewCarStateParameters

from handlers.custom_filters.message_is_photo import MessageIsPhoto

mediagroups = {}
user_messages = []

async def get_unique_dictionaries(mediagroups):
    unique_mediagroups = {}

    for key, value in mediagroups.items():
        unique_combinations = set()
        unique_dicts = []

        for item in value:
            id_pair = (item.get('id'), item.get('unique_id'))

            if id_pair not in unique_combinations:
                unique_combinations.add(id_pair)
                unique_dicts.append(item)

        unique_mediagroups[key] = unique_dicts

    return unique_mediagroups
async def collect_and_send_mediagroup(message: Message, state: FSMContext, photo_id: int, unique_id: int):
    seller_boot_commodity_module = importlib.import_module(
        'handlers.state_handlers.seller_states_handler.load_new_car.get_output_configs')

    '''Обработчик для принятия медиа групп
    Работает с:
    [seller: output_boot_config]'''
    # if message.from_user.is_bot:
    #
    #     return

    try:
        await message.delete()
    except:
        pass
    ic()
    ic(state)
    album_id = message.media_group_id
    ic(album_id)
    if album_id:
        if album_id in mediagroups:
            mediagroups[album_id].append({'id': photo_id, 'unique_id': unique_id})
            user_messages.append(message.message_id)
            return
        mediagroups[album_id] = [{'id': photo_id, 'unique_id': unique_id}]
        user_messages.append(message.message_id)
        await asyncio.sleep(2)


        # new_album = [InputMediaPhoto(media=file_id) for file_id in mediagroups[album_id]]

        if state:
            state_name = await state.get_state()
            ic(state_name)
            #
            if state_name:
                if state_name in ('LoadCommodityStates:photo_verification', 'AdminAdvertParametersStates.NewStateStates:await_input_new_car_photos'):
                    if not 3 <= len(mediagroups[album_id]) <= 5:

                        photo_filter = MessageIsPhoto()
                        mediagroups.clear()
                        user_messages.clear()
                        await photo_filter(message=message, state=state)
                        return
                    match state_name:
                        case 'LoadCommodityStates:photo_verification':
                            await seller_boot_commodity_module.output_load_config_for_seller(request=message, state=state, media_photos=mediagroups)
                        case 'AdminAdvertParametersStates.NewStateStates:await_input_new_car_photos':
                            await NewCarStateParameters().callback_handler(message, state, media_photos=mediagroups)
                    mediagroups.clear()

            elif state_name == "MailingStates:uploading_media":
                return mediagroups
    else:
        if state:
            state_name = await state.get_state()
            ic(state_name)
            #
            if state_name:
                match state_name:
                    case 'LoadCommodityStates:photo_verification':
                        await seller_boot_commodity_module.output_load_config_for_seller(request=message, state=state,
                                                                                         media_photos=mediagroups)
                    case 'AdminAdvertParametersStates.NewStateStates:await_input_new_car_photos':
                        await NewCarStateParameters().callback_handler(message, state, media_photos=mediagroups)