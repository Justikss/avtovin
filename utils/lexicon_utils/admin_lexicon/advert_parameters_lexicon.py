from utils.lexicon_utils.admin_lexicon.admin_lexicon import captions, return_main_menu

advert_parameters_captions = {
    'year': 'Год', 'mileage': 'Пробег', 'color': 'Цвет', 'complectation': 'Комплектация', 'model': 'Модель',
    'brand': 'Бренд', 'state': 'Состояние', 'engine': 'Двигатель', 'param': 'параметра', 'params': 'параметров'
}

__ADVERT_PARAMETERS_LEXICON = {
    'memory_was_forgotten': 'Сброс к началу',
    'selected_new_car_params_pattern': '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n{params_data}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n',
    'this_advert_parameter_dont_can_was_deleting': 'Выбранная характеристика не может быть удалена так как на неё зарегистрированы объявления!',

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
        }},

    'choose_action_on_specific_parameter_value': {
        'message_text': 'Выбранный параметр:\n{parameter_name}: {parameter_value}', 'buttons': {
            'delete_current_advert_parameter': captions['delete'], 'rewrite_current_advert_parameter': 'Редактировать',
            'admin_backward:choose_action_on_specific_adv_parameter': captions['backward'],
            **return_main_menu,
            'width': 2
    }},
    'confirmation_to_delete_exists_parameter': {
        'message_text': 'Подтвердите удаление {param_or_params}:\n{parameter_type_to_parameter_value}', 'buttons': {
            'confirm_delete_advert_parameter': captions['confirm'],
            'admin_backward:confirmation_delete_advert_param': captions['backward'],
            **return_main_menu,
            'width': 1
        }
    },

    'start_rewrite_exists_parameter': {
        'message_text': 'Редактирование.\nВведите новое значения для параметра:\n{parameter_type}: {parameter_value}',
        'buttons': {
            'admin_backward:start_rewrite_exists_parameter_value': captions['backward'],
            'width': 1
        }},
    'start_rewrite_exists_parameter(exists)': 'Редактирование.\nВведённое значения уже существует на выбранном параметре: {parameter_type}',

    'confirmation_rewrite_exists_parameter': {
        'message_text': 'Вы действительно хотите редактировать значения параметра: {parameter_type}\nС: {parameter_old_value}\nНа: {parameter_new_value} ?',
        'buttons': {'confirm_rewrite_existing_advert_parameter': captions['confirm'],
                    'rewrite_current_advert_parameter': 'Ввести заново',
                    'admin_backward:rewrite_exists_advert_param': captions['backward'],
                    'width': 1}
    },
    'review_params_branch': {'message_text': '',
                             'buttons': {'rewrite_current_advert_parameter': 'Редактировать',
                                         'update_media_group': 'Обновить фотографии',
                                         'delete_current_advert_parameter': captions['delete'],
                                         'admin_backward:review_params_branch': captions['backward'],
                                         'admin_backward:go_to_choose_params_state': 'В начало выборки',
                                         **return_main_menu,
                                         'width': 1}}
}

class AdvertParametersChooseState:
    message_text = 'Параметры автомобилей.\nВыберите состояние:'
    buttons_callback_data = 'advert_parameters_choose_state:'
    dynamic_buttons = 2
    width = 2
    backward_command = {'admin_backward:advert_parameters_choose_state': captions['backward'], **return_main_menu}

class AdvertParametersChooseSpecificValue:
    message_text_mileage = f'''{advert_parameters_captions['mileage']}:'''
    message_text_year = 'Год выпуска:'
    message_text_engine = f'''{advert_parameters_captions['engine']}:'''
    message_text_brand = f'''{advert_parameters_captions['brand']}:'''
    message_text_model = f'''{advert_parameters_captions['model']}:'''
    message_text_complectation = f'''{advert_parameters_captions['complectation']}:'''
    message_text_color = f'''{advert_parameters_captions['color']}:'''
    buttons_callback_data_second_hand = 'advert_parameters_specific_value:'
    buttons_callback_data_new = 'new_state_parameters:'
    dynamic_buttons = 3
    width = 2
    second_hand_buttons_interface = {'add_new_advert_parameter': captions['add']}
    new_buttons_interface = {'delete_current_advert_parameter': captions['delete'],
                            'rewrite_current_advert_parameter': 'Редактировать',
                            **second_hand_buttons_interface}
    backward_command = {'admin_backward:choose_specific_advert_parameter_value': captions['backward'],
                        **return_main_menu}

    def __init__(self, parameter_name: str, header: str):

        if parameter_name:
            self.message_text = f'''{header}{self.__class__.__dict__.get(f'message_text_{parameter_name}')}'''

            ic(self.message_text)
        if header:
            self.buttons_interface = self.new_buttons_interface
            self.buttons_callback_data = self.buttons_callback_data_new
        else:
            self.buttons_interface = self.second_hand_buttons_interface
            self.buttons_callback_data = self.buttons_callback_data_second_hand

        self.dynamic_buttons = self.dynamic_buttons
        self.width = self.width

        ic(self.backward_command, self.buttons_interface)

        self.backward_command = {**self.buttons_interface, **self.backward_command}

        ic(self.backward_command, self.buttons_interface)
