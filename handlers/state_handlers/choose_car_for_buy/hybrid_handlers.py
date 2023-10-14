from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from database.data_requests.commodity_requests import CommodityRequester
from handlers.callback_handlers.search_auto_handler import travel_editor, redis_data


class HybridChooseStates(StatesGroup):
    select_brand = State()
    select_model = State()
    select_engine_type = State()
    config_output = State()



async def choose_brand_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(HybridChooseStates.select_brand)

    redis_key = str(callback.from_user.id) + ':cars_type'
    cars_type = await redis_data.get_data(redis_key)


    if cars_type == 'second_hand_cars':
        commodity_state = 'Б/У'
        models_range = CommodityRequester.get_where_state(state=commodity_state)
        cars_data_range = {car.id: (car.brand, car.model, car.engine_type,
                                     car.year_of_release, car.mileage, car.state, car.color, car.photo_url)
                           for car in models_range}
    elif cars_type == 'new_cars':
        commodity_state = 'новая'
        models_range = CommodityRequester.get_where_state(state=commodity_state)
        cars_data_range = {car.id: (car.brand, car.model, car.engine_type, car.complectation,
                                    car.state, car.photo_url)
                           for car in models_range}

    await state.update_data(models_range=cars_data_range)
    await state.update_data(car_class=cars_type)
    button_texts = {car_parameters[0] for car, car_parameters in cars_data_range.items()}
    await travel_editor.edit_message(request=callback, lexicon_key='choose_brand', button_texts=button_texts, callback_sign='car_brand:')

    await state.set_state(HybridChooseStates.select_model)


    async def choose_model_handler(ca)