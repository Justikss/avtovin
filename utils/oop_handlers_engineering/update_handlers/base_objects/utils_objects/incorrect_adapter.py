from aiogram.fsm.context import FSMContext

from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.input_data_utils.memory_storage_incorrect_controller import \
    get_incorrect_flag
from handlers.utils.delete_message import delete_message


class IncorrectAdapter:
    async def get_incorrect_flag(self, state: FSMContext):
        return ic(await get_incorrect_flag(state))

    async def get_last_incorrect_message_id(self, state: FSMContext):
        memory_storage = await state.get_data()
        last_admin_answer = ic(memory_storage.get('last_admin_answer'))
        return last_admin_answer

    async def get_lexicon_part_in_view_of_incorrect(self, lexicon_key, lexicon_object, incorrect) -> dict:
        ic(incorrect)
        ic()
        lexicon_part = lexicon_object[lexicon_key]
        ic(lexicon_part)
        if incorrect:
            if incorrect is True:
                incorrect_message_text = lexicon_object[f"{lexicon_key}(incorrect)"]
            else:
                incorrect_message_text = lexicon_object[f"{lexicon_key}{incorrect}"]

            lexicon_part['message_text'] = incorrect_message_text
        ic(lexicon_part)
        return lexicon_part

    async def try_delete_incorrect_message(self, request, state):
        if await self.get_incorrect_flag(state):
            await delete_message(request, await self.get_last_incorrect_message_id(state))

