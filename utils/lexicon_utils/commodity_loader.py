from handlers.state_handlers.seller_states_handler.load_new_car.boot_car_buttons_controller import RedisBootCommodityHelper
from utils.lexicon_utils.lexicon_uz.commodity_loader_uz import commodity_loader_lexicon_uz
from utils.safe_dict_class import SafeDict, SmartGetattr

commodity_loader_lexicon_ru = {
    'button_backward': '◂ Назад ▸',
    'cancel_button': 'Отмена',
    'confirm_buttons': '✓ Подтвердить ✓',
    'edit_button': '⚙️ Изменить ⚙️',

    'state_text': 'Выберите состояние авто:',
    'engine_text': 'Выберите тип двигателя:',
    'brand_text': 'Выберите марку авто:',
    'model_text': 'Выберите модель авто:',
    'complectation_text': 'Выберите комплектацию:',
    'year_text': 'Выберите диапазон года выпуска авто:',
    'mileage_text': 'Желаемый пробег:',
    'color_text': 'Предпочитаемый цвет:',
    'load_other_color_text': 'Введите цвет автомобиля:',
    # 'make_sure_selected_other_color_text': 'Вы выбрали: <i>X цвет</i>',
    'load_other_color_incorrect_message_text': '\n<b>Цвет должен состоять только из букв, без пробелов(либо с дефисом).</b>',
    'price_only': '''Стоимость ''',
    'input_price': 'Введите стоимость авто:',
    'price_digital': '<blockquote><b>Стоимость: <i>{price}</i></b></blockquote>',

    'edit_button_captions': {'price': 'Стоимость {price}', 'year_of_release': 'Год выпуска: {year}', 'mileage': 'Пробег: {mileage} км.'},
    'input_price_text': 'Введите стоимость:',
    'input_photo_text': 'Пришлите фото автомобиля\n(значок скрепки в левом углу чата)\n\n(!от 5 до 8 экземпляров!)\n\nНе отменяйте сжатие при отправке\nфотографии в телеграм.',
    'edit_photo_caption': 'Фото',
    'config_for_seller': '<b>Ваши конфигурации авто:</b>',
    'can_rewrite_config': 'Возможна перепись полей по нажатию на соответсвующую кнопку',

    'config_for_admins': '<b>Заявка ID:</b><i>{request_id}</i>\n',

    'seller_notification_text': 'Заявка №{request_number} создана!'
}

commodity_loader_lexicon = SafeDict({'ru': commodity_loader_lexicon_ru,
                                     'uz': commodity_loader_lexicon_uz})

class BaseBootButtons(SmartGetattr):

    def __init__(self):
        super().__init__()

        self.base_last_buttons = {'boot_car_backward': commodity_loader_lexicon['button_backward'],
                            'cancel_boot_new_commodity': commodity_loader_lexicon['cancel_button']}
        self.width = 2
        self.message_text = ''
        self.dynamic_buttons = 2

    async def part(self):
        return {'message_text': self.message_text, 'buttons': {**self.base_last_buttons, 'width': self.width}}



