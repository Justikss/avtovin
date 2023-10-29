from aiogram.types import CallbackQuery
import importlib
from aiogram.fsm.context import FSMContext


from handlers.state_handlers.seller_states_handler.seller_registration_handlers import input_seller_name



async def seller_type_identifier(callback: CallbackQuery, state: FSMContext):
    '''Оптимизационный метод, начинающий регистрацию любого типа продавцов'''
    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт
    callback_data = callback.data
    if callback_data == 'i_am_private_person':
        seller_mode = 'person'
    elif callback_data == 'i_am_car_dealership':
        seller_mode = 'dealership'

    await redis_module.redis_data.set_data(key=str(callback.from_user.id) + ':seller_registration_mode', value=seller_mode)
    print('markk')
    return await input_seller_name(request=callback, state=state)

    
    
