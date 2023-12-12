import importlib

from aiogram.fsm.context import FSMContext

from handlers.utils.inline_buttons_pagination_heart import CachedRequestsView
from utils.create_lexicon_part import create_lexicon_part


async def output_choose(callback, state: FSMContext, lexicon_class, models_range, page_size, need_last_buttons=True):
    redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
    redis_key = f'{str(callback.from_user.id)}:inline_buttons_pagination_data'
    await redis_module.redis_data.delete_key(key=redis_key)
    ic(lexicon_class.message_text)
    await state.update_data(message_text=lexicon_class.message_text)
    await state.update_data(dynamic_buttons=lexicon_class.dynamic_buttons)
    await state.update_data(last_buttons=lexicon_class.last_buttons)
    await state.update_data(width=lexicon_class.width)
    lexicon_part = await create_lexicon_part(lexicon_class, models_range, state=state, request=callback, need_last_buttons=need_last_buttons)
    ic(lexicon_part)
    await CachedRequestsView.output_message_with_inline_pagination(callback, car_brands=lexicon_part['buttons'],
                                                                   state=state, pagesize=page_size)