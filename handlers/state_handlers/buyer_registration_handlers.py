import importlib
from typing import Union

from aiogram.exceptions import TelegramBadRequest
import phonenumbers
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, chat
from phonenumbers import NumberParseException
from handlers.callback_handlers.buy_part.main_menu import main_menu
from keyboards.reply.reply_markup_creator import create_reply_markup


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
    person_requester_module = importlib.import_module('database.data_requests.person_requests')

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
    await person_requester_module.PersonRequester.store_data(struct_for_database, user=True)


async def registartion_view_corrector(request: Union[Message, CallbackQuery], state: FSMContext, delete_mode=False):
    '''Вспомогательный метод'''
    redis_storage = importlib.import_module('utils.redis_for_language')  # Ленивый импорт

    if isinstance(request, Message):
        message = request
    else:
        return

    if delete_mode:
        last_message_id = await redis_storage.redis_data.get_data(key=str(message.from_user.id) + ':last_message')
        if last_message_id:

            from handlers.utils.delete_message import delete_message
            await delete_message(request, last_message_id)
            await redis_storage.redis_data.delete_key(key=str(message.from_user.id) + ':last_message')

    memory_data = await state.get_data()
    # if message.message_id:
    #     last_user_answer = message.message_id
    # else:
    last_user_answer = await redis_storage.redis_data.get_data(key=str(request.from_user.id) + ':last_user_message')

    incorrect_flag = memory_data.get('incorrect_answer')


    if last_user_answer:
        from handlers.utils.delete_message import delete_message
        if incorrect_flag:
            await delete_message(request, last_user_answer)

            await redis_storage.redis_data.set_data(key=str(request.from_user.id) + ':last_user_message',
                                                    value=message.message_id)

            await state.update_data(incorrect_answer=False)
        else:

            await delete_message(request, last_user_answer)

            await redis_storage.redis_data.delete_key(key=str(request.from_user.id) + ':last_user_message')

'''ДАЛЬШЕ ОБРАБОТЧИКИ СОСТОЯНИЙ'''


async def input_full_name(request: Union[CallbackQuery, Message], state: FSMContext, incorrect=None, from_backward=None):
    await state.update_data(incorrect_answer=False)
    inline_creator = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт
    redis_storage = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

    # if from_backward:
    #     from keyboards.reply.delete_reply_markup import delete_reply_markup
    #     await delete_reply_markup(request)

    memory_storage = await state.get_data()
    message_id = await redis_storage.redis_data.get_data(key=str(request.from_user.id) + ':last_message')
    lexicon_part = lexicon_module.LEXICON['write_full_name']
    lexicon_code = 'write_full_name'
    if incorrect:
        lexicon_part['message_text'] =  lexicon_module.LEXICON[f'write_full_name{incorrect}']
        await state.update_data(incorrect_answer=True)
        await registartion_view_corrector(request=request, state=state)

    else:
        await state.update_data(incorrect_answer=False)
        #try:
        from handlers.utils.delete_message import delete_message
        await delete_message(request, message_id)


    await state.update_data(last_lexicon_code=None)
    await state.update_data(last_state=None)

    await state.update_data(current_lexicon_code=lexicon_code)
    await state.update_data(current_state=await state.get_state())
    ic(lexicon_part)
    message_text = lexicon_part['message_text']
    ic(message_text)
    keyboard = await inline_creator.InlineCreator.create_markup(lexicon_part)


    if isinstance(request, CallbackQuery):
        message = request.message
    else:
        message = request
    if incorrect:
        message_object = await message.reply(text=message_text, reply_markup=keyboard)
        await redis_storage.redis_data.set_data(key=str(request.from_user.id) + ':last_user_message', value=message.message_id)

    else:
        message_object = await message.answer(text=message_text, reply_markup=keyboard)

    await redis_storage.redis_data.set_data(key=str(request.from_user.id) + ':last_message', value=message_object.message_id)
    await state.set_state(BuyerRegistationStates.input_phone_number)
    ic(await state.get_state())

async def input_phone_number(message: Message, state: FSMContext, incorrect=None, user_name: str = None):
    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт
    inline_creator = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

    memory_storage = await state.get_data()
    message_id = await redis_module.redis_data.get_data(key=str(message.from_user.id) + ':last_message')

    lexicon_part = lexicon_module.LEXICON['write_phone_number']



    if user_name:
        user_name = ' '.join([name_part.capitalize() for name_part in user_name.split(' ')])
        await state.update_data(username=user_name)

    if incorrect:
        lexicon_part['message_text'] = lexicon_module.LEXICON[f'write_phone_number{incorrect}']
        await state.update_data(incorrect_answer=True)

    else:
        await message.delete()
        await state.update_data(incorrect_answer=False)

    await registartion_view_corrector(request=message, state=state)


    await state.update_data(last_lexicon_code=memory_storage['current_lexicon_code'])
    await state.update_data(last_state=await state.get_state())

    await state.update_data(current_lexicon_code=None)
    await state.update_data(current_state=None)

    message_text = lexicon_part['message_text']

    from keyboards.inline.kb_creator import InlineCreator
    # if isinstance(message, Message):
    if not incorrect:
        from keyboards.reply.send_reply_markup import send_reply_button_contact
        await send_reply_button_contact(message)
    keyboard = await InlineCreator.create_markup(lexicon_part)

    from handlers.utils.delete_message import delete_message
    await delete_message(message, message_id)

    if incorrect:
        message_object = await message.reply(text=message_text, reply_markup=keyboard)
        await redis_module.redis_data.set_data(key=str(message.from_user.id) + ':last_user_message',
                                               value=message.message_id)
    else:
        message_object = await message.answer(text=message_text, reply_markup=keyboard)

    user_id = message.from_user.id
    redis_key = str(user_id) + ':last_message'
    await redis_module.redis_data.set_data(redis_key, message_object.message_id)

    await state.set_state(BuyerRegistationStates.finish_check_phone_number)


async def finish_check_phone_number(message: Message, state: FSMContext, input_number):
    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт

    user_id = message.from_user.id
    redis_key = str(user_id) + ':language'
    country = await redis_module.redis_data.get_data(key=redis_key)
    number = input_number



    try:

        # input_number = phonenumbers.parse(number, country)
        # number_is_valid = phonenumbers.is_valid_number(input_number)
        #

        await message.delete()
        await registartion_view_corrector(request=message, state=state)
        memory_storage = await state.get_data()
        # formatted_number = '-'.join(phonenumbers.format_number(input_number, phonenumbers.PhoneNumberFormat.NATIONAL).split())

        await load_user_in_database(memory_storage, number, message)

        await state.clear()

        await main_menu(request=message, state=state)

    except NumberParseException:
        await input_phone_number(message=message, state=state, incorrect='(novalid)')

