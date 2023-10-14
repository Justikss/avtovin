from typing import Union

import phonenumbers
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, chat
from phonenumbers import NumberParseException

from handlers.callback_handlers.main_menu import main_menu
from utils.Lexicon import LEXICON
from keyboards.inline.kb_creator import InlineCreator
from handlers.callback_handlers.language_callback_handler import redis_data
from database.data_requests.user_requests import UserRequester


class BuyerRegistationStates(StatesGroup):
    input_full_name = State()
    input_phone_number = State()
    finish_check_phone_number = State()


async def elements_is_alpha(string: list) -> bool:
    '''Проверка списка из слов: состоян ли они только из букв'''
    for word in string:
        if not word.isalpha():
            return False
    return True


async def load_user_in_database(memory_dict, number, message: Message):
    full_name = memory_dict['username']
    full_name = full_name.split()
    struct_for_database = dict()
    struct_for_database['telegram_id'] = message.from_user.id
    struct_for_database['name'] = full_name[1]
    struct_for_database['surname'] = full_name[0]
    if len(full_name) == 3:
        patronymic_value = full_name[2]
    else:
        patronymic_value = None
    struct_for_database['patronymic'] = patronymic_value
    struct_for_database['phone_number'] = number
    UserRequester.store_data(struct_for_database)

'''ДАЛЬШЕ ОБРАБОТЧИКИ СОСТОЯНИЙ'''


async def input_full_name(request: Union[CallbackQuery, Message], state: FSMContext, incorrect=False):
    memory_storage = await state.get_data()
    message_id = memory_storage['last_message']
    if incorrect:
        lexicon_code = 'write_full_name(incorrect)'
    else:
        lexicon_code = 'write_full_name'


        await chat.Chat.delete_message(self=request.message.chat, message_id=message_id)

    lexicon_part = LEXICON[lexicon_code]

    await state.update_data(last_lexicon_code=None)
    await state.update_data(last_state=None)

    await state.update_data(current_lexicon_code=lexicon_code)
    await state.update_data(current_state=await state.get_state())


    message_text = lexicon_part['message_text']
    keyboard = await InlineCreator.create_markup(lexicon_part)

    if isinstance(request, CallbackQuery):
        message_object = await request.message.answer(text=message_text, reply_markup=keyboard)
    else:
        message_object = await request.answer(text=message_text, reply_markup=keyboard)

    await state.update_data(last_message=message_object.message_id)
    await state.set_state(BuyerRegistationStates.input_phone_number)

async def input_phone_number(message: Message, state: FSMContext, incorrect=False, user_name: str = None):
    memory_storage = await state.get_data()
    message_id = memory_storage['last_message']

    await chat.Chat.delete_message(self=message.chat, message_id=message_id)

    if user_name:
        await state.update_data(username=user_name)

    if incorrect:
        lexicon_code = 'write_phone_number(incorrect)'
    else:
        lexicon_code = 'write_phone_number'

    lexicon_part = LEXICON[lexicon_code]
    await state.update_data(last_lexicon_code=memory_storage['current_lexicon_code'])
    await state.update_data(last_state=await state.get_state())

    await state.update_data(current_lexicon_code=None)
    await state.update_data(current_state=None)


    message_text = lexicon_part['message_text']

    keyboard = await InlineCreator.create_markup(lexicon_part)

    message_object = await message.answer(text=message_text, reply_markup=keyboard)

    user_id = message.from_user.id
    redis_key = str(user_id) + ':last_message'
    await redis_data.set_data(redis_key, message_object.message_id)

    await state.update_data(last_message=message_object.message_id)
    await state.set_state(BuyerRegistationStates.finish_check_phone_number)


async def finish_check_phone_number(message: Message, state: FSMContext):
    user_id = message.from_user.id
    redis_key = str(user_id) + ':language'
    country = await redis_data.get_data(key=redis_key)

    try:
        input_number = phonenumbers.parse(message.text, country)
        number_is_valid = phonenumbers.is_valid_number(input_number)
        if number_is_valid:
            memory_storage = await state.get_data()
            await load_user_in_database(memory_storage, input_number, message)

            await state.clear()

            await main_menu(request=message)
        else:
            await input_phone_number(message=message, state=state, incorrect=True)
    except NumberParseException:
        await input_phone_number(message=message, state=state, incorrect=True)