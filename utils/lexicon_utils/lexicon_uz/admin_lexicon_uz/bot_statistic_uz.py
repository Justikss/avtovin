from utils.lexicon_utils.lexicon_uz.admin_lexicon_uz.advert_parameters_uz import advert_parameters_captions_uz

return_main_menu_uz = {'return_main_menu': 'Menyuga'}
captions_uz = {'backward': 'Orqaga', 'was_selected': 'Siz tanladingiz', 'cancel': 'Bekor qilish', 'confirm': 'Tasdiqlash',
            'sales': 'sotishlar', 'purchases': 'xaridlar', 'any': 'har doim', 'day': 'kun', 'week': 'hafta',
            'month': 'oy', 'year': 'yil', 'days': 'kunlar', 'feedbacks': 'javoblar',
            'dont_write_html_tags': '"&lt; &gt;" belgilarini kiriting taqiqlanadi.',
            'all_users': 'barcha', 'buyers': 'xaridorlar', 'sellers': 'sotuvchilar', 'delete': 'O‘chirish',
            'by_dealership': 'avtosalon', 'by_seller': 'shaxsiy shaxs', 'close': 'Yashirish', 'surname_name_patronymic': 'F.I.Sh.: ', 'add': 'Qo‘shish',
            'successfully': 'Muvaffaqiyatli'
            }
pagination_interface = {'admin_pagination:-': '←', 'page_counter': '[{start}/{end}]', 'admin_pagination:+': '→'}


''''''

statistic_captions_uz = {'Day': 'Kun',
                    'Week': 'Hafta',
                    'Month': 'Oy',
                    'Year': 'Yil',
                    'General': 'Umumiy',
                      'color': 'Rang',
                      'complectation': 'Komplektatsiya',
                      'model': advert_parameters_captions_uz['model'],#.lower(),
                      'brand': advert_parameters_captions_uz['brand'],#.lower(),
                      'engine': advert_parameters_captions_uz['engine'],#.lower(),
                    'top_demand_on': 'Eng ko‘p talab qilingan',
                    'car': 'avto',
                    'individual_stats': 'individual statistika',
                    'top_10_stats': 'top 10'
}

choose_period_keyboard = {'select_bot_statistic_period:day': statistic_captions_uz['Day'],
                          'select_bot_statistic_period:week': statistic_captions_uz['Week'],
                           'select_bot_statistic_period:month': statistic_captions_uz['Month'],
                           'select_bot_statistic_period:year': statistic_captions_uz['Year'],
                           'select_bot_statistic_period:all': statistic_captions_uz['General']}

to_statistic_panel = {'admin_backward:to_statistic_panel': 'Statistika menyusiga'}

STATISTIC_LEXICON_UZ = {
    'stats_loading': 'Statistika hisoblanmoqda...',
    'seller_statistic_view': {
    'message_text': "Sotuvchi: {seller_name}\nRo‘yxatdan o‘tish sanasi: {date_of_registration}\n\n{period} davridagi statistika:\nE’lonlar soni: {adverts_count}\nJavoblar soni: {feedbacks_count}",
        'buttons': {'select_seller_statistic_period:day': statistic_captions_uz['Day'],
                    'select_seller_statistic_period:week': statistic_captions_uz['Week'],
                    'select_seller_statistic_period:month': statistic_captions_uz['Month'],
                    'select_seller_statistic_period:year': statistic_captions_uz['Year'],
                    'select_seller_statistic_period:all': statistic_captions_uz['General'],
                    'admin_backward:check_seller_statistic_values': captions_uz['backward'],
                    **return_main_menu_uz, 'width': (3, 2, 1, 1)}},

    'choose_statistic_type': {
        'message_text': 'Bot bo‘yicha statistika turi:', 'buttons': {'general_statistics': 'Umumiy statistika',
                                                               'demand_for_cars': 'Avtolar bo‘yicha talab',
                                                               **return_main_menu_uz,
                                                               'width': 1}
    },

    'general_bot_statistics': {'message_text': '{period} davridagi statistika\n' + ('▬' * 13) + '\n🔸Javoblar: {feedbacks}\n📢 E’lonlar: {adverts}\
\n🧖‍♂️ Bot foydalanuvchilari: {users}\n🤵🏻‍♂️ Sotuvchilar: {sellers}\n👨🏻‍💻 Xaridorlar: {buyers}', 'buttons': {
                    **choose_period_keyboard,
                    'admin_backward:check_bot_statistic_values': captions_uz['backward'],
                    **return_main_menu_uz, 'width': (3, 2, 1, 1)}},

    'choose_statistics_output_method': {'message_text': 'Statistika chiqarish usulini tanlang:', 'buttons': {
'output_method:top_ten': 'Top 10', 'output_method:individual': 'Individual',
'admin_backward:statistics_output_method': captions_uz['backward'],
**to_statistic_panel,
'width': 2
}},
'choose_method_of_calculating': {'message_text': 'Talab statistikasini hisoblash usulini tanlang:', 'buttons': {
'calculate_method:top': 'Eng yuqori talab', 'calculate_method:bottom': 'Eng past talab',
'admin_backward:method_of_calculate': captions_uz['backward'],
**to_statistic_panel,
'width': 2
}},
'top_ten_message_text':  'Topdagi o‘rni: {top_position}\n{period} davomida javoblar soni: {feedback_count}{parameters}\n\nEng samarali sotuvchi bu mashina:\n<blockquote>{seller_entity}</blockquote>\n' \
                    + ('▬' * 13) + '\nMashinalar topdagi o‘rniga ko‘ra belgilangan:',

'custom_params_period': {'message_text': '{output_method} talabini hisoblash davri:',
                         'buttons': {
                             **choose_period_keyboard,
                             'admin_backward:custom_params_period': captions_uz['backward'],
                             **to_statistic_panel,
                             'width': 3
                         }},

'review_custom_stats_branches': {'message_text': '', 'buttons': {
    **pagination_interface,
    'admin_backward:choose_custom_params': captions_uz['backward'],
    **to_statistic_panel,
    'width': 3
}}
}
