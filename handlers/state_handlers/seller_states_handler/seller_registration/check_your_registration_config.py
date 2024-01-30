from copy import copy
from typing import Union
import importlib
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext



#Фильтр Dealership_name
async def check_your_config(request: Union[CallbackQuery, Message], state: FSMContext, dealership_address=None, from_backward_Delete_mode=None):
    '''Обработчик конечного состояния регистрации пользовтаеля:
    Сверка введённых рег. данных'''
    Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
    message_editor_module = importlib.import_module('handlers.message_editor')
    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт
    buyer_registration_module = importlib.import_module('handlers.state_handlers.buyer_registration_handlers')

    if isinstance(request, CallbackQuery):
        chat_id = request.message.chat.id
        bot = request.message.chat.bot
        message_id = request.message.message_id
    else:
        message_id = request.message_id

        chat_id = request.chat.id
        bot = request.chat.bot

    if dealership_address:
        dealership_address = ' '.join([address_part.capitalize() for address_part in dealership_address.split(' ')])
        await state.update_data(dealership_address=dealership_address)

    from handlers.utils.delete_message import delete_message
    await delete_message(request, message_id)
    # await bot.delete_message(chat_id=chat_id, message_id=message_id)

    memory_storage = await state.get_data()
    await buyer_registration_module.registartion_view_corrector(request=request, state=state)

    lexicon_part = copy(Lexicon_module.LEXICON['checking_seller_entered_data'])
    lexicon_part['rewrite_seller_name'] = memory_storage['seller_name']
    lexicon_part['rewrite_seller_number'] = memory_storage['seller_number']
    seller_mode = await redis_module.redis_data.get_data(key=str(request.from_user.id) + ':seller_registration_mode')
    if seller_mode == 'dealership':
        lexicon_part['rewrite_dealership_address'] = Lexicon_module.LEXICON['address']
        lexicon_part['message_text'] = f'''{lexicon_part['message_text']}\n{Lexicon_module.LEXICON['incoming_address_caption']}{memory_storage['dealership_address']}'''
    # else:
    #     lexicon_part.pop('dealership_address')

    edit_mode = await redis_module.redis_data.get_data(key=str(request.from_user.id) + ':can_edit_seller_registration_data')

    if edit_mode == 'true':
        delete_mode = False
    else:
        delete_mode = True


    await message_editor_module.travel_editor.edit_message(lexicon_key=None, request=request, lexicon_part=lexicon_part, delete_mode=True)

    await redis_module.redis_data.set_data(key=str(request.from_user.id) + ':can_edit_seller_registration_data', value='true')



    