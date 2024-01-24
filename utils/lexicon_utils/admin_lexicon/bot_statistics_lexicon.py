from copy import copy

from utils.lexicon_utils.admin_lexicon.advert_parameters_lexicon import advert_parameters_captions
from utils.safe_dict_class import SafeDict

return_main_menu = {'return_main_menu': 'В меню'}
pagination_interface = {'admin_pagination:-': '←', 'page_counter': '[{start}/{end}]', 'admin_pagination:+': '→'}
captions = {'backward': '◂ Назад ▸', 'was_selected': 'Вы выбрали', 'cancel': 'Отменить', 'confirm': 'Подтвердить',
            'sales': 'продажам', 'purchases': 'покупкам', 'any': 'всё время', 'day': 'день', 'week': 'неделю',
            'month': 'месяц', 'year': 'год', 'days': 'дней', 'feedbacks': 'откликов',
            'dont_write_html_tags': 'Запрещён ввод знаков "&lt; &gt;".',
            'all_users': 'всех', 'buyers': 'покупателей', 'sellers': 'продавцов', 'delete': 'Удалить',
            'by_dealership': 'автосалона',
            'by_seller': 'частного лица', 'close': 'Скрыть', 'surname_name_patronymic': 'ФИО: ', 'add': 'Добавить',
            'successfully': 'Успешно'
            }

statistic_captions = {'Day': 'День',
                    'Week': 'Неделя',
                    'Month': 'Месяц',
                    'Year': 'Год',
                    'General': 'Общая',
                      'color': 'Цвет',
                      'complectation': 'Комплектацию',
                      'model': advert_parameters_captions['model'],#.lower(),
                      'brand': advert_parameters_captions['brand'],#.lower(),
                      'engine': advert_parameters_captions['engine'],#.lower(),
                    'top_demand_on': '<b>Топ спроса за {period}</b>',
                    'car': 'авто',
                    'individual_stats': 'индивидуальной статистики',
                    'top_10_stats': 'топ 10',
                      'bottom_demand_start': 'низкого',
                      'top_demand_start': 'высшего',
                      'for_current_period': 'по текущему периоду'
}

choose_period_keyboard = {'select_bot_statistic_period:day': statistic_captions['Day'],
                          'select_bot_statistic_period:week': statistic_captions['Week'],
                           'select_bot_statistic_period:month': statistic_captions['Month'],
                           'select_bot_statistic_period:year': statistic_captions['Year'],
                           'select_bot_statistic_period:all': statistic_captions['General']}

to_statistic_panel = {'admin_backward:to_statistic_panel': 'В меню статистики'}

__STATISTIC_LEXICON = {
    'stats_is_empty': 'Статистика {for_current_period} пуста',
    'stats_loading': 'Производится расчёт статистики...',
    'seller_statistic_view': {
    'message_text': "<b>Статистика за {period}:</b>\n" + (' ' * 13 + '─' * 8) + "\nПродавец: <i>{seller_name}</i>\nДата регистрации: <i>{date_of_registration}</i>\nКоличество объявлений: {adverts_count}\nКоличество откликов: {feedbacks_count}\n" + (' ' * 13 + '─' * 12),
        'buttons': {'select_seller_statistic_period:day': statistic_captions['Day'],
                    'select_seller_statistic_period:week': statistic_captions['Week'],
                    'select_seller_statistic_period:month': statistic_captions['Month'],
                    'select_seller_statistic_period:year': statistic_captions['Year'],
                    'select_seller_statistic_period:all': statistic_captions['General'],
                    'admin_backward:check_seller_statistic_values': captions['backward'],
                    **return_main_menu, 'width': (3, 2, 1, 1)}},

    'choose_statistic_type': {
        'message_text': '<b>Выберите тип статистики по боту:</b>', 'buttons': {'general_statistics': '📊 Общая статистика',
                                                               'demand_for_cars': '📉 Спрос на авто',
                                                               **return_main_menu,
                                                               'width': 1}
    },

    'general_bot_statistics': {'message_text': '<b>Статистика за {period}</b>\n' + (' ' * 17 + '─' * 8) + '\n<blockquote>🔸Откликов: {feedbacks}\n📢 Объявлений: {adverts}\
\n🧖‍♂️ Пользователей в боте: {users}\n🤵🏻‍♂️ Продавцов: {sellers}\n👨🏻‍💻 Покупателей: {buyers}</blockquote>\n' + (' ' * 17 + '─' * 8), 'buttons': {
                    **choose_period_keyboard,
                    'admin_backward:check_bot_statistic_values': captions['backward'],
                    **return_main_menu, 'width': (3, 2, 1, 1)}},

    'choose_statistics_output_method': {'message_text': '<b>Выберите метод вывода статистики:</b>', 'buttons': {
        'output_method:top_ten': 'Топ 10  👑', 'output_method:individual': '🧑🏽‍🦱 Индивидуально',
        #'admin_backward:statistics_output_method': captions['backward'],
        **to_statistic_panel,
        'width': 2
    }},
    'choose_method_of_calculating': {'message_text': '<b>Выберите метод расчёта статистики спроса:</b>', 'buttons': {
        'calculate_method:top': 'Высший спрос 📈', 'calculate_method:bottom': '📉 Низший спрос',
        'admin_backward:method_of_calculate': captions['backward'],
        **to_statistic_panel,
        'width': 2
    }},

    'top_ten_message_text':  '<b>Вывод от самого {demand_direction} по спросу</b>\nМесто в топе: {top_position}\nОткликов за {period}: {feedback_count}{parameters}\n<b>Самый продуктивный продавец этой машины:</b>\n<blockquote>{seller_entity}</blockquote>\n' \
                        + ('─' * 15) + '\n<b>Машины подписаны своим местом в топе:</b>',

    'custom_params_period': {'message_text': '<b>Период расчёта {output_method} спроса:</b>',
                             'buttons': {
                                 **choose_period_keyboard,
                                 'admin_backward:custom_params_period': captions['backward'],
                                 **to_statistic_panel,
                                 'width': 3
                             }},

    'review_custom_stats_branches': {'message_text': '', 'buttons': {
        **pagination_interface,
        'admin_backward:choose_custom_params': captions['backward'],
        **to_statistic_panel,
        'width': 3
    }}
}

