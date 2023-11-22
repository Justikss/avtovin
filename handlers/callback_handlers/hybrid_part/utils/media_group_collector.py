import asyncio
import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputMediaPhoto

from database.data_requests.new_car_photo_requests import PhotoRequester
from handlers.custom_filters.message_is_photo import MessageIsPhoto

mediagroups = {}
user_messages = []


async def collect_and_send_mediagroup(message: Message, state: FSMContext, photo_id: int, album_id: int, unique_id: int):
    '''Обработчик для принятия медиа групп
    Работает с:
    [seller: output_boot_config]'''
    if message.from_user.is_bot:
        print('isbot')
        return
    print('in', mediagroups)
    try:
        await message.delete()
    except:
        pass
    if album_id:
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
            ic(state_name)
            # print(state_name)
            if state_name == 'LoadCommodityStates:photo_verification':
                if not 3 <= len(mediagroups[album_id]) <= 5:
                    print('NONPHOTOTO')
                    photo_filter = MessageIsPhoto()
                    mediagroups.clear()
                    user_messages.clear()
                    await photo_filter(message=message, state=state)
                    return
                # try:
                #     [await message.bot.delete_message(chat_id=message.chat.id, message_id=message_id) for message_id in user_messages]
                # except:
                #     pass
                await seller_boot_commodity_module.output_load_config_for_seller(request=message, state=state, media_photos=mediagroups)
                mediagroups.clear()

            elif state_name == 'BootNewCarPhotosStates:await_photo':
                ic()
                data = [{'admin_id': message.from_user.id, 'car_brand': 'BMW', 'car_model': 'DualModel', 'photo_id': part['id'],
                         'photo_unique_id': part['unique_id']} for dict_values in mediagroups.values() for part in
                        dict_values]
                await PhotoRequester.load_photo_in_base(data)

