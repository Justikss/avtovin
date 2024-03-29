import importlib

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from states.admin_part_states.users_review_states import SellerReviewStates, BuyerReviewStates

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

async def lexicon_part_to_start_input_search_name_constructor(incorrect, redis_value, memory_storage):
    from utils.safe_dict_class import current_language
    Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
    user_mode = memory_storage.get('admin_review_user_mode')
    format_kwargs = dict()
    lexicon_part = Lexicon_module.ADMIN_LEXICON['input_name_to_search_process']
    if incorrect:
        if incorrect != '(non_exists)' and redis_value:
            lexicon_key_endswith = redis_value
        else:
            lexicon_key_endswith = ''

        ic(lexicon_key_endswith)
        lexicon_part['message_text'] = Lexicon_module.ADMIN_LEXICON[f'''input_name_to_search_process{incorrect}{lexicon_key_endswith}''']
    else:
        format_kwargs = {
            'name_caption': Lexicon_module.ADMIN_LEXICON.get('fullname_caption' if user_mode != 'legal' else 'dealership_name_caption'),
            'user_entity': Lexicon_module.ADMIN_LEXICON.get('user_entity_caption' if user_mode != 'legal' else 'dealership_entity_caption')}
    users_block_state = memory_storage.get('users_block_state')
    users_block_state_caption = Lexicon_module.ADMIN_LEXICON.get(f'banned_users_caption_parent_case:{users_block_state}')

    if incorrect == '(non_exists)' and current_language.get() != 'uz':
        word = users_block_state_caption.strip('<i>').strip('</i>')  # Извлечение слова
        capitalized_word = word[0].upper() + word[1:]  # Преобразование первой буквы в заглавную
        users_block_state_caption = f'<i>{capitalized_word}</i>'  # Возвращение слова в теги
    elif incorrect and current_language.get() == 'uz':
        users_block_state_caption = users_block_state_caption.lower()
    format_kwargs.update({'block_state': users_block_state_caption})
    lexicon_part['message_text'] = lexicon_part['message_text'].format(**format_kwargs)
    return lexicon_part

async def input_person_name_to_search_request_handler(request: CallbackQuery | Message, state: FSMContext, incorrect=None):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    ic(incorrect)
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

    lexicon_part = await lexicon_part_to_start_input_search_name_constructor(incorrect, redis_value, memory_storage)
    ic(lexicon_part)
    reply_to_message = await incorrect_input_controller(request, state, incorrect)
    await message_editor.travel_editor.edit_message(request=request, lexicon_key='',
                                                    lexicon_part=lexicon_part, reply_message=reply_to_message,
                                                    delete_mode= True if reply_to_message else False)