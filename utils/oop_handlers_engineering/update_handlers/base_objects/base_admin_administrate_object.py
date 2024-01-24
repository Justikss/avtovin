from typing import List

from database.data_requests.admin_requests import AdminManager
from database.data_requests.banned_person_requests import BannedRequester
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

    async def get_user_id(self, request, banned=False):
        user_name = request.text.split()[-1]
        telegram_id = None
        ic(user_name)
        ic(banned)
        if user_name.startswith('@'):
            if not banned:
                from database.data_requests.person_requests import PersonRequester

                telegram_ids = await PersonRequester.get_all_unique_user_ids()
                telegram_id = await self.get_telegram_id_from_massive(request, telegram_ids, user_name)
                ic(telegram_ids)

            elif banned or not user_name:
                telegram_ids = await BannedRequester.retrieve_all_banned_ids()
                ic(telegram_ids)
                telegram_id = await self.get_telegram_id_from_massive(request, telegram_ids, user_name)

        ic(telegram_id)
        if not str(telegram_id).isdigit():
            return False
        return telegram_id

    async def get_telegram_id_from_massive(self, request, telegram_ids, user_info):
        tg_id = None
        for telegram_id in telegram_ids:
            username = await get_username(request.bot, telegram_id)
            ic(username)
            ic(f'@{username}' == user_info)
            if f'@{username}' == user_info:
                tg_id = telegram_id
                break

        return tg_id

    async def query_state_callback(self, request, query):
        if query:
            lexicon_code = 'successfully'
        else:
            lexicon_code = 'unsuccessfully'
        await self.delete_message(request, request.message_id)
        message = self.admin_lexicon[lexicon_code]
        await self.send_alert_answer(request, message)
