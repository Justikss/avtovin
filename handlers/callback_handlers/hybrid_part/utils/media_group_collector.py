import asyncio
import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputMediaPhoto

mediagroups = {}
user_messages = []


async def collect_and_send_mediagroup(message: Message, state: FSMContext, photo_id: int, album_id: int, unique_id: int):
    '''Обработчик для принятия медиа групп
    Работает с:
    [seller: output_boot_config]'''
    if message.from_user.is_bot:
        return
    print('in', mediagroups)
    await message.delete()
    if album_id in mediagroups:
        mediagroups[album_id].append({'id': photo_id, 'unique_id': unique_id})
        user_messages.append(message.message_id)
        return
    mediagroups[album_id] = [{'id': photo_id, 'unique_id': unique_id}]
    user_messages.append(message.message_id)
    await asyncio.sleep(1)

    # new_album = [InputMediaPhoto(media=file_id) for file_id in mediagroups[album_id]]

    if state:
        seller_boot_commodity_module = importlib.import_module('handlers.state_handlers.seller_states_handler.load_new_car.get_output_configs')
        state_name = await state.get_state()
        print(state_name)
        if state_name == 'LoadCommodityStates:load_config_output':
            print('saerawe')
            # try:
            #     [await message.bot.delete_message(chat_id=message.chat.id, message_id=message_id) for message_id in user_messages]
            # except:
            #     pass
            await seller_boot_commodity_module.output_load_config_for_seller(request=message, state=state, media_photos=mediagroups)
            mediagroups.clear()



