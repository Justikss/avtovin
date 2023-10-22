import importlib

from config_data.config import SUPPORT_NUMBER, SUPPORT_TELEGRAM

LEXICON = {
            'choose_language': {'message_text': 'Выберите ваш язык', 'language_uz': '🇺🇿 Uzb',
                                'language_ru': "🇷🇺 Rus", 'width': 2},
            'hello_text': {'message_text': 'Приветственное сообщение', 'start_sell': 'Продажа',
                           'start_buy': 'Покупка', 'width': 2},
            'write_full_name': {'message_text': 'Укажите ФИО', 'backward:user_registration': 'Назад', 'width': 1},
            'write_full_name(incorrect)': {
                'message_text': 'Некорректный ввод, принимается 2-3 буквенных слова, разделённые пробелом',
                'backward:user_registration': 'Назад', 'width': 2},
            'write_phone_number': {'message_text': 'Укажите номер телефона, начиная с +',
                                   'backward:user_registration_number': 'Назад', 'width': 1},
            'write_phone_number(incorrect)': {'message_text': 'Некорректный ввод номера, укажите номер начиная с +',
                                              'backward:user_registration_number': 'Назад', 'width': 1},
            # 'most_answers': {'message_text': 'Ответы на часто задаваемые вопросы', 'in_main': 'В меню', 'width': 1},
            'main_menu': {'message_text': 'Меню', 'offers_to_user': 'Предложения', 'car_search': 'Поиск Авто',
                          'faq': 'F.A.Q.', 'support': 'Поддержка', 'backward:set_language': 'Назад', 'width': 2},
            'f_a_q': {'message_text': 'Ответы на часто задаваемые вопросы:', 'return_main_menu': 'В меню',
                      'width': 1},
            'tech_support': {'message_text': 'Выберите ваше действие', 'write_to_support': 'Написать',
                             'call_to_support': 'Позвонить', 'width': 2, 'return_main_menu': 'В меню'},
            'write_to_support': {'message_text': SUPPORT_TELEGRAM, 'backward:support': 'Назад', 'width': 1},
            'call_to_support': {'message_text': SUPPORT_NUMBER, 'backward:support': 'Назад', 'width': 1},

            'search_car': {'message_text': 'Выберите категорию', 'new_cars': 'Новое', 'second_hand_cars': 'Б\У',
                           'return_main_menu': 'В меню', 'width': 2},
            'cars_not_found': {'message_text': 'К сожалению автомобилей этого класса нет на витрине.',
                               'backward:choose_car_category': 'Назад', 'return_main_menu': 'В меню', 'width': 1},

            'search_configuration': {'message_text': 'Настройте ваш поиск', 'start_configuration_search': 'Начать',
                                     'backward': 'Назад', 'width': 1},

            'choose_brand': {'message_text': 'Выберите марку', 'backward': 'Назад', 'width': 1},
            'choose_model': {'message_text': 'Выберите модель', 'backward_in_carpooling': 'Назад', 'width': 1},
            'choose_engine_type': {'message_text': 'Выберите тип двигателя', 'backward_in_carpooling': 'Назад',
                                   'width': 1},
            'choose_complectation': {'message_text': 'Выберите комплектацию', 'backward_in_carpooling': 'Назад',
                                     'width': 1},

            'choose_year_of_release': {'message_text': 'Выберите год', 'backward_in_carpooling': 'Назад',
                                       'width': 1},
            'choose_mileage': {'message_text': 'Выберите пробег', 'backward_in_carpooling': 'Назад', 'width': 1},
            'choose_color': {'message_text': 'Выберите цвет', 'backward_in_carpooling': 'Назад', 'width': 1},

            'chosen_configuration': {
                'message_text': {'your_configs': 'Ваши настройки:', 'engine_type': 'Тип двигателя: ',
                                 'model': 'Модель: ',
                                 'brand': 'Марка: ', 'complectation': 'Комплектация: ',
                                 'cost': 'Стоимость: ~', 'mileage': 'Пробег: ', 'year': 'Год: ',
                                 'color': 'Цвет: '}, 'confirm_buy_settings': 'Подтвердить',
                'backward_in_carpooling': 'Назад', 'width': 1},
            'confirm_buy_configuration': {'message_text': 'Вы успешно оставили заявку!',
                                          'return_main_menu': 'В меню', 'width': 1},

            'button_confirm_from_seller': 'Подтвердить',
            'buttons_history_output': {'pagination_left': '<', 'pagination_right': '>',
                                       'return_from_offers_history': 'В меню', 'width': 2},
            'backward_name': 'Назад',

            'show_offers_history': {'no_more_pages': 'Больше нет страниц', 'no_less_pages': 'Позади нет страниц',
                                    'history_not_found': 'История запросов пуста'},
            'offer_parts': {'dealship_name': 'Салон', 'car_price': 'Стоимость',
                            'dealship_contacts': 'Контакты салона',
                            'individual': 'Частное лицо', 'individual_contacts': 'Контакты'},

            "buyer_haven't_confirm_offers": 'История запросов пуста',
            "seller_haven't_this_car": 'У вас не продаётся такой автомобиль'
        }

