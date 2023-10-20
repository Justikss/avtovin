import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery


async def cache_state(callback: CallbackQuery, state: FSMContext, first=False):
    redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
    redis_key = str(callback.from_user.id) + ':state_history_stack'
    if first:
        state_stack = [await state.get_state()]
        await redis_module.redis_data.set_data(key=redis_key, value=state_stack)
        print('first_state', state_stack)
    else:
        state_stack = await redis_module.redis_data.get_data(key=redis_key, use_json=True)
        current_state = await state.get_state()
        if state_stack[-1] != current_state:
            state_stack.append(current_state)
            await redis_module.redis_data.set_data(key=redis_key, value=state_stack)
            print('state_stack[-1] != current_state', state_stack)
        print('state_stack[-1] == current_state')



