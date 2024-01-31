import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils.get_username import get_username
from utils.oop_handlers_engineering.update_handlers.base_objects.base_admin_administrate_object import \
    BaseAdminCommandHandler


class AdminListHandler(BaseAdminCommandHandler):
    async def process_message(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

        admins = await self.admin_manager.retrieve_all_admins()

        table_text = self.admin_lexicon['admin_list_header']
        body_data = dict()
        if admins:
            for admin in admins:
                # '✖️✅✔️'
                username = f'@{await get_username(request.bot, admin.telegram_id)}'

                red_status = '✖️' if not admin.admin_rang else '✅'
                body_data.update({username: red_status})
            max_username_len = max(len("@Justion"), len("@AikenOZ"))

            ic(max_username_len)
            for username, red_status in body_data.items():
                username = username.ljust(max_username_len, ' ')
                part = f'\n{username} | {red_status}'
                table_text += part

        table_text = f'```{table_text}```'
        lexicon_part = {'message_text': table_text,
                        'buttons': {'return_main_menu': self.admin_lexicon['close_admin_list'],
                                'width': 1}}

        await self.delete_message(request, request.message_id)
        await self.delete_message(request, from_redis=True)


        message = await request.answer(text=table_text,  parse_mode='Markdown', reply_markup=await message_editor.InlineCreator.create_markup(lexicon_part))


        await self.redis_module.redis_data.set_data(key=f'{request.from_user.id}:last_message',
                                                    value=message.message_id)

        await super().process_message(request, state, **kwargs)
