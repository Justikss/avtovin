from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.data_requests.banned_person_requests import BannedRequester
from utils.oop_handlers_engineering.update_handlers.base_objects.base_admin_administrate_object import \
    BaseAdminCommandHandler


class UnbanPersonAdminHandler(BaseAdminCommandHandler):
    async def process_message(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        #Тестировать: отсутсвие пользователей для взятия
        #unban s @username
        #unban b @username
        seller, user = False, False

        command_body = request.text[request.text.index('/unban ')+1:]
        ic(command_body)
        if ic(command_body.startswith('s')):
            seller = True
        elif ic(command_body.startswith('b')):
            user=True
        else:
            user = True
            seller = True
        user_id = await self.get_user_id(request, banned=True) #настроить поиск по баненым

        query = await BannedRequester.remove_ban(user_id, seller, user)
        # if query:
        #     await
        await self.query_state_callback(request, query)

