from typing import List

from database.data_requests.admin_requests import AdminManager
from utils.get_username import get_username

from utils.lexicon_utils.Lexicon import ADMIN_LEXICON
from utils.oop_handlers_engineering.generate_output_objects.specific_objects.base_admin_pagination import \
    AdminPaginationInit
from utils.oop_handlers_engineering.generate_output_objects.specific_objects.base_inline_pagination import \
    InlinePaginationInit
from utils.oop_handlers_engineering.generate_output_objects.specific_objects.base_travel_editor import \
    TravelMessageEditorInit
from utils.oop_handlers_engineering.update_handlers.base_objects.base_message_handler_init import BaseMessageHandler

class BaseAdminCommandHandler(BaseMessageHandler):
    def __init__(self,
                 output_methods: List[AdminPaginationInit | InlinePaginationInit | TravelMessageEditorInit] = None,
                 filters=None):

        self.admin_manager = AdminManager
        self.admin_lexicon = ADMIN_LEXICON
        super().__init__(output_methods, filters)

    async def get_user_id(self, request):
        user_info = request.text.split()[-1]

        if '@' in user_info:
            # user_info = await self.get_user_id_by_username(request, user_info)

            from database.data_requests.person_requests import PersonRequester
            telegram_ids = await PersonRequester.get_all_unique_user_ids()
            ic(telegram_ids)
            for telegram_id in telegram_ids:
                username = await get_username(request.bot, telegram_id)
                ic(username)
                if f'@{username}' == user_info:
                    user_info = telegram_id
                    break
        ic(user_info)
        return user_info


    async def query_state_callback(self, request, query):
        if query:
            lexicon_code = 'successfully'
        else:
            lexicon_code = 'unsuccessfully'
        await self.delete_message(request, request.message_id)
        message = self.admin_lexicon[lexicon_code]
        await self.send_alert_answer(request, message)