statistic_class_lexicon_ru = {
    'select_custom_params_process_message_text': 'Топ спроса на {object_entity}\nза {period}\nСписок по убыванию от самой {popular_state} {param_type}:',
    'output_current_top_buttons': 'Вывести текущий топ',
    'choose_custom_params_to_stats_message_text': '{header}\nСписок {demand_order} спроса;\n<b>Выберите параметр: {param}:</b>',
    'backward': '◂ Назад ▸',
    'to_statistic_panel': 'В меню статистики',
    'by_more': 'по увеличению',
    'by_low': 'по убыванию'
}

# Добавление в узбекский словарь
statistic_class_lexicon_uz = {
    'select_custom_params_process_message_text': '{object_entity} bo‘yicha eng ko‘p talab\n{period} davomida\n{param_type} bo‘yicha kamayish tartibida ro‘yxatlanadi:',
    'output_current_top_buttons': 'Joriy topni chiqarish',
    'choose_custom_params_to_stats_message_text': '{header}\nTalabning {demand_order} tartibidagi ro‘yxati;\n<b>Variantni tanlang: {param}:</b>',
    'backward': '◂ Orqaga ▸',
    'to_statistic_panel': 'Statistika menyusida',
    'by_more': "o'sish bilan",
    'by_low': "pasaytiruvchi"
}

statistic_class_lexicon = SafeDict({'ru': statistic_class_lexicon_ru,
                                    'uz': statistic_class_lexicon_uz})




class SelectCustomParamsProcess:
    def __init__(self):
        self.message_text = statistic_class_lexicon['select_custom_params_process_message_text']  # Или lexicon_uz для узбекской версии
        self.width = 1
        self.backward_buttons = {'admin_backward:select_custom_params': statistic_class_lexicon['backward'],
                                    'admin_backward:to_statistic_panel': statistic_class_lexicon['to_statistic_panel']}
        self.buttons_callback_data = 'bot_statistic_param:'
        self.output_current_top_buttons = {'output_current_top': statistic_class_lexicon['output_current_top_buttons']}


class TopTenDisplay:
    def __init__(self):
        self.buttons_callback_data = 'ttp:'
        self.backward_command = {'admin_backward:top_ten_display': statistic_class_lexicon['backward'],
                            'admin_backward:to_statistic_panel': statistic_class_lexicon['to_statistic_panel']}
        self.width = 1
        self.dynamic_buttons = 2


class ChooseCustomParamsToStats:
    def __init__(self, period, param_to_output, calculate_method, chosen_params=None):
        self.buttons_callback_data = 'custom_demand_param:'
        self.backward_command = {'admin_backward:choose_custom_params': statistic_class_lexicon['backward'],
                            'admin_backward:to_statistic_panel': statistic_class_lexicon['to_statistic_panel']}
        self.output_top_button = {'output_current_demand_stats': statistic_class_lexicon['output_current_top_buttons']}
        self.width = 1
        self.dynamic_buttons = 2

        self.dynamic_buttons = self.dynamic_buttons if param_to_output == 'engine' else 3
        self.message_text = statistic_class_lexicon['choose_custom_params_to_stats_message_text'].format(
            header='{header}',
            demand_order=statistic_class_lexicon['by_low'] if calculate_method == 'bottom' else statistic_class_lexicon['by_more'],
            param=advert_parameters_captions[param_to_output]
        )

        if chosen_params:
            self.backward_command = {**self.output_top_button, **self.backward_command}
        else:
            self.backward_command = self.backward_command

SelectCustomParamsProcess = SelectCustomParamsProcess()
TopTenDisplay = TopTenDisplay()