import asyncio
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

    async def username_len_filter(self, username):
        if len(username) > 35:
            return False
        return True

    async def get_user_id(self, request, banned=False):
        user_name = request.text.split()[-1]
        telegram_id = None
        ic(user_name)
        ic(banned)
        if user_name.startswith('@'):
            if not await self.username_len_filter(user_name):
                return False
            if not banned:
                from database.data_requests.person_requests import PersonRequester

                telegram_ids = await PersonRequester.get_all_unique_user_ids()
                telegram_id = await self.get_telegram_id_from_massive(request, telegram_ids, user_name)
                ic(telegram_ids)

            elif banned or not user_name:
                telegram_ids = await BannedRequester.retrieve_all_banned_ids()
                ic(telegram_ids)
                telegram_id = await self.get_telegram_id_from_massive(request, telegram_ids, user_name)
                if not telegram_id and banned:
                    return await self.get_user_id(request)

        ic(telegram_id)
        if not str(telegram_id).isdigit():
            return False
        return telegram_id

    async def get_telegram_id_from_massive(self, request, telegram_ids, user_info):
        tasks = [get_username(request.bot, telegram_id) for telegram_id in telegram_ids]
        usernames = await asyncio.gather(*tasks)

        for telegram_id, username in zip(telegram_ids, usernames):
            if f'@{username}' == user_info:
                return telegram_id
        return None

    async def query_state_callback(self, request, query, state, action_on=None):
        lexicon_code = None

        if query:
            lexicon_code = 'successfully'
        else:
            if action_on:
                match action_on:
                    case 'admin':
                        lexicon_code = 'inputted_user_not_is_admin'
                    case 'unban':
                         lexicon_code = 'user_has_not_been_blocked'
                    case 'set_admin':
                         lexicon_code = 'inputted_admin_is_exists'
            if not lexicon_code:
                lexicon_code = 'unsuccessfully'
        await self.delete_message(request, request.message_id)
        message = self.admin_lexicon[lexicon_code]
        await self.send_alert_answer(request, message)
        from handlers.callback_handlers.hybrid_part.return_main_menu import return_main_menu_callback_handler
        await return_main_menu_callback_handler(request, state)

    async def user_id_not_found_handler(self, request, user_id):
        if not user_id:
            await self.send_alert_answer(request, self.admin_lexicon['user_id_not_found'])
            return True