# class LEXICON:
#     def __init__(self, input_language):
#         self.language = input_language
#         self.LEXICON = {
#             'choose_language': {'message_text': 'Выберите ваш язык', 'language_uz': '🇺🇿 Uzb',
#                                 'language_ru': "🇷🇺 Rus", 'width': 2},
#             'hello_text': {'message_text': 'Приветственное сообщение', 'start_sell': 'Продажа',
#                            'start_buy': 'Покупка', 'width': 2},
#             'write_full_name': {'message_text': 'Укажите ФИО', 'backward:user_registration': 'Назад', 'width': 1},
#             'write_full_name(incorrect)': {
#                 'message_text': 'Некорректный ввод, принимается 2-3 буквенных слова, разделённые пробелом',
#                 'backward:user_registration': 'Назад', 'width': 2},
#             'write_phone_number': {'message_text': 'Укажите номер телефона, начиная с +',
#                                    'backward:user_registration_number': 'Назад', 'width': 1},
#             'write_phone_number(incorrect)': {'message_text': 'Некорректный ввод номера, укажите номер начиная с +',
#                                               'backward:user_registration_number': 'Назад', 'width': 1},
#             # 'most_answers': {'message_text': 'Ответы на часто задаваемые вопросы', 'in_main': 'В меню', 'width': 1},
#             'main_menu': {'message_text': 'Меню', 'offers_to_user': 'Предложения', 'car_search': 'Поиск Авто',
#                           'faq': 'F.A.Q.', 'support': 'Поддержка', 'backward:set_language': 'Назад', 'width': 2},
#             'f_a_q': {'message_text': 'Ответы на часто задаваемые вопросы:', 'return_main_menu': 'В меню',
#                       'width': 1},
#             'tech_support': {'message_text': 'Выберите ваше действие', 'write_to_support': 'Написать',
#                              'call_to_support': 'Позвонить', 'width': 2, 'return_main_menu': 'В меню'},
#             'write_to_support': {'message_text': SUPPORT_TELEGRAM, 'backward:support': 'Назад', 'width': 1},
#             'call_to_support': {'message_text': SUPPORT_NUMBER, 'backward:support': 'Назад', 'width': 1},
#
#             'search_car': {'message_text': 'Выберите категорию', 'new_cars': 'Новое', 'second_hand_cars': 'Б\У',
#                            'return_main_menu': 'В меню', 'width': 2},
#             'cars_not_found': {'message_text': 'К сожалению автомобилей этого класса нет на витрине.',
#                                'backward:choose_car_category': 'Назад', 'return_main_menu': 'В меню', 'width': 1},
#
#             'search_configuration': {'message_text': 'Настройте ваш поиск', 'start_configuration_search': 'Начать',
#                                      'backward': 'Назад', 'width': 1},
#
#             'choose_brand': {'message_text': 'Выберите марку', 'backward': 'Назад', 'width': 1},
#             'choose_model': {'message_text': 'Выберите модель', 'backward_in_carpooling': 'Назад', 'width': 1},
#             'choose_engine_type': {'message_text': 'Выберите тип двигателя', 'backward_in_carpooling': 'Назад',
#                                    'width': 1},
#             'choose_complectation': {'message_text': 'Выберите комплектацию', 'backward_in_carpooling': 'Назад',
#                                      'width': 1},
#
#             'choose_year_of_release': {'message_text': 'Выберите год', 'backward_in_carpooling': 'Назад',
#                                        'width': 1},
#             'choose_mileage': {'message_text': 'Выберите пробег', 'backward_in_carpooling': 'Назад', 'width': 1},
#             'choose_color': {'message_text': 'Выберите цвет', 'backward_in_carpooling': 'Назад', 'width': 1},
#
#             'chosen_configuration': {
#                 'message_text': {'your_configs': 'Ваши настройки:', 'engine_type': 'Тип двигателя: ',
#                                  'model': 'Модель: ',
#                                  'brand': 'Марка: ', 'complectation': 'Комплектация: ',
#                                  'cost': 'Стоимость: ', 'mileage': 'Пробег: ', 'year': 'Год: ',
#                                  'color': 'Цвет: '}, 'confirm_buy_settings': 'Подтвердить',
#                 'backward_in_carpooling': 'Назад', 'width': 1},
#             'confirm_buy_configuration': {'message_text': 'Вы успешно оставили заявку!',
#                                           'return_main_menu': 'В меню', 'width': 1},
#
#             'button_confirm_from_seller': 'Подтвердить',
#             'buttons_history_output': {'pagination_left': '<', 'pagination_right': '>',
#                                        'return_from_offers_history': 'В меню', 'width': 2},
#             'backward_name': 'Назад',
#
#             'show_offers_history': {'no_more_pages': 'Больше нет страниц', 'no_less_pages': 'Позади нет страниц',
#                                     'history_not_found': 'История запросов пуста'},
#             'offer_parts': {'dealship_name': 'Салон', 'car_price': 'Стоимость',
#                             'dealship_contacts': 'Контакты салона',
#                             'individual': 'Частное лицо', 'individual_contacts': 'Контакты'},
#
#             "buyer_haven't_confirm_offers": 'История запросов пуста',
#             "seller_haven't_this_car": 'У вас не продаётся такой автомобиль'
#         }
#         if input_language == 'ru':
#             pass
#         elif input_language == 'uz':
#             self.LEXICON = {
#             'choose_language': {'message_text': 'Выберите ваш язык', 'language_uz': '🇺🇿 Uzb',
#                                 'language_ru': "🇷🇺 Rus", 'width': 2},
#             'hello_text': {'message_text': 'Приветственное сообщение', 'start_sell': 'Продажа',
#                            'start_buy': 'Покупка', 'width': 2},
#             'write_full_name': {'message_text': 'Укажите ФИО', 'backward:user_registration': 'Назад', 'width': 1},
#             'write_full_name(incorrect)': {
#                 'message_text': 'Некорректный ввод, принимается 2-3 буквенных слова, разделённые пробелом',
#                 'backward:user_registration': 'Назад', 'width': 2},
#             'write_phone_number': {'message_text': 'Укажите номер телефона, начиная с +',
#                                    'backward:user_registration_number': 'Назад', 'width': 1},
#             'write_phone_number(incorrect)': {'message_text': 'Некорректный ввод номера, укажите номер начиная с +',
#                                               'backward:user_registration_number': 'Назад', 'width': 1},
#             # 'most_answers': {'message_text': 'Ответы на часто задаваемые вопросы', 'in_main': 'В меню', 'width': 1},
#             'main_menu': {'message_text': 'Меню', 'offers_to_user': 'Предложения', 'car_search': 'Поиск Авто',
#                           'faq': 'F.A.Q.', 'support': 'Поддержка', 'backward:set_language': 'Назад', 'width': 2},
#             'f_a_q': {'message_text': 'Ответы на часто задаваемые вопросы:', 'return_main_menu': 'В меню',
#                       'width': 1},
#             'tech_support': {'message_text': 'Выберите ваше действие', 'write_to_support': 'Написать',
#                              'call_to_support': 'Позвонить', 'width': 2, 'return_main_menu': 'В меню'},
#             'write_to_support': {'message_text': SUPPORT_TELEGRAM, 'backward:support': 'Назад', 'width': 1},
#             'call_to_support': {'message_text': SUPPORT_NUMBER, 'backward:support': 'Назад', 'width': 1},
#
#             'search_car': {'message_text': 'Выберите категорию', 'new_cars': 'Новое', 'second_hand_cars': 'Б\У',
#                            'return_main_menu': 'В меню', 'width': 2},
#             'cars_not_found': {'message_text': 'К сожалению автомобилей этого класса нет на витрине.',
#                                'backward:choose_car_category': 'Назад', 'return_main_menu': 'В меню', 'width': 1},
#
#             'search_configuration': {'message_text': 'Настройте ваш поиск', 'start_configuration_search': 'Начать',
#                                      'backward': 'Назад', 'width': 1},
#
#             'choose_brand': {'message_text': 'Выберите марку', 'backward': 'Назад', 'width': 1},
#             'choose_model': {'message_text': 'Выберите модель', 'backward_in_carpooling': 'Назад', 'width': 1},
#             'choose_engine_type': {'message_text': 'Выберите тип двигателя', 'backward_in_carpooling': 'Назад',
#                                    'width': 1},
#             'choose_complectation': {'message_text': 'Выберите комплектацию', 'backward_in_carpooling': 'Назад',
#                                      'width': 1},
#
#             'choose_year_of_release': {'message_text': 'Выберите год', 'backward_in_carpooling': 'Назад',
#                                        'width': 1},
#             'choose_mileage': {'message_text': 'Выберите пробег', 'backward_in_carpooling': 'Назад', 'width': 1},
#             'choose_color': {'message_text': 'Выберите цвет', 'backward_in_carpooling': 'Назад', 'width': 1},
#
#             'chosen_configuration': {
#                 'message_text': {'your_configs': 'Ваши настройки:', 'engine_type': 'Тип двигателя: ',
#                                  'model': 'Модель: ',
#                                  'brand': 'Марка: ', 'complectation': 'Комплектация: ',
#                                  'cost': 'Стоимость: ', 'mileage': 'Пробег: ', 'year': 'Год: ',
#                                  'color': 'Цвет: '}, 'confirm_buy_settings': 'Подтвердить',
#                 'backward_in_carpooling:': 'Назад', 'width': 1},
#             'confirm_buy_configuration': {'message_text': 'Вы успешно оставили заявку!',
#                                           'return_main_menu': 'В меню', 'width': 1},
#
#             'button_confirm_from_seller': 'Подтвердить',
#             'buttons_history_output': {'pagination_left': '<', 'pagination_right': '>',
#                                        'return_from_offers_history': 'В меню', 'width': 2},
#             'backward_name': 'Назад',
#
#             'show_offers_history': {'no_more_pages': 'Больше нет страниц', 'no_less_pages': 'Позади нет страниц',
#                                     'history_not_found': 'История запросов пуста'},
#             'offer_parts': {'dealship_name': 'Салон', 'car_price': 'Стоимость',
#                             'dealship_contacts': 'Контакты салона',
#                             'individual': 'Частное лицо', 'individual_contacts': 'Контакты'},
#
#             "buyer_haven't_confirm_offers": 'История запросов пуста',
#             "seller_haven't_this_car": 'У вас не продаётся такой автомобиль'
#         }




