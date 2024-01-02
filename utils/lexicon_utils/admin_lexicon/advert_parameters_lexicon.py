from utils.lexicon_utils.admin_lexicon.admin_lexicon import captions, return_main_menu

advert_parameters_captions = {
    'year': 'год', 'mileage': 'пробег', 'color': 'цвет', 'complectation': 'комплектация', 'model': 'модель',
    'brand': 'бренд'
}

__ADVERT_PARAMETERS_LEXICON = {
    'choose_second_hand_parameter_type': {'message_text': 'Параметры Б/У автомобилей:', 'buttons': {
        'second_hand_choice_advert_parameters_type_mileage': 'Пробег', 'second_hand_choice_advert_parameters_type_year': 'Год',
        'admin_backward:choose_second_hand_advert_parameters_type': captions['backward'],
        **return_main_menu,
        'width': 2
    }},

    'start_add_new_advert_parameter_value': {'message_text': 'Добавление параметра\nВведите новое значение для параметра: {parameter_name}',
                                             'buttons': {
                                                 'admin_backward:await_input_new_parameter_value': captions['backward'],
                                                 'width': 1
                                             }},
    'start_add_new_advert_parameter_value(exists)': 'Добавление параметра\nУказанное значение уже присутсвует в конфигурации: {parameter_name}, введите уникальное значение:',
    # 'start_add_new_advert_parameter_value': '',

    'confirmation_add_new_advert_parameter_value': {
        'message_text': 'Желаете добавить:\n{parameter_name}: {new_parameter_value} ?',
        'buttons': {
            'confirm_action_add_new_parameter_value': captions['confirm'],
            'admin_backward:confirmation_add_new_parameter_value_rewrite': 'Ввести заново',
            'admin_backward:confirmation_add_new_parameter_value_cancel': captions['cancel'],
            'width': 1
        }}
}

class AdvertParametersChooseState:
    message_text = 'Параметры автомобилей.\nВыберите состояние:'
    buttons_callback_data = 'advert_parameters_choose_state:'
    dynamic_buttons = 2
    width = 2
    backward_command = {'admin_backward:advert_parameters_choose_state': captions['backward'], **return_main_menu}

class AdvertSecondHandParametersChooseSpecificValue:
    message_text_mileage = 'Пробег:'
    message_text_year = 'Год выпуска:'
    buttons_callback_data = 'advert_parameters_specific_value:'
    dynamic_buttons = 3
    width = 2
    backward_command = {'add_new_advert_parameter': captions['add'],
                        'admin_backward:choose_specific_advert_parameter_value': captions['backward'],
                        **return_main_menu}

    def __init__(self, parameter_name: str):
        if parameter_name:
            ic(f'message_text_{parameter_name}')
            ic(self.__class__.__dict__)
            ic(self.__class__.__dict__.get(f'message_text_{parameter_name}'))
            self.message_text = self.__class__.__dict__.get(f'message_text_{parameter_name}')
            ic(self.message_text)
        self.buttons_callback_data = self.buttons_callback_data
        self.dynamic_buttons = self.dynamic_buttons
        self.width = self.width
        self.backward_command = self.backward_command