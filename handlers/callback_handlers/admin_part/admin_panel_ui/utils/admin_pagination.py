import importlib
from typing import Optional

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.data_requests.car_advert_requests import AdvertRequester
from database.data_requests.mailing_requests import get_mailing_by_id
from database.tables.mailing import Mailing
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.car_catalog_review.output_choose.utils.send_advert_review import \
    send_advert_review
from handlers.callback_handlers.admin_part.admin_panel_ui.advertisement_actions.mailing.mailing_storage.utils.\
    send_mailing_review import send_mailing_review
from handlers.utils.pagination_heart import Pagination

redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
media_group_delete_module = importlib.import_module('handlers.callback_handlers.sell_part.seller_main_menu')

class AdminPaginationOutput(Pagination):
    @staticmethod
    async def get_pagination_class_object(request: CallbackQuery | Message):
        user_id = request.from_user.id

        admin_pagination = await redis_module.redis_data.get_data(
            key=f'{user_id}:admin_pagination', use_json=True)

        if admin_pagination and admin_pagination != 'null':
            admin_pagination_object = AdminPaginationOutput(**admin_pagination)


            return admin_pagination_object

    @staticmethod
    async def delete_current_page(request: CallbackQuery | Message, state: FSMContext):
        user_id = request.from_user.id

        admin_pagination_object = await AdminPaginationOutput.get_pagination_class_object(request)
        admin_pagination_object.data.pop(admin_pagination_object.current_page-1)
        if admin_pagination_object.total_pages == 1:
            return False
        admin_pagination_object.total_pages -= 1

        dictated_pagination_data = await admin_pagination_object.to_dict()
        await redis_module.redis_data.set_data(key=f'{user_id}:admin_pagination',
                                               value=dictated_pagination_data)

        await admin_pagination_object.output_page(request, state, None)

        return True

    async def get_output_data(self, request: CallbackQuery | Message, state: FSMContext, output_data):
        current_state = str(await state.get_state())
        output_structured_data = []
        for data_part in output_data:
            if current_state.startswith('MailingReviewStates'):
                current_model: Optional[Mailing] = await get_mailing_by_id(data_part)
                if current_model:
                    current_model = current_model.__dict__
                    output_structured_data.append(current_model)
            else:
                advert_model = await AdvertRequester.get_where_id(data_part)
                if advert_model:
                    output_structured_data.append(advert_model)

        return output_structured_data

    @staticmethod
    async def set_pagination_data(request: CallbackQuery | Message, state: FSMContext, pagination_data):
        user_id = request.from_user.id

        admin_pagination_object = AdminPaginationOutput(data=pagination_data,
                                                    page_size=1)

        dictated_pagination_data = await admin_pagination_object.to_dict()

        await redis_module.redis_data.set_data(key=f'{user_id}:admin_pagination',
                                                 value=dictated_pagination_data)

        await AdminPaginationOutput.output_page(request, state, '+')

    @staticmethod
    async def output_page(request: CallbackQuery | Message, state: FSMContext, operation):
        user_id = request.from_user.id
        current_state = str(await state.get_state())
        admin_pagination_object = await AdminPaginationOutput.get_pagination_class_object(request)
        if admin_pagination_object:
            page_data = await admin_pagination_object.get_page(operation)
            data_to_output = await admin_pagination_object.get_output_data(request, state, page_data)

            dictated_pagination_data = await admin_pagination_object.to_dict()

            await redis_module.redis_data.set_data(key=f'{user_id}:admin_pagination',
                                                   value=dictated_pagination_data)
            ic(data_to_output)
            if data_to_output:
                await media_group_delete_module.delete_media_groups(request=request)

                if current_state.startswith('MailingReviewStates'):
                    await send_mailing_review(request, admin_pagination_object, data_to_output, message_editor)

                elif current_state.startswith(('AdminCarCatalogReviewStates', 'AdminCarCatalogSearchByIdStates')):
                    ic()
                    await send_advert_review(request, state, admin_pagination_object, data_to_output, message_editor)
            else:
                return False


    @staticmethod
    async def admin_pagination_vector(callback: CallbackQuery, state: FSMContext):
        operation = callback.data.split(':')[-1]
        ic(operation)
        await AdminPaginationOutput.output_page(callback, state, operation)

