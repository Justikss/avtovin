import importlib
from typing import Optional

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.data_requests.mailing_requests import get_mailing_by_id
from database.tables.mailing import Mailing
from handlers.utils.pagination_heart import Pagination
from handlers.utils.send_any_medias import send_media
from utils.lexicon_utils.Lexicon import ADVERT_LEXICON
from utils.lexicon_utils.admin_lexicon.admin_lexicon import captions

redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
media_group_delete_module = importlib.import_module('handlers.callback_handlers.sell_part.seller_main_menu')

class AdminPaginationOutput(Pagination):
    async def get_output_data(self, request: CallbackQuery | Message, state: FSMContext, output_data):
        current_state = str(await state.get_state())
        output_structured_data = []
        for data_part in output_data:
            if current_state.startswith('MailingReviewStates'):
                current_model: Optional[Mailing] = await get_mailing_by_id(data_part)
                if current_model:
                    current_model = current_model.__dict__
                    output_structured_data.append(current_model)

        return output_structured_data

    @staticmethod
    async def set_pagination_data(request: CallbackQuery | Message, state: FSMContext, pagination_data):
        user_id = request.from_user.id

        admin_pagination_object = AdminPaginationOutput(data=pagination_data,
                                                    page_size=1)

        dictated_pagination_data = await admin_pagination_object.to_dict()

        await redis_module.redis_data.set_data(key=f'{user_id}:admin_pagination',
                                                 value=dictated_pagination_data)

    @staticmethod
    async def output_page(request: CallbackQuery | Message, state: FSMContext, operation):
        user_id = request.from_user.id
        current_state = str(await state.get_state())

        admin_pagination = await redis_module.redis_data.get_data(
            key=f'{user_id}:admin_pagination', use_json=True)

        if admin_pagination and admin_pagination != 'null':
            admin_pagination_object = AdminPaginationOutput(**admin_pagination)

            page_data = await admin_pagination_object.get_page(operation)

            dictated_pagination_data = await admin_pagination_object.to_dict()

            await redis_module.redis_data.set_data(key=f'{user_id}:admin_pagination',
                                                   value=dictated_pagination_data)

            data_to_output = await admin_pagination_object.get_output_data(request, state, page_data)

            if data_to_output:
                await media_group_delete_module.delete_media_groups(request=request)

                if current_state.startswith('MailingReviewStates'):
                    ic(data_to_output)
                    output_data = data_to_output[0]['__data__']
                    ic(output_data)
                    lexicon_part = ADVERT_LEXICON['send_mailing_review']
                    lexicon_part['message_text'] = lexicon_part['message_text'].format(
                        mailing_recipients=captions[output_data['recipients_type']],
                        mailing_text=output_data['text'],
                        mailing_date=str(output_data['scheduled_time']).split()[0],
                        mailing_time=str(output_data['scheduled_time']).split()[-1]
                    )
                    lexicon_part['buttons']['page_counter'] = lexicon_part['buttons']['page_counter'].format(
                    start=admin_pagination_object.current_page,
                    end=admin_pagination_object.total_pages
                    )
                    await send_media(request, media_info_list=output_data['media'])

                    await message_editor.travel_editor.edit_message(request=request, lexicon_key='',
                                                                    lexicon_part=lexicon_part, save_media_group=True,
                                                                    dynamic_buttons=2, delete_mode=True)


    @staticmethod
    async def admin_pagination_vector(callback: CallbackQuery, state: FSMContext):
        operation = callback.data.split(':')[-1]
        await AdminPaginationOutput.output_page(callback, state, operation)