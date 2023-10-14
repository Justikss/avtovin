from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from handlers.state_handlers.buyer_registration_handlers import InlineCreator, LEXICON
from handlers.callback_handlers.language_callback_handler import redis_data


async def backward_button_handler(callback: CallbackQuery, state: FSMContext):
    memory_data = await state.get_data()
    if memory_data.get('last_lexicon_code'):
        last_lexicon_code = memory_data['last_lexicon_code']
        last_state = memory_data['last_state']
        await state.set_state(last_state)
    else:
        user_id = callback.from_user.id
        redis_key = str(user_id) + ':last_lexicon_code'
        last_lexicon_code = await redis_data.get_data(redis_key)
        await state.clear()

    lexicon_part = LEXICON[last_lexicon_code]
    print(lexicon_part)
    message_text = lexicon_part['message_text']
    keyboard = await InlineCreator.create_markup(lexicon_part)
    await callback.message.edit_text(text=message_text, reply_markup=keyboard)
    # await callback.answer(text=str(await state.get_state()))

    await state.update_data(last_lexicon_code=None)
    await state.update_data(last_state=None)
