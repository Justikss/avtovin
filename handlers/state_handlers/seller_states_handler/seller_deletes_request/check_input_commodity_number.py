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
    memory_storage = await state.get_data()


    input_number = message.text
    if input_number.isdigit():
        print('isdigit')
        removable_commodity = CommodityRequester.get_where_id(car_id=input_number)
        print('removable_commodity', removable_commodity)
        if removable_commodity:
            last_user_message_id = memory_storage.get('last_user_message_delete_state')
            if last_user_message_id:
                try:
                    await message.chat.delete_message(message_id=last_user_message_id)
                    await state.update_data(last_user_message_delete_state=None)
                except:
                    pass
            try:
                await message.delete()
            except:
                pass
            await state.set_state(DeleteRequestStates.check_input_on_valid)
            await state.update_data(car_id=input_number)
            output_string = await output_message_constructor([removable_commodity])
            output_string = output_string[0]
            lexicon_part = {'message_text': output_string['text']}
            media_group = output_string['album']
            #
            #
            # if memory_storage.get('incorrect_flag_deletes'):
            #     delete_mode = True
            # else:
            #     delete_mode = False
            #
            return (
                await message_editor.travel_editor.edit_message(request=message, lexicon_key='',
                                                                    lexicon_part=lexicon_part, media_group=media_group,
                                                                    need_media_caption=True),

                await message_editor.travel_editor.edit_message(request=message, lexicon_key='confirm_delete_request',
                                                                save_media_group=True, delete_mode=True)
                    )


    lexicon_part = {'message_text': LEXICON['incorrect_input_removed_car_id'],
                    'buttons': LEXICON['seller_start_delete_request']['buttons']}

    # await message_editor.redis_data.get_data(key=str(message.from_user.id))

    last_user_message_id = memory_storage.get('last_user_message_delete_state')
    if last_user_message_id:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=last_user_message_id)
        except:
            pass

    await message_editor.travel_editor.edit_message(request=message, lexicon_key='',
                                                    lexicon_part=lexicon_part, reply_mode=True, delete_mode=True)

    await state.update_data(last_user_message_delete_state=message.message_id)
    # await state.update_data(incorrect_flag_deletes=True)

    # await message.bot.edit_message_text(chat_id=message.chat.id, message_id=last_message_id, text=LEXICON['incorrect_input_removed_car_id'])
