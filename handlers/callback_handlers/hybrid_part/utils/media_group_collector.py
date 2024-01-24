import asyncio
import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputMediaPhoto

from handlers.custom_filters.message_is_photo import MessageIsPhoto
from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from states.load_commodity_states import LoadCommodityStates

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
    new_car_state_parameters_module = importlib.import_module(
        'handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.new_car_state_parameters_handler')

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
    if not await state.get_state() in (LoadCommodityStates.photo_verification,
                             AdminAdvertParametersStates.NewStateStates.await_input_new_car_photos):
        return
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
                            await new_car_state_parameters_module\
                                .NewCarStateParameters().callback_handler(message, state, media_photos=mediagroups)
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
                        await new_car_state_parameters_module\
                            .NewCarStateParameters().callback_handler(message, state, media_photos=mediagroups)