class LexiconCommodityLoader(SmartGetattr):
    class load_commodity_state(BaseBootButtons):
        def __init__(self):
            super().__init__()
            self.message_text = f'''<b>{commodity_loader_lexicon['state_text']}</b>'''
            self.buttons_callback_data = 'load_state_'
            self.width = 2
            self.dynamic_buttons = 1
            self.last_buttons = {'cancel_boot_new_commodity': commodity_loader_lexicon['button_backward']}

    class load_commodity_engine_type(BaseBootButtons, RedisBootCommodityHelper):
        def __init__(self):
            super().__init__()
            self.message_text = f'''<b>{commodity_loader_lexicon['engine_text']}</b>'''
            self.buttons_callback_data = 'load_engine_'
            self.width = 2
            self.last_buttons = self.base_last_buttons

    class load_commodity_brand(BaseBootButtons, RedisBootCommodityHelper):
        def __init__(self):
            super().__init__()
            self.message_text = f'''<b>{commodity_loader_lexicon['brand_text']}</b>'''
            self.buttons_callback_data = 'load_brand_'
            self.width = 2
            self.last_buttons = self.base_last_buttons

    class load_commodity_model(BaseBootButtons, RedisBootCommodityHelper):
        def __init__(self):
            super().__init__()
            self.message_text = f'''<b>{commodity_loader_lexicon['model_text']}</b>'''
            self.buttons_callback_data = 'load_model_'
            self.width = 2
            self.last_buttons = self.base_last_buttons

    # load_commodity_model = {, 'buttons': {, , 'width': 2}}
    class load_commodity_complectation(BaseBootButtons, RedisBootCommodityHelper):
        def __init__(self):
            super().__init__()
            self.message_text = f'''<b>{commodity_loader_lexicon['complectation_text']}</b>'''
            self.buttons_callback_data = 'load_complectation_'
            self.width = 1
            self.last_buttons = self.base_last_buttons

    class load_commodity_year_of_realise(BaseBootButtons, RedisBootCommodityHelper):
        def __init__(self):
            super().__init__()
            self.message_text = f'''<b>{commodity_loader_lexicon['year_text']}</b>'''
            self.buttons_callback_data = 'load_year_'
            self.width = 2
            self.last_buttons = self.base_last_buttons
    class load_commodity_mileage(BaseBootButtons, RedisBootCommodityHelper):
        def __init__(self):
            super().__init__()
            self.message_text = f'''<b>{commodity_loader_lexicon['mileage_text']}</b>'''
            self.buttons_callback_data = 'load_mileage_'
            self.dynamic_buttons = 3
            self.width = 2
            self.last_buttons = self.base_last_buttons
    class load_commodity_color(BaseBootButtons, RedisBootCommodityHelper):
        def __init__(self):
            super().__init__()
            self.message_text = f'''<b>{commodity_loader_lexicon['color_text']}</b>'''
            self.buttons_callback_data = 'load_color_'
            self.width = 2
            self.dynamic_buttons = 2
            self.last_buttons = self.base_last_buttons

    class load_commodity_price(BaseBootButtons, RedisBootCommodityHelper):
        def __init__(self):
            super().__init__()
            self.message_text = f'''<b>{commodity_loader_lexicon['input_price_text']}</b>'''
            self.width = 1
            self.last_buttons = self.base_last_buttons

    class load_commodity_photo(BaseBootButtons, RedisBootCommodityHelper):
        def __init__(self):
            super().__init__()
            self.message_text = commodity_loader_lexicon['input_photo_text']
            self.width = 1
            self.last_buttons = self.base_last_buttons

    def __init__(self):
        super().__init__()

        # load_other_color = {'message_text': commodity_loader_lexicon'Введите цвет автомобиля:', 'buttons': {'rewrite_boot_color': commodity_loader_lexicon'◂ Назад ▸', 'cancel_boot_new_commodity': commodity_loader_lexicon'🚫 Отмена 🚫', 'width': 1}}
        # make_sure_selected_other_color = {'message_text': 'Вы выбрали: <i>X цвет</i>', 'buttons': {'make_sure_other_color': '✓ Подтвердить ✓', 'rewrite_other_boot_color': '⚙️ Изменить ⚙️', 'width': 1}}
        self.load_other_color_incorrect_message_text = commodity_loader_lexicon['load_other_color_incorrect_message_text']
        self.price_only = commodity_loader_lexicon['price_only']
        self.input_price = commodity_loader_lexicon['input_price']
        self.price_digital = commodity_loader_lexicon['price_digital']
        self.edit_button_captions = commodity_loader_lexicon['edit_button_captions']
        self.load_commodity_state = self.load_commodity_state
        self.load_commodity_engine_type = self.load_commodity_engine_type
        self.load_commodity_brand = self.load_commodity_brand
        self.load_commodity_model = self.load_commodity_model
        self.load_commodity_complectation = self.load_commodity_complectation
        self.load_commodity_year_of_realise = self.load_commodity_year_of_realise
        self.load_commodity_mileage = self.load_commodity_mileage
        self.load_commodity_color = self.load_commodity_color
        self.load_commodity_price = self.load_commodity_price
        self.load_commodity_photo = self.load_commodity_photo

        self.edit_photo_caption = commodity_loader_lexicon['edit_photo_caption']


        self.config_for_seller = commodity_loader_lexicon['config_for_seller']
        self.can_rewrite_config = commodity_loader_lexicon['can_rewrite_config']
        self.config_for_seller_button_callbacks = ('rewrite_boot_state', 'rewrite_boot_engine', 'rewrite_boot_brand', 'rewrite_boot_model', 'rewrite_boot_complectation', 'rewrite_boot_year', 'rewrite_boot_mileage', 'rewrite_boot_color', 'rewrite_boot_price', 'rewrite_boot_photo')

        self.config_for_admins = commodity_loader_lexicon['config_for_admins']

        self.seller_notification = {'message_text': commodity_loader_lexicon['seller_notification_text']}

BaseBootButtons = BaseBootButtons()
LexiconCommodityLoader = LexiconCommodityLoader()
