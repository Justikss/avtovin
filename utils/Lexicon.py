import importlib

from config_data.config import SUPPORT_NUMBER, SUPPORT_TELEGRAM

LEXICON = {
            'unexpected_behavior': 'Неожиданное поведение',
            'too_late': 'Вы опоздали',
            'success_notification': 'Принято',
            'user_in_system': {'message_text': 'Вы в системе'},
            'choose_language': {'message_text': 'Выберите ваш язык', 'language_uz': '🇺🇿 Uzb',
                                'language_ru': "🇷🇺 Rus", 'width': 2},
            'hello_text': {'message_text': 'Приветственное сообщение', 'start_sell': 'Продажа',
                           'start_buy': 'Покупка', 'width': 2},
            'write_full_name': {'message_text': 'Укажите ФИО', 'backward:user_registration': 'Назад', 'width': 1},
            'write_full_name(novalid)': {
                'message_text': 'Некорректный ввод, принимается 2-3 буквенных слова, разделённые пробелом',
                'backward:user_registration': 'Назад', 'width': 2},
            'write_phone_number': {'message_text': 'Укажите номер телефона, начиная с +',
                                   'backward:user_registration_number': 'Назад', 'width': 1},
            'write_phone_number(novalid)': {'message_text': 'Некорректный ввод номера, укажите номер начиная с +',
                                              'backward:user_registration_number': 'Назад', 'width': 1},
            'write_phone_number(exists)': {'message_text': 'Некорректный ввод номера!\nОн уже зарегистрирован\nожидается иной',
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

            'choose_engine_type': {'message_text': 'Выберите тип двигателя', 'backward': 'Назад',
                                               'width': 1},
            'choose_brand': {'message_text': 'Выберите марку', 'backward_in_carpooling': 'Назад', 'width': 1},
            'choose_model': {'message_text': 'Выберите модель', 'backward_in_carpooling': 'Назад', 'width': 1},

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
                                 'cost': 'Ориентировочная стоимость: ~', 'mileage': 'Пробег: ', 'year': 'Год: ',
                                 'color': 'Цвет: '}, 'confirm_buy_settings': 'Подтвердить',
                'backward_in_carpooling': 'Назад', 'width': 1},
                
            'confirm_buy_configuration': {'message_text': 'Вы успешно оставили заявку!',
                                          'return_main_menu': 'В меню', 'width': 1},
            'buy_configuration_error': {'message_text': 'У вас уже оставлена такая заявка.', 
                                        'return_main_menu': 'В меню', 'width': 1},
            'buy_configuration_non_registration': {'message_text': 'Ошибка. Ваш аккаунт незарегестрирован\nНажмите /start'},

            'confirm_from_seller': {'message_text': {'from_user': 'Пользователь', 'tendered': 'оставил заявку:',
            'contacts': 'Контакты:', 'separator': '=' * 40}, 'confirm_button': 'Подтвердить'},

            'buttons_history_output': {'pagination_left': '<', 'pagination_right': '>',
                                       'return_from_offers_history': 'В меню', 'width': 2},
            'backward_name': 'Назад',


            'show_offers_history': {'no_more_pages': 'Больше нет страниц', 'no_less_pages': 'Позади нет страниц',
                                    'history_not_found': 'История запросов пуста'},
            'offer_parts': {'dealship_name': 'Салон', 'car_price': 'Примерная цена',
                            'dealship_contacts': 'Контакты салона',
                            'individual': 'Частное лицо', 'individual_contacts': 'Контакты'},

            "buyer_haven't_confirm_offers": 'История запросов пуста',
            "seller_haven't_this_car": 'У вас не продаётся такой автомобиль',
            
            
            'who_is_seller': {'message_text': 'Выберите пункты ниже:', 'i_am_private_person': 'Частное лицо', 'i_am_car_dealership': 'Автосалон', 'width': 2},
            'write_full_seller_name': {'message_text': 'Укажите ФИО', 'backward:seller_registration': 'Назад', 'width': 1},
            'write_full_seller_name(novalid)': {
                'message_text': 'Некорректный ввод, принимается 2-3 буквенных слова, разделённые пробелом',
                'backward:user_registration': 'Назад', 'width': 2},
            'write_full_seller_name(exists)': {'message_text': 'Это имя уже зарегестрировано\nожидается иное', 'backward:seller_registration': 'Назад', 'width': 1},
            
            
            'write_dealership_name': {'message_text': 'Введите название автосалона:', 'backward:seller_registration': 'Назад', 'width': 1},
            'write_dealership_name(novalid)': {'message_text': 'Название автосалона должно быть длинной < 250 символов\nИ Только из букв и цифр:', 'backward:seller_registration': 'Назад', 'width': 1},
            'write_dealership_name(exists)': {'message_text': 'Это название уже зарегестрировано\nожидается иное', 'backward:seller_registration': 'Назад', 'width': 1},
            

            'write_seller_phone_number': {'message_text': 'Укажите номер телефона, начиная с +',
                                   'backward:seller_registration_number': 'Назад', 'width': 1},
            'write_seller_phone_number(novalid)': {'message_text': 'Некорректный ввод номера, укажите номер начиная с +',
                                              'backward:seller_registration_number': 'Назад', 'width': 1},
            'write_seller_phone_number(exists)': {'message_text': 'Некорректный ввод номера!\nОн уже зарегистрирован\nожидается иной',
                                              'backward:seller_registration_number': 'Назад', 'width': 1},          
            'write_dealership_address': {'message_text': 'Введите адрес автосалона', 'backward:seller_registration_number': 'Назад', 'width': 1},
            'write_dealership_address(novalid)': {'message_text': 'Ошибка\n Адрес автосалона должен содержать буквы', 'backward:seller_registration_number': 'Назад', 'width': 1},


            'checking_seller_entered_data': {'message_text': 'Введённые данные корректны?\n(Нажмите на поле для его переписи)', 'rewrite_seller_name': '', 'rewrite_seller_number': '', 'rewrite_dealership_address': '', 'confirm_registration_from_seller': 'Да, всё верно', 'width': 1},
            'confirm_registration_from_seller': {'message_text': 'Регисрация завершена\nДождитесь одобрения от администрации', 'return_to_sell_zone': 'К покупкам', 'width': 1},
            'try_again_seller_registration': {'message_text': 'Ошибка.\nдля подробностей перепройдите процесс регистрации.', 'return_to_start_seller_registration': 'Перепройти регистрацию', 'width': 1},
            'seller_main_menu': {'message_text': 'Успешно профиль подтверждён!', 'seller_pofile': 'Профиль', 'seller_faq': 'FAQ', 'support': 'Поддержка', 'create_seller_request': 'Заявки', 'width': 2},

            'confirm_new_seller_registration_from_admin_button': {'confirm_from_admin': 'Подтвердить', 'callback_startswith': 'confirm_new_seller_registration_from:'},
            'seller_waiting_registration_confirm': {'start_text_legal': 'Заявка на регистрацию автосалона:', 'start_text_natural': 'Заявка на регистрацию частного продавца:',
                                                 'legal_message': {'name': 'Название автосалона: ', 'address': 'Адрес: '},
                                                  'natural_message': {'name': 'Имя: ', 'surname': 'Фамилия: ', 'patronymic': 'Отчество: '},
                                                   'phone_number': 'Телефонный номер: '},
            'success_seller_registration_notice': {'message_text': 'Вы зарегестрированы в системе', 'return_seller_main_menu': 'В меню продавца', 'width': 1}
            
            
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




