import importlib

from aiogram.types import Message

from handlers.callback_handlers.sell_part.seller_main_menu import get_tariff

car_advert_requests_module = importlib.import_module('database.data_requests.car_advert_requests')



async def save_tariff_handler(message: Message):
    tariff_to_seller_binder_module = importlib.import_module('database.data_requests.tariff_to_seller_requests')
    dying_tariffs_requester_module = importlib.import_module('database.data_requests.dying_tariff')

    user_id = message.from_user.id
    await dying_tariffs_requester_module.DyingTariffRequester.remove_old_tariff_to_update(user_id)
    await tariff_to_seller_binder_module.TariffToSellerBinder.remove_bind(user_id)

    # await car_advert_requests_module.AdvertRequester.set_sleep_status(sleep_status=False, seller_id=user_id)

    await get_tariff(message, normal_status=True)

    await message.answer('Тариф установлен!')
