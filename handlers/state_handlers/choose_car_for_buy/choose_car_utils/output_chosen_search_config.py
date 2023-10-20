import importlib

from aiogram.types import CallbackQuery
from utils.Lexicon import LEXICON

async def string_for_output(callback: CallbackQuery, engine, model,
                            brand, complectation=None, average_cost=None,
                            color=None, year=None, mileage=None):
    redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт


    redis_key = str(callback.from_user.id) + ':cars_type'
    cars_state = await redis_module.redis_data.get_data(redis_key)

    lexicon_part = LEXICON.get('chosen_configuration')
    message_text = lexicon_part.get('message_text')


    if cars_state == 'second_hand_cars':
        result_string = f'''
            {message_text['your_configs']}\n{message_text['engine_type']} {engine}\n{message_text['color']} {color}\n{message_text['model']} {model}\n{message_text['brand']} {brand}\n{message_text['year']} {year}\n{message_text['mileage']} {mileage}'''

    elif cars_state == 'new_cars':
        result_string = f'''
            {message_text['your_configs']}\n{message_text['engine_type']} {engine}\n{message_text['model']} {model}\n{message_text['brand']} {brand}\n{message_text['complectation']} {complectation}\n{message_text['cost']} {average_cost}'''


    return result_string