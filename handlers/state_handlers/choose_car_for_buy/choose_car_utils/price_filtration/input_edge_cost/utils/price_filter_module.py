from aiogram.fsm.context import FSMContext


class PriceFilterForBuyerModule:
    async def __call__(self, currency, inputted_cost, state: FSMContext) -> bool | str:
        current_state = str(await state.get_state())
        ic(inputted_cost)
        if not current_state.startswith('BuyerSearchCostFilterStates'):
            return False
        elif not str(inputted_cost).isdigit():
            return False

        from handlers.state_handlers.choose_car_for_buy.choose_car_utils.price_filtration.input_edge_cost.start import \
            StartInputCarPriceFilterStartInputHandler
        default_cost_diapason, _ = await StartInputCarPriceFilterStartInputHandler().get_diapason_edges(
            await state.get_data()
        )
        inputted_usd_price = await self.inputted_value_handler(currency, inputted_cost)
        ic(inputted_usd_price)
        if inputted_usd_price in range(default_cost_diapason['from'], default_cost_diapason['before']+1):
            prices_in_diapason_is_exists = await self.prices_in_diapason_is_exists(
                inputted_usd_price, default_cost_diapason, state
            )
            if str(prices_in_diapason_is_exists).isdigit():
                return f'nearest_price:{prices_in_diapason_is_exists}'
            else:
                return False
        else:
            incorrect_flag = '(range)'
            return incorrect_flag

    async def prices_in_diapason_is_exists(self, inputted_cost, default_cost_diapason, state: FSMContext):
        async def seek_near_number_out_of_range(direction):
            closest_number = None
            min_distance = float('inf')

            # Итерация с минимальным использованием памяти
            for number in all_advert_prices:
                if direction == 'lower' and number < lower_bound:
                    distance = abs(number - lower_bound)
                    if distance < min_distance:
                        min_distance = distance
                        closest_number = number
                elif direction == 'upper' and number > upper_bound:
                    distance = abs(number - upper_bound)
                    if distance < min_distance:
                        min_distance = distance
                        closest_number = number

            return closest_number

        memory_storage = await state.get_data()

        diapason_side = memory_storage.get('selected_side_to_input')
        all_advert_prices = memory_storage.get('all_usd_prices')

        default_cost_diapason[diapason_side] = inputted_cost
        lower_bound = default_cost_diapason['from']
        upper_bound = default_cost_diapason['before']

        # Определение направления поиска на основе diapason_side
        direction = 'lower' if diapason_side == 'from' else 'upper'

        # Фильтрация с использованием генератора
        filtered_exist_costs = (number for number in all_advert_prices if lower_bound <= number <= upper_bound)
        inputted_range_is_valid = any(filtered_exist_costs)

        if not inputted_range_is_valid:
            return await seek_near_number_out_of_range(direction)
        else:
            return inputted_range_is_valid

    async def inputted_value_handler(self, currency, inputted_cost):
        from utils.get_currency_sum_usd import convertator

        if currency == 'usd':
            usd_cost = inputted_cost
        elif currency == 'sum':
            usd_cost = await convertator(currency, inputted_cost)
        else:
            return None

        return usd_cost


price_adverts_filter_module = PriceFilterForBuyerModule()