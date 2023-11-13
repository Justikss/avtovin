import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from handlers.callback_handlers.sell_part.commodity_requests.output_sellers_requests_by_car_brand import \
    output_message_constructor
from states.seller_deletes_request_states import DeleteRequestStates
from database.data_requests.commodity_requests import CommodityRequester

async def check_input_number_handler(message: Message, state: FSMContext):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    await state.set_state(DeleteRequestStates.check_input_on_valid)

    input_number = message.text
    if input_number.isdigit():
        removable_commodity = CommodityRequester.get_where_id(car_id=input_number)
        if removable_commodity:
            removable_commodity = removable_commodity[0]
            output_string = await output_message_constructor([removable_commodity])
            lexicon_part = {'message_text': output_string['text']}
            media_group = output_string['album']
            await message_editor.travel_editor.edit_message(request=message, lexicon_key='', lexicon_part=lexicon_part, media_group=media_group, need_media_caption=True)


            await message_editor.travel_editor.edit_message(request=message, lexicon_key='', lexicon_part=lexicon_part, media_group=media_group, need_media_caption=True)
