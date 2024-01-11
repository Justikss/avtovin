from utils.lexicon_utils.admin_lexicon.admin_lexicon import return_main_menu, captions

statistic_captions = {'Day': 'День',
                    'Week': 'Неделя',
                    'Month': 'Месяц',
                    'Year': 'Год',
                    'General': 'Общая'}

choose_period_keyboard = {'select_bot_statistic_period:day': statistic_captions['Day'],
                          'select_bot_statistic_period:week': statistic_captions['Week'],
                           'select_bot_statistic_period:month': statistic_captions['Month'],
                           'select_bot_statistic_period:year': statistic_captions['Year'],
                           'select_bot_statistic_period:all': statistic_captions['General']}

to_statistic_panel = {'admin_backward:to_statistic_panel': 'В меню статистики'}

__STATISTIC_LEXICON = {
    'stats_loading': 'Производится расчёт статистики...',
    'seller_statistic_view': {
    'message_text': "Продавец: {seller_name}\nДата регистрации: {date_of_registration}\n\nСтатистика за {period}:\nКоличество объявлений: {adverts_count}\nКоличество откликов: {feedbacks_count}",
        'buttons': {'select_seller_statistic_period:day': statistic_captions['Day'],
                    'select_seller_statistic_period:week': statistic_captions['Week'],
                    'select_seller_statistic_period:month': statistic_captions['Month'],
                    'select_seller_statistic_period:year': statistic_captions['Year'],
                    'select_seller_statistic_period:all': statistic_captions['General'],
                    'admin_backward:check_seller_statistic_values': captions['backward'],
                    **return_main_menu, 'width': (3, 2, 1, 1)}},

    'choose_statistic_type': {
        'message_text': 'Тип статистики по боту:', 'buttons': {'general_statistics': 'Общая статистика',
                                                               'demand_for_cars': 'Спрос на авто',
                                                               **return_main_menu,
                                                               'width': 1}
    },

    'general_bot_statistics': {'message_text': 'Статистика за {period}\n' + ('▬' * 13) + '\n🔸Откликов: {feedbacks}\n📢 Объявлений: {adverts}\
\n🧖‍♂️ Пользователей в боте: {users}\n🤵🏻‍♂️ Продавцов: {sellers}\n👨🏻‍💻 Покупателей: {buyers}', 'buttons': {
                    **choose_period_keyboard,
                    'admin_backward:check_bot_statistic_values': captions['backward'],
                    **return_main_menu, 'width': (3, 2, 1, 1)}},

    'choose_statistics_output_method': {'message_text': 'Выберите метод вывода статистики:', 'buttons': {
        'output_method:top_ten': 'Топ 10', 'output_method:individual': 'Индивидуально',
        'admin_backward:statistics_output_method': captions['backward'],
        **to_statistic_panel,
        'width': 2
    }},
    'choose_method_of_calculating': {'message_text': 'Выберите метод расчёта статистики спроса:', 'buttons': {
        'calculate_method:top': 'Высший спрос', 'calculate_method:bottom': 'Низший спрос',
        'admin_backward:method_of_calculate': captions['backward'],
        **to_statistic_panel,
        'width': 2
    }},

    'period_of_calculate_demand_statistics': {'message_text': 'Период расчёта статистики:', 'buttons': {
        **choose_period_keyboard,
        'admin_backward:period_of_calcul_demand_stats': captions['backward'],
        **to_statistic_panel,
        'width': (3, 2, 1, 1)
    }},
    'top_ten_message_text':  'Место в топе: {top_position}{parameters}\n\nСамый продуктивный продавец этой машины:\n<blockquote>{seller_entity}</blockquote>\n' \
                        + ('▬' * 13) + '\nМашины подписаны своим местом в топе:'
}

class SelectCustomParamsProcess:
    message_text = 'Топ спроса на {object_entity}\nза {period}\nСписок по убыванию от самой {popular_state} {param_type}:'
    width = 1
    backward_buttons = {'admin_backward:select_custom_params': captions['backward'], **to_statistic_panel}
    buttons_callback_data = 'bot_statistic_param:'

    output_current_top_buttons = {'output_current_top': 'Вывести текущий топ'}


class TopTenDisplay:
    # message_text =

    buttons_callback_data = 'top_ten_params:'
    backward_command = {'admin_backward:top_ten_display': captions['backward'], **to_statistic_panel}
    width = 1
    dynamic_buttons = 2
