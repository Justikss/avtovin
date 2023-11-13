import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from handlers.callback_handlers.sell_part.commodity_requests.output_sellers_requests_by_car_brand import \
    output_message_constructor
from states.seller_deletes_request_states import DeleteRequestStates
from database.data_requests.commodity_requests import CommodityRequester
from utils.Lexicon import LEXICON


async def check_input_id_handler(message: Message, state: FSMContext):
    '''Метод проверки введённого id заказа для удаления - на валидность'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    await message.delete()

    input_number = message.text
    if input_number.isdigit():
        print('isdigit')
        removable_commodity = CommodityRequester.get_where_id(car_id=input_number)
        if removable_commodity:
            await state.set_state(DeleteRequestStates.check_input_on_valid)
            await state.update_data(car_id=input_number)
            removable_commodity = removable_commodity[0]
            output_string = await output_message_constructor([removable_commodity])
            lexicon_part = {'message_text': output_string['text']}
            media_group = output_string['album']

            return (
                await message_editor.travel_editor.edit_message(request=message, lexicon_key='',
                                                                    lexicon_part=lexicon_part, media_group=media_group,
                                                                    need_media_caption=True),

                await message_editor.travel_editor.edit_message(request=message, lexicon_key='confirm_delete_request',
                                                                save_media_group=True)
                    )

    '''СДЕЛАТЬ ВЫСЫЛКУ ОПОВЕЩЕНИЯ INCORRECT, А НЕ РЕДАКТИРОВАНИЕ'''
    last_message_id = await message_editor.redis_data.get_data(key=f'{str(message.from_user.id)}:last_message')

    await message.bot.edit_message_text(chat_id=message.chat.id, message_id=last_message_id, text=LEXICON['incorrect_input_removed_car_id'])
