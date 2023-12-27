from aiogram.types import CallbackQuery


async def close_mailing_messages(callback: CallbackQuery):
    head_message_id = callback.data.split(':')[-1]
    await callback.answer('В разработке')