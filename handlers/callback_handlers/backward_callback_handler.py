import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.callback_handlers.search_auto_handler import search_auto_callback_handler
from handlers.state_handlers.buyer_registration_handlers import LEXICON, input_full_name, BuyerRegistationStates
from handlers.callback_handlers.language_callback_handler import redis_data, set_language

from handlers.callback_handlers.FAQ_tech_support import tech_support_callback_handler


async def backward_button_handler(callback: CallbackQuery, state: FSMContext = None):
    '''Кнопка назад, ориентируется на запись в редис: прошлый лексикон код,

                                                        прошлое состояние'''
    inline_creator = importlib.import_module('keyboards.inline.kb_creator')  # Ленивый импорт
    redis_storage = importlib.import_module('utils.redis_for_language')  # Ленивый импорт


    if ':' in callback.data:
        mode = callback.data.split(':')
        mode = mode[1]

        if mode == 'support':
            await tech_support_callback_handler(callback=callback)

        elif mode == 'choose_car_category':
            print('choty')
            await search_auto_callback_handler(callback=callback)

        elif mode == 'set_language':
            await set_language(callback=callback)

        elif mode.startswith('user_registration'):

            last_user_message = int(
                await redis_storage.redis_data.get_data(key=str(callback.from_user.id) + ':last_user_message'))
            if last_user_message:
                await callback.message.chat.delete_message(message_id=last_user_message)
                await redis_storage.redis_data.delete_key(key=str(callback.from_user.id) + ':last_user_message')

            if mode == 'user_registration_number':
                await state.set_state(BuyerRegistationStates.input_full_name)
                await input_full_name(request=callback, state=state)
            else:
                await state.clear()
                await callback.message.delete()

                user_id = callback.from_user.id
                redis_key = str(user_id) + ':last_lexicon_code'
                last_lexicon_code = await redis_data.get_data(redis_key)

                lexicon_part = LEXICON[last_lexicon_code]
                message_text = lexicon_part['message_text']
                keyboard = await inline_creator.InlineCreator.create_markup(lexicon_part)
                message_object = await callback.message.answer(text=message_text, reply_markup=keyboard)
                await redis_storage.redis_data.set_data(key=str(user_id) + ':last_message', value = message_object.message_id)

    else:

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
