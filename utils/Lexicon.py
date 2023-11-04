import importlib

from dataclasses import dataclass

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
            'write_full_seller_name': {'message_text': 'Укажите ФИО', 'backward:seller_registration_seller_person_name': 'Назад', 'width': 1},
            'write_full_seller_name(novalid)': {
                'message_text': 'Некорректный ввод, принимается 2-3 буквенных слова, разделённые пробелом',
                'backward:seller_registration_seller_person_name': 'Назад', 'width': 2},
            'write_full_seller_name(exists)': {'message_text': 'Это имя уже зарегестрировано\nожидается иное', 'backward:seller_registration_seller_person_name': 'Назад', 'width': 1},
            
            'write_dealership_name': {'message_text': 'Введите название автосалона:', 'backward:seller_registration_dealership_name': 'Назад', 'width': 1},
            'write_dealership_name(novalid)': {'message_text': 'Название автосалона должно быть длинной < 250 символов\nИ Только из букв и цифр:', 'backward:seller_registration_dealership_name': 'Назад', 'width': 1},
            'write_dealership_name(exists)': {'message_text': 'Это название уже зарегестрировано\nожидается иное', 'backward:seller_registration_dealership_name': 'Назад', 'width': 1},
            
            'write_seller_phone_number': {'message_text': 'Укажите номер телефона, начиная с +',
                                   'backward:seller_registration_number': 'Назад', 'width': 1},
            'write_seller_phone_number(novalid)': {'message_text': 'Некорректный ввод номера, укажите номер начиная с +',
                                              'backward:seller_registration_number': 'Назад', 'width': 1},
            'write_seller_phone_number(exists)': {'message_text': 'Некорректный ввод номера!\nОн уже зарегистрирован\nожидается иной',
                                              'backward:seller_registration_number': 'Назад', 'width': 1},          
            
            'write_dealership_address': {'message_text': 'Введите адрес автосалона', 'backward:seller_registration_dealership_address': 'Назад', 'width': 1},
            'write_dealership_address(novalid)': {'message_text': 'Ошибка\n Адрес автосалона должен содержать буквы', 'backward:seller_registration_dealership_address': 'Назад', 'width': 1},


            'checking_seller_entered_data': {'message_text': 'Введённые данные корректны?\n(Нажмите на поле для его переписи)', 'rewrite_seller_name': '', 'rewrite_seller_number': '', 'rewrite_dealership_address': '', 'confirm_registration_from_seller': 'Да, всё верно', 'width': 1},
            'confirm_registration_from_seller': {'message_text': 'Регисрация завершена\nДождитесь одобрения от администрации', 'return_to_sell_zone': 'К покупкам', 'width': 1},
            'try_again_seller_registration': {'message_text': 'Ошибка.\nдля подробностей перепройдите процесс регистрации.', 'return_to_start_seller_registration': 'Перепройти регистрацию', 'width': 1},
            'seller_main_menu': {'message_text': 'Успешно профиль подтверждён!', 'seller_pofile': 'Профиль', 'seller_faq': 'FAQ', 'support': 'Поддержка', 'create_seller_request': 'Заявки', 'width': 2},

            'confirm_new_seller_registration_from_admin_button': {'confirm_from_admin': 'Подтвердить', 'callback_startswith': 'confirm_new_seller_registration_from:'},
            'seller_waiting_registration_confirm': {'start_text_legal': 'Заявка на регистрацию автосалона:', 'start_text_natural': 'Заявка на регистрацию частного продавца:',
                                                 'legal_message': {'name': 'Название автосалона: ', 'address': 'Адрес: '},
                                                  'natural_message': {'name': 'Имя: ', 'surname': 'Фамилия: ', 'patronymic': 'Отчество: '},
                                                   'phone_number': 'Телефонный номер: '},
            'success_seller_registration_notice': {'message_text': 'Вы зарегестрированы в системе', 'return_main_menu': 'В меню продавца', 'width': 1},

            'seller_faq': {'message_text': 'Самые частые вопросы: ', 'return_main_menu': 'В меню', 'width': 1},
            'create_seller_request': {'message_text': 'Заявки', 'create_new_request': 'Создать заявку', 'return_main_menu': 'В меню', 'width': 1},

            'confirm_load_config_from_seller_button': {'confirm_load_config_from_seller': 'Подтвердить', 'width': 1},
            'seller_load_notification_button': {'return_main_menu': 'В меню'},

            'message_not_digit': ' должна состоять только из цифр',
            'message_not_photo': '\nПришлите url-ссылку или прикрепите фотографию\n(значок скрепки в левом углу чата)'
            
        }


