from aiogram.types import Message

from database.data_requests.car_advert_requests import AdvertRequester
from database.data_requests.dying_tariff import DyingTariffRequester
from database.data_requests.tariff_to_seller_requests import TariffToSellerBinder
from handlers.callback_handlers.sell_part.seller_main_menu import get_tariff


async def save_tariff_handler(message: Message):
    user_id = message.from_user.id
    await DyingTariffRequester.remove_old_tariff_to_update(user_id)
    await TariffToSellerBinder.remove_bind(user_id)

    await AdvertRequester.set_sleep_status(sleep_status=False, seller_id=user_id)

    await get_tariff(message, normal_status=True)

    await message.answer('Тариф установлен!')
