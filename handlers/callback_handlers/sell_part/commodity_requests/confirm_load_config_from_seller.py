from copy import copy

from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
import importlib

from config_data.config import ADMIN_CHAT
from database.data_requests.car_configurations_requests import CarConfigs
from utils.Lexicon import LexiconCommodityLoader, LEXICON
from handlers.state_handlers.seller_states_handler.load_new_car.get_output_configs import data_formatter



async def create_notification_for_seller(request_number) -> str:
    '''Плашка "Заявка №XXXX Создана"'''
    create_request_notification = LexiconCommodityLoader.seller_notification['message_text']
    create_request_notification = create_request_notification.split('_')
    create_request_notification = f'{request_number}'.join(create_request_notification)

    return create_request_notification


async def confirm_load_config_from_seller(callback: CallbackQuery, state: FSMContext):
    '''Обработчик одобрения собственных конфигураций загрузки нового авто от селлера.'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    media_group_delete_module = importlib.import_module('utils.chat_cleaner.media_group_messages')

    await message_editor.redis_data.delete_key(key=str(callback.from_user.id) + ':can_edit_seller_boot_commodity')

    boot_data = await data_formatter(request=callback, state=state, id_values=True)

    print('load_photos??: ', boot_data.get('photos'))
    commodity_number = await CarConfigs.add_advert(callback.from_user.id, boot_data)

    notification_string = await create_notification_for_seller(request_number=commodity_number)
    mock_lexicon_part = {'message_text': notification_string}
    lexicon_part = LEXICON['seller_load_notification_button']
    for key, value in lexicon_part.items():
        mock_lexicon_part[key] = value
    mock_lexicon_part['width'] = 1

    await media_group_delete_module.delete_media_groups(request=callback)
    print('await mock_lex_par')
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=mock_lexicon_part, delete_mode=True)

    last_output_boot_config_string = await message_editor.redis_data.get_data(key=str(callback.from_user.id) + ':boot_config')
    boot_config_string_startswith = copy(LexiconCommodityLoader.config_for_admins) + callback.from_user.username + ' :'

    message_for_admin_chat = last_output_boot_config_string.split('\n')[:-2]
    message_for_admin_chat[0] = boot_config_string_startswith
    message_for_admin_chat = '\n'.join(message_for_admin_chat)

    photos = boot_data.get('photos')
    if not photos:
        memory_data = await state.get_data()
        photos = memory_data.get('load_photo')
    print('load_photos hand??: ', photos)
    print('photo_id: ', photos)
    print('isit: ', message_for_admin_chat)
    # await callback.message.bot.send_photo(chat_id=ADMIN_CHAT, caption=message_for_admin_chat, photo=photo)
    ic(photos)
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
                                                    lexicon_part={'message_text': message_for_admin_chat},
                                                    send_chat=ADMIN_CHAT, media_group=photos)
    await callback.answer()
    await state.clear()
