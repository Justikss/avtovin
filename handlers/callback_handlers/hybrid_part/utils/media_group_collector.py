import asyncio
import importlib
import logging
import os

import httpx
from aiogram.exceptions import TelegramNetworkError
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputMediaPhoto, FSInputFile
from httpx import ConnectError

from handlers.custom_filters.message_is_photo import MessageIsPhoto
from handlers.state_handlers.seller_states_handler.load_new_car.hybrid_handlers import input_photo_to_load
from handlers.utils.delete_message import delete_message
from states.admin_part_states.catalog_states.advert_parameters_states import AdminAdvertParametersStates
from states.load_commodity_states import LoadCommodityStates
from utils.middleware.update_spam_defender.modules.language import LanguageMiddlewareModule

# from utils.photo_utils.insert_watermark import insert_watermark

mediagroups = dict()
min_side_size = 400
user_messages = dict()
media_incorect_flag = dict()

seller_boot_commodity_module = importlib.import_module(
    'handlers.state_handlers.seller_states_handler.load_new_car.get_output_configs')


async def collect_and_send_mediagroup(message: Message, state: FSMContext, photo_id: int, unique_id: int,
                                      photo_width: int, photo_height: int):

    new_car_state_parameters_module = importlib.import_module(
        'handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.new_car_state_parameters_handler')

    '''Обработчик для принятия медиа групп
    Работает с:
    [seller: output_boot_config]'''
    # if message.from_user.is_bot:
    #
    #     return
    user_id = message.from_user.id
    if not user_messages.get(user_id):
        user_messages[user_id] = []

    if not mediagroups.get(user_id):
        mediagroups[user_id] = dict()
    # try:
    #     await message.delete()
    # except:
    #     pass
    ic()
    ic(state)
    state_name = await state.get_state()
    if not state_name in (LoadCommodityStates.photo_verification,
                             AdminAdvertParametersStates.NewStateStates.await_input_new_car_photos):

        return
        # pass
    album_id = message.media_group_id
    ic(album_id)
    if album_id:
        ic(photo_height, photo_width)
        ic(min_side_size)
        ic(photo_height < min_side_size, photo_width < min_side_size)
        ic(any(side < min_side_size for side in (photo_height, photo_width)), state_name, state_name == 'LoadCommodityStates:photo_verification')
        if any(side < min_side_size for side in (photo_height, photo_width)) and state_name == 'LoadCommodityStates:photo_verification':
            media_incorect_flag[user_id] = 'size'
        if album_id in mediagroups.get(user_id):
            mediagroups[user_id][album_id].append({'id': photo_id, 'unique_id': unique_id})
            user_messages[user_id].append(message.message_id)
            return
        mediagroups[user_id][album_id] = [{'id': photo_id, 'unique_id': unique_id}]
        user_messages[user_id].append(message.message_id)
        await asyncio.sleep(2.5)
        # media_group = await insert_watermark(mediagroups[album_id], message.chat.id, message.bot)
        await delete_message(message, user_messages[user_id])

        # new_album = [InputMediaPhoto(media=file_id) for file_id in mediagroups[album_id]]

        # await handle_user_input_photos(album_id, message, state)
        ic(mediagroups, user_messages)
        if state:

            state_name = await state.get_state()
            ic(state_name)
            #
            if state_name:
                if state_name in ('LoadCommodityStates:photo_verification', 'AdminAdvertParametersStates.NewStateStates:await_input_new_car_photos'):
                    if not 5 <= len(mediagroups[user_id][album_id]) <= 8:

                        photo_filter = MessageIsPhoto()
                        mediagroups[user_id].clear()
                        user_messages[user_id].clear()
                        media_incorect_flag[user_id] = None

                        await photo_filter(message=message, state=state)
                        return
                    match state_name:
                        case 'LoadCommodityStates:photo_verification':
                            memory_storage = await state.get_data()
                            # media_incorect_flag = memory_storage.get('media_incorect_flag')
                            ic(media_incorect_flag)
                            ic()
                            if media_incorect_flag.get(user_id):
                                await input_photo_to_load(message, state, incorrect='size')
                                del media_incorect_flag[user_id]
                            else:
                                await handle_user_input_photos(mediagroups[user_id][album_id], message, state)
                        case 'AdminAdvertParametersStates.NewStateStates:await_input_new_car_photos':
                            await new_car_state_parameters_module\
                                .NewCarStateParameters().callback_handler(message, state, media_photos=mediagroups[user_id])
                    mediagroups[user_id].clear()

            elif state_name == "MailingStates:uploading_media":
                result = mediagroups[user_id]
                mediagroups[user_id].clear()
                return result
    else:
        await delete_message(message, user_messages[user_id])

        if state:
            state_name = await state.get_state()
            ic(state_name)
            #
            if state_name:
                match state_name:
                    case 'LoadCommodityStates:photo_verification':
                        await seller_boot_commodity_module.output_load_config_for_seller(request=message, state=state,
                                                                                         media_photos=mediagroups[user_id])
                    case 'AdminAdvertParametersStates.NewStateStates:await_input_new_car_photos':
                        await new_car_state_parameters_module\
                            .NewCarStateParameters().callback_handler(message, state, media_photos=mediagroups[user_id])


