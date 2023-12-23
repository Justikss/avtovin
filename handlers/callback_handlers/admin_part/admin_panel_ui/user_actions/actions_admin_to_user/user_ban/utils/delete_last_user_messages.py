import importlib

from aiogram.types import CallbackQuery

from handlers.custom_filters.message_is_photo import MessageIsPhoto


async def wipe_user_chat_history(request, state, user_id, seller=False, user=False):
    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт

    if isinstance(request, CallbackQuery):
        message = request.message
    else:
        message = request

    redis_key = f'{user_id}:user_state'
    ic()
    user_state = await redis_module.redis_data.get_data(key=redis_key)
    ic(user_state, user, seller)
    if user_state:
        if user_state == 'buy' and user or user_state == 'sell' and seller:
            await redis_module.redis_data.delete_key(key=redis_key)
            await MessageIsPhoto.chat_cleaner(self=MessageIsPhoto,
                                              trash_redis_keys=(
                                              ':last_seller_message', ':last_user_message', ':last_message'),
                                              message=message, user_id=user_id)




