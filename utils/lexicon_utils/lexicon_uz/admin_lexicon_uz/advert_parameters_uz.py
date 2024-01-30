from utils.lexicon_utils.lexicon_uz.admin_lexicon_uz.admin_lexicon_uz import return_main_menu_uz, captions_uz

max_advert_parameter_name_len = 150
max_integer_for_database = 2147483647

advert_parameters_captions_uz = {
    'year': 'Yil', 'mileage': 'Yurgan masofasi', 'color': 'Rang', 'complectation': 'Komplektatsiya', 'model': 'Model',
    'brand': 'Brend', 'state': 'Holati', 'engine': 'Dvigatel', 'from_param_branch': ' parametrlar filialidan:\n{param_branch}\n'
}

ADVERT_PARAMETERS_LEXICON_UZ = {
    'memory_was_forgotten': 'Boshidan boshlash',
    'selected_new_car_params_pattern': '───────────────\n<blockquote>{params_data}</blockquote>\n───────────────\n',
    'this_advert_parameter_dont_can_was_deleting': 'Tanlangan xususiyat o‘chirib bo‘lmaydi, chunki unga e’lonlar ro‘yxatdan o‘tgan!',

    'choose_second_hand_parameter_type': {'message_text': 'Ishlatilgan avtomobillarning parametrlari:', 'buttons': {
        'second_hand_choice_advert_parameters_type_mileage': 'Yurgan masofasi', 'second_hand_choice_advert_parameters_type_year': 'Yil',
        'admin_backward:choose_second_hand_advert_parameters_type': captions_uz['backward'],
        **return_main_menu_uz,
        'width': 2
    }},

    'start_add_new_advert_parameter_value': {'message_text': 'Parametr qo‘shish\nParametr uchun yangi qiymat kiriting: {parameter_name}',
                                             'buttons': {
                                                 'admin_backward:await_input_new_parameter_value': captions_uz['backward'],
                                                 'width': 1
                                             }},

    'start_add_new_advert_parameter_value(text_symbols)': "Parametr qo'shish: {parameter_name}.\n<b>Iltimos, to'g'ri nomni kiriting.\nSiz kiritishingiz mumkin: Raqamlar, harflar, va belgilar (raqamlar yoki harflar mavjud bo'lganda):</b>",
    'start_add_new_advert_parameter_value(year_len)': "Parametr qo'shish: {parameter_name}.\n<b>Iltimos, hozirgi yildan oshmaydigan oralig'ini kiriting, uzunligi 9 belgigacha.\nMisol: 2019-2020:</b>",
    'start_add_new_advert_parameter_value(symbols)': "Parametr qo'shish: {parameter_name}.\n<b>Iltimos, raqamlardan boshlanib, to'g'ri ijobiy oralig'ini kiriting. Qo'shimcha ravishda kiritish mumkin: bir dona plus belgisi (oxirida) yoki chiziq va oltigacha nuqta:</b>",


    'start_add_new_advert_parameter_value(int_len)': "Parametr qo'shish\n<b>Kiritilgan raqam {max_integer_for_database} qiymatidan oshmasligi kerak:</b>\nParametr uchun yangi qiymat kiriting: {parameter_name}".format(max_integer_for_database=max_integer_for_database, parameter_name='{parameter_name}'),
    'start_add_new_advert_parameter_value(len)': 'Parametr qo‘shish\n<b>Kiritilgan qiymat uzunligi {max_advert_parameter_name_len} harfdan oshmasligi kerak:</b>\nParametr uchun yangi qiymat kiriting: {parameter_name}'.format(max_advert_parameter_name_len=max_advert_parameter_name_len, parameter_name='{parameter_name}'),
    'start_add_new_advert_parameter_value_new_state_buttons': {
        'admin_backward:await_input_new_parameter_value': captions_uz['backward'],
        'admin_backward:go_to_choose_params_state': 'Tanlashni boshiga qaytish',
        'width': 1},


    'start_add_new_advert_parameter_value(exists)': 'Parametr qo‘shish\n<b>Kiritilgan qiymat allaqachon mavjud: {parameter_name}, noyob qiymat kiriting:</b>',
    # 'start_add_new_advert_parameter_value': '',

    'confirmation_add_new_advert_parameter_value': {
        'message_text': 'Qo‘shmoqchimisiz:\n{parameter_name}: {new_parameter_value} ?',
        'buttons': {
            'confirm_action_add_new_parameter_value': captions_uz['confirm'],
            'admin_backward:confirmation_add_new_parameter_value_rewrite': 'Qayta kiriting',
            'admin_backward:confirmation_add_new_parameter_value_cancel': captions_uz['cancel'],
            'width': 1
        }},

    'choose_action_on_specific_parameter_value': {
        'message_text': 'Tanlangan parametr:\n{parameter_name}: {parameter_value}', 'buttons': {
            'delete_current_advert_parameter': captions_uz['delete'], 'rewrite_current_advert_parameter': 'Tahrirlash',
'admin_backward:choose_action_on_specific_adv_parameter': captions_uz['backward'],
**return_main_menu_uz,
'width': 2
}},
'confirmation_to_delete_exists_parameter': {
'message_text': 'Tanlangan parametrni o‘chirishni tasdiqlang{from_param_branch}\nParametr:\n{parameter_type_to_parameter_value}', 'buttons': {
'confirm_delete_advert_parameter': captions_uz['confirm'],
'admin_backward:confirmation_delete_advert_param': captions_uz['backward'],
**return_main_menu_uz,
'width': 1
}
},
'start_rewrite_exists_parameter': {
    'message_text': '<b>Tahrirlash.</b>\n────────\nParametr uchun yangi qiymatni kiriting: {parameter_type}.\nJoriy sozlama: <b>{parameter_value}</b>\n────────',
    'buttons': {
        'admin_backward:start_rewrite_exists_parameter_value': captions_uz['backward'],
        'width': 1
    }},
'start_rewrite_exists_parameter(text_symbols)': "Parametrni tahrirlash: {parameter_type}.\n<b>Iltimos, to'g'ri nomni kiriting.\nSiz kiritishingiz mumkin: Raqamlar, harflar, va belgilar (raqamlar yoki harflar mavjud bo'lganda):</b>",
'start_rewrite_exists_parameter(year_len)': "Parametrni tahrirlash: {parameter_type}.\n<b>Iltimos, hozirgi yildan oshmaydigan oralig'ini kiriting, uzunligi 9 belgigacha.\nMisol: 2019-2020:</b>",
'start_rewrite_exists_parameter(symbols)': "Parametrni tahrirlash: {parameter_type}.\n<b>Iltimos, raqamlardan boshlanib, to'g'ri ijobiy oralig'ini kiriting. Qo'shimcha ravishda kiritish mumkin: bir dona plus belgisi (oxirida) yoki chiziq va oltigacha nuqta:</b>",

'start_rewrite_exists_parameter(len)': 'Parametrni tahrirlash: {0}.\n<b>Kiritilgan qiymat uzunligi {1} harfdan oshmasligi kerak.</b>'.format('{parameter_type}', max_advert_parameter_name_len),
'start_rewrite_exists_parameter(exists)': 'Tahrirlash.\nKiritilgan qiymat allaqachon tanlangan parametrda mavjud: {parameter_type}',
'start_rewrite_exists_parameter(int_len)': 'Parametrni tahrirlash: {0}.\n<b>Kiritilgan raqam {1} qiymatidan oshmasligi kerak:</b>'.format(
    '{parameter_type}', max_integer_for_database),

    'confirmation_rewrite_exists_parameter': {
    'message_text': 'Siz rostdan ham parametr qiymatini tahrirlamoqchimisiz: {parameter_type}\nEski: {parameter_old_value}\nYangi: {parameter_new_value} ?',
    'buttons': {'confirm_rewrite_existing_advert_parameter': captions_uz['confirm'],
                'rewrite_current_advert_parameter': 'Qayta kiriting',
                'admin_backward:rewrite_exists_advert_param': captions_uz['backward'],
                'width': 1}
},
'input_photos_to_load_param_branch': {'message_text': 'Avtomobilning suratini yuboring\n(klips ramzini chatning chap burchagida)\n\n(!5 dan 8 gacha namunalar!)\n\nTelegramda surat yuborishda siqishni bekor qilmang.',
                                      'buttons': {
                                          'admin_backward:await_input_new_parameter_value': captions_uz['backward'],
                                          'width': 1
                                      }},
'load_new_params_branch_confirmation': {
    'message_text': 'Yangi avto parametrlar filialini yuklashni tasdiqlashni kutish:', 'buttons': {
                                    'confirm_load_new_params_branch': captions_uz['confirm'],
                                    'update_params_branch_media_group': 'Fotolarni yangilash',
                                     'admin_backward:review_params_branch_to_load': captions_uz['backward'],
                                     'admin_backward:go_to_choose_params_state': 'Tanlashni boshiga qaytish',
                                     **return_main_menu_uz,
                                     'width': 1
    }},
'review_params_branch': {'message_text': '',
                         'buttons': {'rewrite_current_advert_parameter': 'Tahrirlash',
                                     'update_params_branch_media_group': 'Fotolarni yangilash',
                                     'delete_current_advert_parameter': captions_uz['delete'],
                                     'admin_backward:review_params_branch': captions_uz['backward'],
                                     'admin_backward:go_to_choose_params_state': 'Tanlashni boshiga qaytish',
                                     **return_main_menu_uz,
                                     'width': 1}}
}