class LexiconCommodityLoader:
    load_commodity_state = {'message_text': 'Бу/Новое', 'buttons': {'load_state_new': 'Новое', 'load_state_second_hand': 'Б/у', 'width': 2}}
    load_engine_type = {'message_text': 'Тип двигателя', 'buttons': {'load_engine_hybrid': 'Гибрид', 'load_engine_DWS': 'ДВС', 'load_engine_electro': 'Электро', 'width': 2}}
    load_commodity_brand = {'message_text': 'Марка', 'buttons': {'load_brand_bmw': 'BMW', 'load_brand_mercedes': 'Mercedes', 'load_brand_renault': 'Renault', 'load_brand_skoda': 'Skoda', 'width': 2}}
    load_commodity_model = {'message_text': 'Модель', 'buttons': {'load_model_1': 'model_1', 'load_model_2': 'model_2', 'load_model_3': 'model_3', 'load_model_4': 'model_4', 'width': 2}}
    load_commodity_complectation = {'message_text': 'Комплектация', 'buttons': {'load_complectation_1': 'complectation_1', 'load_complectation_2': 'complectation_2', 'load_complectation_3': 'complectation_3', 'load_complectation_4': 'complectation_4', 'width': 2}}

    load_commodity_year_of_realise = {'message_text': 'Год выпуска', 'buttons': {'load_year_2005': '2005', 'load_year_2020': '2020', 'load_year_2015': '2015', 'load_year_2001': '2001', 'width': 2}}
    load_commodity_mileage = {'message_text': 'Пробег', 'buttons': {'load_mileage_25000': '25000', 'load_mileage_50000': '50000', 'load_mileage_100000': '100000', 'load_mileage_35000': '35000', 'width': 2}}
    load_commodity_color = {'message_text': 'Цвет', 'buttons': {'load_color_black': 'Чёрный', 'load_color_red': 'Красный', 'load_color_pink': 'Розовый', 'load_color_white': 'Белый', 'width': 2}}
    load_commodity_price = {'message_text': 'Сумма', 'buttons': {'return_main_menu': 'В меню', 'width': 1}}
    load_commodity_photo = {'message_text': 'Пришлите фото автомобиля', 'buttons': {'return_main_menu': 'В меню', 'width': 1}}


    config_for_seller = 'Ваши конфигурации:'
    config_for_admins = 'Заявка от продавца @'

    seller_notification = {'message_text': 'Заявка №_ создана!'}

    
    @classmethod
    async def get_output_string(cls, mode, boot_data: dict) -> str:
        '''Метод создаёт строку для вывода выбранных конфигураций загружаемого авто продавцу/админам.'''
        if mode == 'to_seller':
            start_sub_string = cls.config_for_seller
        elif mode.startswith('to_admins_from_'):
            seller_link = mode.split('_')[3]
            start_sub_string = cls.config_for_admins + seller_link

        bottom_layer = f'''{cls.load_commodity_price['message_text']}: {boot_data['price']}\
            \n{boot_data.get('photo_id')}\n{boot_data.get('photo_unique_id')}'''

        top_layer = f'''{start_sub_string}\
            \n{cls.load_commodity_state['message_text']}: {boot_data['state']}\
            \n{cls.load_engine_type['message_text']}: {boot_data['engine_type']}\
            \n{cls.load_commodity_brand['message_text']}: {boot_data['brand']}\
            \n{cls.load_commodity_model['message_text']}: {boot_data['model']}\
            \n{cls.load_commodity_complectation['message_text']}: {boot_data['complectation']}\n'''

        is_second_hand = (boot_data['year_of_release'], boot_data['mileage'], boot_data['color'])
        if None not in is_second_hand:
            middle_layer = f'''{cls.load_commodity_year_of_realise['message_text']}: {boot_data['year_of_release']}\
                \n{cls.load_commodity_mileage['message_text']}: {boot_data['mileage']}\
                \n{cls.load_commodity_color['message_text']}: {boot_data['color']}\n'''
            output_load_commodity_config = top_layer + middle_layer + bottom_layer
        else:
            output_load_commodity_config = top_layer + bottom_layer

        return output_load_commodity_config

    @classmethod
    async def create_notification_for_seller(cls, request_number) -> str:
        '''Плашка "Заявка №XXXX Создана"'''
        create_request_notification= cls.seller_notification['message_text']
        create_request_notification = create_request_notification.split('_')
        create_request_notification = f'{request_number}'.join(create_request_notification)

        return create_request_notification

