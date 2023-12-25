import importlib

from aiogram.fsm.context import FSMContext

from utils.lexicon_utils.Lexicon import LEXICON

async def remove_last_inline_pagination_data(callback):
    redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
    redis_key = f'{str(callback.from_user.id)}:inline_buttons_pagination_data'
    await redis_module.redis_data.delete_key(key=redis_key)
async def set_state_data(lexicon_class, state: FSMContext):
    await state.update_data(message_text=lexicon_class.message_text)
    await state.update_data(width=lexicon_class.width)
    if hasattr(lexicon_class, 'dynamic_buttons'):
        await state.update_data(dynamic_buttons=lexicon_class.dynamic_buttons)
    if hasattr(lexicon_class, 'last_buttons'):
        await state.update_data(last_buttons=lexicon_class.last_buttons)
    if hasattr(lexicon_class, 'backward_command'):
        if lexicon_class.backward_command:
            await state.update_data(backward_command=lexicon_class.backward_command)

async def output_choose(callback, state: FSMContext, lexicon_class, models_range, page_size, need_last_buttons=True):
    create_lexicon_part_module = importlib.import_module('handlers.state_handlers.choose_car_for_buy.hybrid_handlers')
    inline_pagination_module = importlib.import_module('handlers.utils.inline_buttons_pagination_heart')

    if not models_range:
        return await callback.answer(LEXICON['search_parameter_invalid'])

    await remove_last_inline_pagination_data(callback)

    ic(lexicon_class.message_text)

    await set_state_data(lexicon_class, state)

    lexicon_part = await create_lexicon_part_module.create_lexicon_part(lexicon_class, models_range, state=state, request=callback, need_last_buttons=need_last_buttons)
    await state.update_data(message_text=lexicon_part['message_text'])
    # ic(lexicon_class.last_buttons)
    ic(lexicon_part)

    await inline_pagination_module.CachedRequestsView.output_message_with_inline_pagination(callback, buttons_data=lexicon_part['buttons'],
                                                                   state=state, pagesize=page_size)