# Добавление в узбекский словарь
advert_params_class_lexicon_uz = {
    'new_car_state_parameters_caption': "<b>Avtomobil qo'shish</b>\n",
    'car_parameters_start': {'message_text': '<b>Avtomobil parametr turini tanlang:</b>', 'buttons': {
        "advert_parameters_choose_state:2": "foydl. avtomobillar konfigi", 'advert_parameters_choose_state:1': "Avtomobil qo'shing",
        'admin_backward:advert_parameters_choose_state': '◂ Orqaga ▸',
        'return_main_menu': 'Menyuda',
        'width': 2}},
    'rewrite_current_advert_parameter': 'Tahrirlash',
    'backward': '◂ Orqaga ▸',
    'delete': 'O‘chirish',
    'add': 'Qo‘shish',
    'return_main_menu': 'Menyuda',
    'translate_param_caption': '<blockquote><b>Rus tilidagi sarlavhalar oʻzbek tili foydalanuvchilari uchun avtomatik tarzda tarjima qilinadi</b></blockquote>\n'
}

advert_params_captions_uz = {
    'choose_param': '<b>Avtomatik {parameter} ni tanlang</b>',
    'year': 'Yili',
    'mileage': 'Yurgan masofa',
    'color': 'Rang',
    'complectation': 'Komplektatsiya',
    'model': 'Model',
    'brand': 'Brend',
    'state': 'Holati',
    'engine': 'Dvigatel',
    'from_param_branch': ' parametr shoxobchasidan:\n{param_branch}\n',
    'year_of_realise': 'Chiqarilgan yili'
}