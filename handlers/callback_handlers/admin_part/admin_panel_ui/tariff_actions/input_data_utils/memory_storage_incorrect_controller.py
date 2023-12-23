

async def incorrect(state, message_id):
    await state.update_data(admin_incorrect_flag=True)
    await state.update_data(last_admin_answer=message_id)