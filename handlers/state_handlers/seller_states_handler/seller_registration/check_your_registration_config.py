from typing import Union
import importlib
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from handlers.state_handlers.seller_states_handler.seller_registration.seller_registration_handlers import registartion_view_corrector
from utils.Lexicon import LEXICON


#Фильтр Dealership_name
async def check_your_config(request: Union[CallbackQuery, Message], state: FSMContext, dealership_address=None):
    '''Обработчик конечного состояния регистрации пользовтаеля:
    Сверка введённых рег. данных'''
    message_editor_module = importlib.import_module('handlers.message_editor')
    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт


    if dealership_address:
        await state.update_data(dealership_address=dealership_address)
        print('dealership_address', dealership_address)

    bot = request.chat.bot
    await bot.delete_message(chat_id=request.chat.id, message_id=request.message_id)
    memory_storage = await state.get_data()
    await registartion_view_corrector(request=request, state=state)
    

    lexicon_part = LEXICON['checking_seller_entered_data']
    lexicon_part['rewrite_seller_name'] = memory_storage['seller_name']
    lexicon_part['rewrite_seller_number'] = memory_storage['seller_number']
    seller_mode = await redis_module.redis_data.get_data(key=str(request.from_user.id) + ':seller_registration_mode')
    if seller_mode == 'dealership':
        lexicon_part['rewrite_dealership_address'] = memory_storage['dealership_address']
    # else:
    #     lexicon_part.pop('dealership_address')
    print(lexicon_part)

    edit_mode = await redis_module.redis_data.get_data(key=str(request.from_user.id) + ':can_edit_seller_registration_data')

    if edit_mode == 'true':
        delete_mode = False
    else:
        delete_mode = True


    await message_editor_module.travel_editor.edit_message(lexicon_key=None, request=request, lexicon_part=lexicon_part, delete_mode=True)

    await redis_module.redis_data.set_data(key=str(request.from_user.id) + ':can_edit_seller_registration_data', value='true')



    