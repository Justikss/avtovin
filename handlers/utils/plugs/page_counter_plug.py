from aiogram.types import CallbackQuery


async def page_conter_plug(callback: CallbackQuery):
    await callback.answer()