async def handle_user_input_photos(mediagroups, message, state):
    redis_data_module = importlib.import_module('utils.redis_for_language')
    message_editor_module = importlib.import_module('handlers.message_editor')
    Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

    bot = message.bot
    chat_id = message.chat.id

    async def send_watermark_request(photo_urls):
        url = 'http://localhost:8000/watermark/'
        data = {"photo_list": photo_urls}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=data)
            except ConnectError:
                logging.critical(f"Ошибка ConnectError запроса на добавление вотермарки фотографии\nInputted urls: %s"
                                 f"сервер сервиса выключен.",
                                 str(photo_urls))
                return False
            if response.status_code == 200:
                return response.json()
            else:
                logging.critical(f"Ошибка запроса на добавление вотермарки фотографии\nInputted urls: %s"
                                 f"status code: %d",
                                 str(photo_urls),
                                 response.status_code)



    async def async_remove_photos(file_path):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, os.remove, file_path)

    # await message_editor_module.travel_editor.edit_message(request=message,
    #                                                        lexicon_part=Lexicon_module.LEXICON['awaiting_process'],
    #                                                        lexicon_key='')

    tasks = [bot.get_file(mediagroup['id']) for mediagroup in mediagroups]
    files_info = await asyncio.gather(*tasks)
    urls = [f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}" for file_info in files_info]


    photo_paths = await send_watermark_request(urls)
    ic(photo_paths)
    if photo_paths:
        photo_paths = photo_paths['file_paths']
        medias = [FSInputFile(path) for path in photo_paths]
        with_watermark = True
    else:
        with_watermark = False

        medias = [photo['id'] for photo in mediagroups]
        # from handlers.utils.message_answer_without_callback import send_message_answer
        # Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
        #
        # await send_message_answer(message, Lexicon_module.ADMIN_LEXICON['unsuccessfully'])
        # await seller_boot_commodity_module.output_load_config_for_seller(request=message, state=state,
        #                                                                  media_photos=[])
        # return
    media_group = [InputMediaPhoto(media=media) for media in medias]
    ic(media_group)
    try:
        sendned_media_groups = await bot.send_media_group(chat_id, media=media_group)
        media_photos = [{'id': media_message.photo[-1].file_id, 'unique_id': media_message.photo[-1].file_unique_id} for
                        media_message in sendned_media_groups]

        await redis_data_module.redis_data.set_data(key=f'{chat_id}:last_media_group',
                                                    value=[media_message.message_id
                                                           for media_message in sendned_media_groups])

        await seller_boot_commodity_module.output_load_config_for_seller(request=message, state=state,
                                                                         media_photos=media_photos)
    except Exception as ex:
        from handlers.utils.message_answer_without_callback import send_message_answer
        Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

        await send_message_answer(message, Lexicon_module.ADMIN_LEXICON['unsuccessfully'])
        # await LanguageMiddlewareModule()(message)
        await seller_boot_commodity_module.output_load_config_for_seller(request=message, state=state,
                                                                         media_photos=[])
        logging.critical('Ошибка при отправке фотографий с вотермаркой в чат: %s'
                         'photo_paths: %s'
                         'urls: %s', ex, str(photo_paths), str(urls))
        return
    finally:
        if with_watermark:
            delete_photos_tasks = [async_remove_photos(file_path) for file_path in photo_paths]
            await asyncio.gather(*delete_photos_tasks)