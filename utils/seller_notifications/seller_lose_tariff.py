from aiogram import Bot
from aiogram.types import CallbackQuery

from utils.user_notification import send_notification


async def send_notification_about_lose_tariff(seller_id, callback: CallbackQuery=None, bot: Bot=None):
    ic(seller_id)
    if not isinstance(seller_id, int):
        seller_id = seller_id.telegram_id
    await send_notification(callback, user_status='seller_without_tariff', chat_id=seller_id, bot=bot)
