from aiogram.fsm.context import FSMContext


async def incorrect(state, message_id):
    await state.update_data(admin_incorrect_flag=True)
    await state.update_data(last_admin_answer=message_id)

async def get_incorrect_flag(state: FSMContext, incorrect_flag_name='admin_incorrect_flag'):
    memory_storage = await state.get_data()
    incorrect_flag = memory_storage.get(incorrect_flag_name)
    if incorrect_flag:
        await state.update_data(admin_incorrect_flag=True)
    return incorrect_flag