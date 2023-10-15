from aiogram.types import CallbackQuery

from handlers.callback_handlers.main_menu import redis_data

async def string_for_output(callback: CallbackQuery, car_photo: str, middle_cost: int):
    redis_key = str(callback.from_user.id) + ':cars_type'
    cars_state = await redis_data.get_data(redis_key)


    '''Распилить строкии в лексикон'''

    if cars_state == 'second_hand_cars':
        result_string = '''     Ваши настройки:
        Тип двигателя:
        Модель:
        Марка:
        Комплектация:
        Стоимость: '''
    elif cars_state == 'new_cars':
        result_string = '''     Ваши настройки:
        Тип двигателя:
        Модель:
        Марка:
        Комплектация:
        Стоимость: '''

    return result_string