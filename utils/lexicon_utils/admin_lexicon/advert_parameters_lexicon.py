
from utils.lexicon_utils.lexicon_uz.admin_lexicon_uz.advert_parameters_uz import advert_params_class_lexicon_uz, \
    advert_params_captions_uz
from utils.safe_dict_class import SafeDict

_captions = {'backward': '◂ Назад ▸', 'was_selected': 'Вы выбрали', 'cancel': 'Отменить', 'confirm': 'Подтвердить',
            'sales': 'продажам', 'purchases': 'покупкам', 'any': 'всё время', 'day': 'день', 'week': 'неделю',
            'month': 'месяц', 'year': 'год', 'days': 'дней', 'feedbacks': 'откликов',
            'dont_write_html_tags': 'Запрещён ввод знаков "&lt; &gt;".',
            'all_users': 'всех', 'buyers': 'покупателей', 'sellers': 'продавцов', 'delete': 'Удалить',
            'by_dealership': 'автосалона',
            'by_seller': 'частного лица', 'close': 'Скрыть', 'surname_name_patronymic': 'ФИО: ', 'add': 'Добавить',
            'successfully': 'Успешно'
            }

return_main_menu = {'return_main_menu': 'В меню'}


advert_parameters_captions = {
    'year': 'Год', 'mileage': 'Пробег', 'color': 'Цвет', 'complectation': 'Комплектация', 'model': 'Модель',
    'brand': 'Бренд', 'state': 'Состояние', 'engine': 'Двигатель', 'from_param_branch': ' из ветки параметров:\n{param_branch}\n',
    'year_of_realise': 'Год выпуска'
}

__ADVERT_PARAMETERS_LEXICON = {
    'memory_was_forgotten': 'Сброс к началу',
    'selected_new_car_params_pattern': '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n{params_data}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n',
    'this_advert_parameter_dont_can_was_deleting': 'Выбранная характеристика не может быть удалена так как на неё зарегистрированы объявления!',

    'choose_second_hand_parameter_type': {'message_text': 'Параметры Б/У автомобилей:', 'buttons': {
        'second_hand_choice_advert_parameters_type_mileage': 'Пробег', 'second_hand_choice_advert_parameters_type_year': 'Год',
        'admin_backward:choose_second_hand_advert_parameters_type': _captions['backward'],
        **return_main_menu,
        'width': 2
    }},

    'start_add_new_advert_parameter_value': {'message_text': 'Добавление параметра\nВведите новое значение для параметра: {parameter_name}',
                                             'buttons': {
                                                 'admin_backward:await_input_new_parameter_value': _captions['backward'],
                                                 'width': 1
                                             }},
    'start_add_new_advert_parameter_value_new_state_buttons': {
        'admin_backward:await_input_new_parameter_value': _captions['backward'],
        'admin_backward:go_to_choose_params_state': 'В начало выборки',
        'width': 1},


    'start_add_new_advert_parameter_value(exists)': 'Добавление параметра\nУказанное значение уже присутсвует в конфигурации: {parameter_name}, введите уникальное значение:',
    # 'start_add_new_advert_parameter_value': '',

    'confirmation_add_new_advert_parameter_value': {
        'message_text': 'Желаете добавить:\n{parameter_name}: {new_parameter_value} ?',
        'buttons': {
            'confirm_action_add_new_parameter_value': _captions['confirm'],
            'admin_backward:confirmation_add_new_parameter_value_rewrite': 'Ввести заново',
            'admin_backward:confirmation_add_new_parameter_value_cancel': _captions['cancel'],
            'width': 1
        }},

    'choose_action_on_specific_parameter_value': {
        'message_text': 'Выбранный параметр:\n{parameter_name}: {parameter_value}', 'buttons': {
            'delete_current_advert_parameter': _captions['delete'], 'rewrite_current_advert_parameter': 'Редактировать',
            'admin_backward:choose_action_on_specific_adv_parameter': _captions['backward'],
            **return_main_menu,
            'width': 2
    }},
    'confirmation_to_delete_exists_parameter': {
        'message_text': 'Подтвердите удаление{from_param_branch}\nПараметра:\n{parameter_type_to_parameter_value}', 'buttons': {
            'confirm_delete_advert_parameter': _captions['confirm'],
            'admin_backward:confirmation_delete_advert_param': _captions['backward'],
            **return_main_menu,
            'width': 1
        }
    },

    'start_rewrite_exists_parameter': {
        'message_text': 'Редактирование.\nВведите новое значения для параметра:\n{parameter_type}: {parameter_value}',
        'buttons': {
            'admin_backward:start_rewrite_exists_parameter_value': _captions['backward'],
            'width': 1
        }},
    'start_rewrite_exists_parameter(exists)': 'Редактирование.\nВведённое значения уже существует на выбранном параметре: {parameter_type}',

    'confirmation_rewrite_exists_parameter': {
        'message_text': 'Вы действительно хотите редактировать значения параметра: {parameter_type}\nС: {parameter_old_value}\nНа: {parameter_new_value} ?',
        'buttons': {'confirm_rewrite_existing_advert_parameter': _captions['confirm'],
                    'rewrite_current_advert_parameter': 'Ввести заново',
                    'admin_backward:rewrite_exists_advert_param': _captions['backward'],
                    'width': 1}
    },
    'input_photos_to_load_param_branch': {'message_text': 'Пришлите от 3-5 фотографий автомобиля\nсогласно введённым характеристикам:',
                                          'buttons': {
                                              'admin_backward:await_input_new_parameter_value': _captions['backward'],
                                              'width': 1
                                          }},
    'load_new_params_branch_confirmation': {
        'message_text': 'Ожидание подтверждения загрузки новой ветки параметров для авто:', 'buttons': {
                                        'confirm_load_new_params_branch': _captions['confirm'],
                                        'update_params_branch_media_group': 'Обновить фотографии',
                                         'admin_backward:review_params_branch_to_load': _captions['backward'],
                                         'admin_backward:go_to_choose_params_state': 'В начало выборки',
                                         **return_main_menu,
                                         'width': 1
        }},
    'review_params_branch': {'message_text': '',
                             'buttons': {'rewrite_current_advert_parameter': 'Редактировать',
                                         'update_params_branch_media_group': 'Обновить фотографии',
                                         'delete_current_advert_parameter': _captions['delete'],
                                         'admin_backward:review_params_branch': _captions['backward'],
                                         'admin_backward:go_to_choose_params_state': 'В начало выборки',
                                         **return_main_menu,
                                         'width': 1}}
}

