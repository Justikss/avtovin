import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.data_requests.recomendations_request import RecommendationRequester


async def insert_numbers_in_buttons(callback: CallbackQuery):
    Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
    offer_requester = importlib.import_module('database.data_requests.offers_requests')
    user_id = callback.from_user.id

    confirm_offers = await offer_requester.OffersRequester.get_for_buyer_id(buyer_id=user_id)

    non_confirm_offers = await offer_requester.CachedOrderRequests.get_cache(buyer_id=user_id)

    recommendated_offers = await RecommendationRequester.retrieve_by_buyer_id(buyer_id=user_id)
    ic(non_confirm_offers)
    lexicon_part = Lexicon_module.LEXICON['buyer_requests']
    lexicon_part['buttons']['buyer_active_offers'] = lexicon_part['buttons']['buyer_active_offers'].format(
        confirmed=str(len(confirm_offers)) if confirm_offers else '0')
    lexicon_part['buttons']['buyer_cached_offers'] = lexicon_part['buttons']['buyer_cached_offers'].format(
        non_confirmed=str(len(non_confirm_offers)) if non_confirm_offers else '0')
    lexicon_part['buttons']['buyers_recommended_offers'] = lexicon_part['buttons']['buyers_recommended_offers'].format(
        new=str(len(recommendated_offers)) if recommendated_offers else '0')
    ic(lexicon_part)
    return lexicon_part
async def buyer_offers_callback_handler(callback: CallbackQuery, state: FSMContext, delete_mode=False):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    await state.clear()
    lexicon_part = await insert_numbers_in_buttons(callback)
    await message_editor.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part, delete_mode=delete_mode)