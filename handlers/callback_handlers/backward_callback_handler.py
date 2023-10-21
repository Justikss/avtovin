import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from handlers.state_handlers.buyer_registration_handlers import LEXICON
from handlers.callback_handlers.language_callback_handler import redis_data

from handlers.callback_handlers.FAQ_tech_support import tech_support_callback_handler


async def backward_button_handler(callback: CallbackQuery, state: FSMContext = None):
    '''Кнопка назад, ориентируется на запись в редис: прошлый лексикон код,
                                                        прошлое состояние'''
    mode = callback.data.split(':')
    mode = mode[1]

    if mode == 'support':
        await tech_support_callback_handler(callback=callback)
    else:

        inline_creator = importlib.import_module('keyboards.inline.kb_creator')  # Ленивый импорт
        memory_data = await state.get_data()
        last_lexicon_code = memory_data.get('last_lexicon_code')
        if last_lexicon_code:
            if last_lexicon_code.endswith('(incorrect)'):
                last_lexicon_code = str(last_lexicon_code.split('(')[0])
            last_state = memory_data['last_state']
            await state.set_state(last_state)
            await state.update_data(last_lexicon_code=None)
        else:
            user_id = callback.from_user.id
            redis_key = str(user_id) + ':last_lexicon_code'
            last_lexicon_code = await redis_data.get_data(redis_key)
            await state.clear()


        lexicon_part = LEXICON[last_lexicon_code]
        message_text = lexicon_part['message_text']
        keyboard = await inline_creator.InlineCreator.create_markup(lexicon_part)
        await callback.message.edit_text(text=message_text, reply_markup=keyboard)

        await state.update_data(last_lexicon_code=None)
        await state.update_data(last_state=None)
