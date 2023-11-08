from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
import importlib

from config_data.config import ADMIN_CHAT
from utils.Lexicon import LexiconCommodityLoader, LEXICON
from database.data_requests.commodity_requests import CommodityRequester
from handlers.state_handlers.seller_states_handler.load_new_car.get_output_configs import data_formatter

async def confirm_load_config_from_seller(callback: CallbackQuery, state: FSMContext):
    '''Обработчик одобрения собственных конфигураций загрузки нового авто от селлера.'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    await message_editor.redis_data.delete_key(key=str(callback.from_user.id) + ':can_edit_seller_boot_commodity')

    boot_data = await data_formatter(request=callback, state=state)

    await state.clear()

    commodity_number = CommodityRequester.store_data([boot_data])
    print('load_proc -=',  commodity_number)

    notification_string = await LexiconCommodityLoader.create_notification_for_seller(request_number=commodity_number)
    mock_lexicon_part = {'message_text': notification_string}
    lexicon_part = LEXICON['seller_load_notification_button']
    for key, value in lexicon_part.items():
        mock_lexicon_part[key] = value
    mock_lexicon_part['width'] = 1

    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=mock_lexicon_part)

    last_output_boot_config_string = await message_editor.redis_data.get_data(key=str(callback.from_user.id) + ':boot_config')
    boot_config_string_startswith = LexiconCommodityLoader.config_for_admins + callback.from_user.username + ' :'

    message_for_admin_chat = last_output_boot_config_string.split('\n')[:-2]
    message_for_admin_chat[0] = boot_config_string_startswith
    message_for_admin_chat = '\n'.join(message_for_admin_chat)

    photo = boot_data['photo_id'] #if not None else boot_data['photo_url']
    print('photo_id: ', photo)
    await callback.message.bot.send_photo(chat_id=ADMIN_CHAT, caption=message_for_admin_chat, photo=photo)