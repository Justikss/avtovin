import importlib

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from states.admin_part_states.users_review_states import SellerReviewStates, BuyerReviewStates
from utils.lexicon_utils.Lexicon import ADMIN_LEXICON

async def incorrect_input_controller(request: CallbackQuery | Message, state: FSMContext, incorrect):
    memory_storage = await state.get_data()


    if incorrect:
        if not memory_storage.get('admin_incorrect_flag'):
            await state.update_data(admin_incorrect_flag=True)
        last_message = memory_storage.get('last_admin_message')
        if last_message:
            try:
                await request.chat.delete_message(last_message)
            except TelegramBadRequest:
                pass

        await state.update_data(last_admin_message=request.message_id)
        return request.message_id

async def lexicon_part_to_start_input_search_name_constructor(incorrect, redis_value):
    lexicon_part = ADMIN_LEXICON['input_name_to_search_process']
    if incorrect:
        if incorrect != '(non_exists)' and redis_value:
            lexicon_key_endswith = redis_value
        else:
            lexicon_key_endswith = ''
        ic(lexicon_key_endswith)
        lexicon_part['message_text'] = ADMIN_LEXICON[f'''input_name_to_search_process{incorrect}{lexicon_key_endswith}''']
    return lexicon_part

async def input_person_name_to_search_request_handler(request: CallbackQuery | Message, state: FSMContext, incorrect=None):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    current_state = str(await state.get_state())
    ic(current_state, incorrect)
    memory_storage = await state.get_data()
    search_mode = memory_storage.get('admin_review_user_mode')
    if not current_state.endswith('search'):
        match search_mode:
            case 'natural':
                state_to_set = SellerReviewStates.natural_entity_search
            case 'legal':
                state_to_set = SellerReviewStates.legal_entity_search
            case 'buyer':
                state_to_set = BuyerReviewStates.buyer_entity_search
            case _:
                state_to_set = None

        if state_to_set:
            await state.set_state(state_to_set)
        ic(state_to_set, search_mode)
    redis_value = None
    current_state = str(await state.get_state())
    if current_state.endswith('legal_entity_search'):
        redis_value = 'dealership'

    await message_editor.redis_data.set_data(f'{request.from_user.id}:seller_registration_mode', value=redis_value)

    lexicon_part = await lexicon_part_to_start_input_search_name_constructor(incorrect, redis_value)

    reply_to_message = await incorrect_input_controller(request, state, incorrect)
    await message_editor.travel_editor.edit_message(request=request, lexicon_key='',
                                                    lexicon_part=lexicon_part, reply_message=reply_to_message,
                                                    delete_mode= True if reply_to_message else False)