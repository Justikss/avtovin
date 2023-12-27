from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery


async def confirm_boot_mailing_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()