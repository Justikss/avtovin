from utils.lexicon_utils.admin_lexicon.admin_lexicon import captions, return_main_menu


__ADVERT_PARAMETERS_LEXICON = {
    'choose_second_hand_parameter_type': {'message_text': 'Параметры Б/У автомобилей:', 'buttons': {
        'advert_second_hand_parameters_type_mileage': 'Пробег', 'advert_second_hand_parameters_type_year': 'Год',
        'admin_backward:choose_second_hand_advert_parameters_type': captions['backward'],
        **return_main_menu,
        'width': 2
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
    buttons_callback_data = 'second_hand_advert_parameters_specific_value:'
    dynamic_buttons = 3
    width = 2
    backward_command = {'add_new_second_hand_parameter': captions['add'],
                        'admin_backward:choose_specific_second_hand_value': captions['backward'],
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