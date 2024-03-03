import importlib
from typing import Union

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message


class RedisBootCommodityHelper:
    async def initializate(self, request: Union[CallbackQuery, Message], state: FSMContext):
        if self.__class__ is not RedisBootCommodityHelper:
            message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

            there_data_update = await message_editor.redis_data.get_data(
                key=str(request.from_user.id) + ':can_edit_seller_boot_commodity')
            ic(there_data_update)
            ic(self.last_buttons, self.dynamic_buttons)
            if there_data_update and isinstance(self.last_buttons, dict) and isinstance(self.dynamic_buttons, int):
                ic()
                # Предполагаем, что вы хотите оставить последнюю пару в словаре
                # self.last_buttons = {key: value for key, value in self.last_buttons.items() if key != 'cancel_boot_new_commodity'}
                ic(self.last_buttons.get('cancel_boot_new_commodity'))
                if self.last_buttons.get('cancel_boot_new_commodity'):
                    await state.update_data(last_buttons={'cancel_boot_new_commodity': self.last_buttons['cancel_boot_new_commodity']})
                    await state.update_data(dynamic_buttons=self.dynamic_buttons - 1)
                    self.last_buttons = {'cancel_boot_new_commodity': self.last_buttons['cancel_boot_new_commodity']}
                    if self.dynamic_buttons != 1:
                        self.dynamic_buttons -= 1
                    ic(self.last_buttons, self.dynamic_buttons)

            ic(state)
            if state:
                memory_storage = await state.get_data()
                current_state = str(await state.get_state())
                ic(current_state)
                state_cache = memory_storage.get('boot_car_states_cache')
                if not state_cache:
                    state_cache = []
                if current_state not in state_cache:
                    state_cache.append(current_state)
                ic(state_cache)
                await state.update_data(boot_car_states_cache=state_cache)
