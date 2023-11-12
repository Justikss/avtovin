import asyncio
import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputMediaPhoto

mediagroups = {}
async def collect_and_send_mediagroup(message: Message, state: FSMContext, photo_id: str, album_id: int):
    print('in')
    if album_id in mediagroups:
        mediagroups[album_id].append(photo_id)
        return
    mediagroups[album_id] = [photo_id]
    await asyncio.sleep(1)

    # new_album = [InputMediaPhoto(media=file_id) for file_id in mediagroups[album_id]]

    if state:
        seller_boot_commodity_module = importlib.import_module('handlers.state_handlers.seller_states_handler.load_new_car.get_output_configs')
        state_name = await state.get_state()
        print(state_name)
        if state_name == 'LoadCommodityStates:load_config_output':
            print('saerawe')
            await seller_boot_commodity_module.output_load_config_for_seller(request=message, state=state, media_photos=mediagroups)


