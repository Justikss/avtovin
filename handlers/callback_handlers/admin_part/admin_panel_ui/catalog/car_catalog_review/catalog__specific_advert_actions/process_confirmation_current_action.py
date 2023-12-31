import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.data_requests.car_advert_requests import AdvertRequester
from handlers.callback_handlers.sell_part.checkout_seller_person_profile import get_seller_name
from handlers.utils.message_answer_without_callback import send_message_answer
from states.admin_part_states.catalog_states.catalog_review_states import AdminCarCatalogReviewStates
from utils.get_username import get_username
from utils.lexicon_utils.Lexicon import CATALOG_LEXICON
from utils.lexicon_utils.admin_lexicon.admin_catalog_lexicon import catalog_captions

async def confirmation_close_advert_lexicon_part_modification(message: Message, state: FSMContext, close_reason):
    memory_storage = await state.get_data()
    action = memory_storage.get('advert_action_subject')
    current_advert_id = memory_storage.get('current_catalog_advert_id')

    advert_model = await AdvertRequester.get_where_id(current_advert_id)
    ic(advert_model, current_advert_id, action, memory_storage)
    if advert_model:
        seller_entity = await get_seller_name(advert_model.seller, for_admin=True)
        await state.update_data(user_id=advert_model.seller.telegram_id)
        if isinstance(seller_entity, tuple):
            seller_entity = seller_entity[0]

        seller_username = await get_username(message.bot, advert_model.seller.telegram_id)
        advert_caption = '' if action == 'block' else catalog_captions['advert'].format(advert_id=current_advert_id)
        ic(advert_caption, seller_username, seller_entity)
        lexicon_part = CATALOG_LEXICON['catalog_close_advert__confirmation_advert_close_action']
        lexicon_part['message_text'] = lexicon_part['message_text'].format(
            action_subject=catalog_captions[f'catalog_review__make_{action}'],
            seller_entity=seller_entity,
            # telegram_username=seller_username,
            advert_caption=advert_caption,
            action_reason=close_reason
        )
        return lexicon_part
    else:
        await send_message_answer(message, catalog_captions['inactive_advert_or_seller'])


async def confirmation_reason_to_close_advert_admin_handler(message: Message, state: FSMContext, reason):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    await state.set_state(AdminCarCatalogReviewStates.action_confirmation)
    lexicon_part = await confirmation_close_advert_lexicon_part_modification(message, state, reason)
    if lexicon_part:
        await message_editor.travel_editor.edit_message(request=message, lexicon_key='',
                                                        lexicon_part=lexicon_part, delete_mode=True)


