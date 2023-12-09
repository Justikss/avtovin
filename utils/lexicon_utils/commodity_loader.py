from handlers.state_handlers.seller_states_handler.load_new_car.boot_car_buttons_controller import RedisBootCommodityHelper


class BaseBootButtons:
    last_buttons = {'boot_car_backward': 'Назад', 'cancel_boot_new_commodity': 'Отмена'}
    width = 0
    message_text = ''
    dynamic_buttons = 2
    def __init__(self):
        self.last_buttons = self.last_buttons
        self.width = self.width
        self.dynamic_buttons = self.dynamic_buttons
        self.message_text = self.message_text

    async def part(self):
        return {'message_text': self.message_text, 'buttons': {**self.last_buttons, 'width': self.width}}



class LexiconCommodityLoader:
    class load_commodity_state(BaseBootButtons, RedisBootCommodityHelper):
        message_text = 'Состояние'
        buttons_callback_data = 'load_state_'
        width = 2
        dynamic_buttons = 1
        last_buttons = {'cancel_boot_new_commodity': 'Отмена'}

    class load_commodity_engine_type(BaseBootButtons, RedisBootCommodityHelper):
        message_text = 'Тип двигателя'
        buttons_callback_data = 'load_engine_'
        width = 2

    class load_commodity_brand(BaseBootButtons, RedisBootCommodityHelper):
        message_text = 'Марка'
        buttons_callback_data = 'load_brand_'
        width = 2

    class load_commodity_model(BaseBootButtons, RedisBootCommodityHelper):
        message_text = 'Модель'
        buttons_callback_data = 'load_model_'
        width = 2

    # load_commodity_model = {, 'buttons': {, , 'width': 2}}
    class load_commodity_complectation(BaseBootButtons, RedisBootCommodityHelper):
        message_text = 'Комплектация'
        buttons_callback_data = 'load_complectation_'
        width = 1

    class load_commodity_year_of_realise(BaseBootButtons, RedisBootCommodityHelper):
        message_text = 'Год выпуска'
        buttons_callback_data = 'load_year_'
        width = 2
    class load_commodity_mileage(BaseBootButtons, RedisBootCommodityHelper):
        message_text = 'Пробег'
        buttons_callback_data = 'load_mileage_'
        dynamic_buttons = 3
        width = 2
    class load_commodity_color(BaseBootButtons, RedisBootCommodityHelper):
        message_text = 'Цвет'
        buttons_callback_data = 'load_color_'
        width = 3
        dynamic_buttons = 3
        last_buttons = {'other_color': 'Другой цвет', **BaseBootButtons.last_buttons}

    load_other_color = {'message_text': 'Введите цвет автомобиля:', 'buttons': {'rewrite_boot_color': 'Назад', 'cancel_boot_new_commodity': 'Отмена', 'width': 1}}
    make_sure_selected_other_color = {'message_text': 'Ваш цвет: X', 'buttons': {'make_sure_other_color': 'Подтвердить', 'rewrite_other_boot_color': 'Изменить', 'width': 1}}
    load_other_color_incorrect_message_text = '\n<b>Цвет должен состоять только из букв, без пробелов(либо с дефисом).</b>'
    price_only = f'''Стоимость '''

    class load_commodity_price(BaseBootButtons, RedisBootCommodityHelper):
        message_text = '<blockquote><b>Стоимость: <i>X</i></b></blockquote>'
        width = 1

    class load_commodity_photo(BaseBootButtons, RedisBootCommodityHelper):
        message_text = 'Пришлите фото автомобиля\n(значок скрепки в левом углу чата)\n\n(!от 3 до 5 экземпляров!)\n\nНе отменяйте сжатие при отправке\nфотографии в телеграмм.'
        width = 1

    edit_photo_caption = 'Фото'


    config_for_seller = '<b>Ваши конфигурации:</b>'
    can_rewrite_config = 'Возможна перепись полей по нажатию на соответсвующую кнопку'
    config_for_seller_button_callbacks = ('rewrite_boot_state', 'rewrite_boot_engine', 'rewrite_boot_brand', 'rewrite_boot_model', 'rewrite_boot_complectation', 'rewrite_boot_year', 'rewrite_boot_mileage', 'rewrite_boot_color', 'rewrite_boot_price', 'rewrite_boot_photo')

    config_for_admins = '<b>Заявка от <i>@X</i></b>'

    seller_notification = {'message_text': 'Заявка №_ создана!'}

