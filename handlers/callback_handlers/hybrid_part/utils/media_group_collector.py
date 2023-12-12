import asyncio
import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputMediaPhoto

from database.data_requests.car_configurations_requests import CarConfigs
from database.data_requests.new_car_photo_requests import PhotoRequester
from database.db_connect import manager
from database.tables.car_configurations import CarComplectation, CarBrand, CarModel, CarEngine, CarColor
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
async def collect_and_send_mediagroup(message: Message, state: FSMContext, photo_id: int, album_id: int, unique_id: int):
    '''Обработчик для принятия медиа групп
    Работает с:
    [seller: output_boot_config]'''
    # if message.from_user.is_bot:
    #     print('isbot')
    #     return
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
        await asyncio.sleep(2)


        # new_album = [InputMediaPhoto(media=file_id) for file_id in mediagroups[album_id]]

        if state:
            seller_boot_commodity_module = importlib.import_module('handlers.state_handlers.seller_states_handler.load_new_car.get_output_configs')
            state_name = await state.get_state()
            ic(state_name)
            # print(state_name)
            if state_name:
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

                elif state_name.startswith('BootNewCarPhotosStates'):
                    ic()
                    # mediagroupss = [value for value in mediagroups.values()]
                    # mediagroupss = set(mediagroupss)

                    mediagroupss = []
                    for e in mediagroups.values():
                        if e not in mediagroupss:
                            mediagroupss.append(e)
                    if isinstance(mediagroupss[0], list):
                        mediagroupss = mediagroupss[-1]

                    executor = int(state_name.split('_')[-1])-1
                    if executor:
                        pre_data = [[1, 1, 2], [2, 2, 2], [3, 2, 2], [4, 2, 2], [5, 1, 2], [6, 1, 2], [7, 3, 2], [8, 3, 1]]
                        current_part = pre_data[executor]
                        data = [{'admin_id': message.from_user.id,
                                 'car_complectation': current_part[0],
                                'car_engine': current_part[1],
                                 'car_color': current_part[2],
                                 'photo_id': part['id'],
                                 'photo_unique_id': part['unique_id']} for part in mediagroupss]
                    # else:
                    #     executor -= 3
                    #     data = []
                    #     complectations = await manager.execute(CarComplectation.select().join(CarModel).join(CarBrand).where(CarBrand.id == executor))
                    #     engines = await manager.execute(CarEngine.select().join(CarComplectation).join(CarModel).join(CarBrand).where(CarBrand.id == executor))
                    #     car_color = await manager.execute(CarColor.select())
                    #     for complect in complectations:
                    #         for engine in engines:
                    #             for color in car_color:
                    #                 for part in mediagroupss:
                    #                     data.append({'admin_id': message.from_user.id,
                    #                                         'car_complectation': complect.id,
                    #                                         'car_engine': engine.id,
                    #                                         'car_color': color.id,
                    #                                         'photo_id': part['id'],
                    #                                         'photo_unique_id': part['unique_id']})

                    print('load_moment')
                    await state.clear()
                    await PhotoRequester.load_photo_in_base(data)

