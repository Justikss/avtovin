from aiogram import Bot
from aiogram.types import CallbackQuery

from utils.user_notification import send_notification


async def send_notification_about_lose_tariff(seller_id, callback: CallbackQuery=None, bot: Bot=None, last_notif=False):
    ic(seller_id)
    if not isinstance(seller_id, int):
        seller_id = seller_id.telegram_id
    if last_notif:
        user_status = 'seller_lose_self_tariff'
    else:
        user_status = 'seller_without_tariff'
    await send_notification(callback, user_status=user_status, chat_id=seller_id, bot=bot)