# Добавление в русский словарь
advert_params_class_lexicon_ru = {
    'car_parameters_message_text': 'Параметры автомобилей.\nВыберите состояние:',
    'rewrite_current_advert_parameter': 'Редактировать',
    'backward': '◂ Назад ▸',
    'delete': 'Удалить',
    'add': 'Добавить',

    'return_main_menu': 'В меню'
}

advert_params_captions = SafeDict({'ru': advert_parameters_captions,
                                   'uz': advert_params_captions_uz})

advert_params_class_lexicon = SafeDict({'ru': advert_params_class_lexicon_ru,
                                        'uz': advert_params_class_lexicon_uz})

class AdvertParametersChooseState:
    def __init__(self):
        self.message_text = advert_params_class_lexicon['car_parameters_message_text']  # Или lexicon_uz для узбекской версии
        self.buttons_callback_data = 'advert_parameters_choose_state:'
        self.dynamic_buttons = 2
        self.width = 2
        self.backward_command = {'admin_backward:advert_parameters_choose_state': advert_params_class_lexicon['backward'],
                            'return_main_menu': advert_params_class_lexicon['return_main_menu']}

class AdvertParametersChooseSpecificValue:
    def __init__(self, parameter_name: str, header: str):
        self.message_text_mileage = f'''{advert_parameters_captions['mileage']}:'''
        self.message_text_year = f'''{advert_parameters_captions['year_of_realise']}:'''
        self.message_text_engine = f'''{advert_parameters_captions['engine']}:'''
        self.message_text_brand = f'''{advert_parameters_captions['brand']}:'''
        self.message_text_model = f'''{advert_parameters_captions['model']}:'''
        self.message_text_complectation = f'''{advert_parameters_captions['complectation']}:'''
        self.message_text_color = f'''{advert_parameters_captions['color']}:'''
        self.buttons_callback_data_second_hand = 'advert_parameters_specific_value:'
        self.buttons_callback_data_new = 'new_state_parameters:'
        self.dynamic_buttons = 3
        self.width = 2
        self.second_hand_buttons_interface = {'add_new_advert_parameter': advert_params_class_lexicon['add']}
        self.new_buttons_interface = {'delete_current_advert_parameter': advert_params_class_lexicon['delete'],
                                 'rewrite_current_advert_parameter': advert_params_class_lexicon[
                                     'rewrite_current_advert_parameter'],
                                 **self.second_hand_buttons_interface}
        self.backward_command = {
            'admin_backward:choose_specific_advert_parameter_value': advert_params_class_lexicon['backward'],
            'return_main_menu': advert_params_class_lexicon['return_main_menu']}

        if parameter_name:
            self.message_text = f'''{header if header else ''}{self.__class__.__dict__.get(f'message_text_{parameter_name}')}'''

        if header:
            if parameter_name == 'brand':
                self.buttons_interface = self.second_hand_buttons_interface
            else:
                self.buttons_interface = self.new_buttons_interface
            self.buttons_callback_data = self.buttons_callback_data_new
        else:
            self.buttons_interface = self.second_hand_buttons_interface
            self.buttons_callback_data = self.buttons_callback_data_second_hand

        if parameter_name not in ('state', 'engine'):
            self.backward_command = {**self.buttons_interface, **self.backward_command}


AdvertParametersChooseState = AdvertParametersChooseState()