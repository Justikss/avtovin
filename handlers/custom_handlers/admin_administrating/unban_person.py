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

        seller, user = await self.identify_entity(request)

        user_id = await self.get_user_id(request, banned=True)

        if await self.user_id_not_found_handler(request, user_id):
            return
        else:
            query = await BannedRequester.remove_ban(user_id, seller, user)


            if query:
                await self.logging_action(request, subject=request.text, action='unban_person')

            await self.query_state_callback(request, query, state, action_on='unban')


    async def identify_entity(self, request):
        ic(request.text)
        command_body = request.text[7:]
        ic(command_body)

        seller, user = False, False

        if ic(command_body.startswith('s')):
            seller = True
        elif ic(command_body.startswith('b')):
            user=True
        else:
            user = True
            seller = True

        return seller, user