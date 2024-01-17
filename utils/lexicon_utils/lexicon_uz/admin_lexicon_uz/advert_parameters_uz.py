from utils.lexicon_utils.lexicon_uz.admin_lexicon_uz.admin_lexicon_uz import return_main_menu_uz, captions_uz

advert_parameters_captions_uz = {
    'year': 'Yil', 'mileage': 'Yurgan masofasi', 'color': 'Rang', 'complectation': 'Komplektatsiya', 'model': 'Model',
    'brand': 'Brend', 'state': 'Holati', 'engine': 'Dvigatel', 'from_param_branch': ' parametrlar filialidan:\n{param_branch}\n'
}

ADVERT_PARAMETERS_LEXICON_UZ = {
    'memory_was_forgotten': 'Boshidan boshlash',
    'selected_new_car_params_pattern': '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n{params_data}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n',
    'this_advert_parameter_dont_can_was_deleting': 'Tanlangan xususiyat o‘chirib bo‘lmaydi, chunki unga e’lonlar ro‘yxatdan o‘tgan!',

    'choose_second_hand_parameter_type': {'message_text': 'B/U avtomobillar parametrlari:', 'buttons': {
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
    'start_add_new_advert_parameter_value_new_state_buttons': {
        'admin_backward:await_input_new_parameter_value': captions_uz['backward'],
        'admin_backward:go_to_choose_params_state': 'Tanlashni boshiga qaytish',
        'width': 1},


    'start_add_new_advert_parameter_value(exists)': 'Parametr qo‘shish\nKiritilgan qiymat allaqachon mavjud: {parameter_name}, noyob qiymat kiriting:',
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
    'message_text': 'Tahrirlash.\nParametr uchun yangi qiymatni kiriting:\n{parameter_type}: {parameter_value}',
    'buttons': {
        'admin_backward:start_rewrite_exists_parameter_value': captions_uz['backward'],
        'width': 1
    }},
'start_rewrite_exists_parameter(exists)': 'Tahrirlash.\nKiritilgan qiymat allaqachon tanlangan parametrda mavjud: {parameter_type}',

'confirmation_rewrite_exists_parameter': {
    'message_text': 'Siz rostdan ham parametr qiymatini tahrirlamoqchimisiz: {parameter_type}\nEski: {parameter_old_value}\nYangi: {parameter_new_value} ?',
    'buttons': {'confirm_rewrite_existing_advert_parameter': captions_uz['confirm'],
                'rewrite_current_advert_parameter': 'Qayta kiriting',
                'admin_backward:rewrite_exists_advert_param': captions_uz['backward'],
                'width': 1}
},
'input_photos_to_load_param_branch': {'message_text': 'Avtomobilning kiritilgan xususiyatlariga mos keladigan 3-5 ta fotosuratni yuboring:',
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
    'car_parameters_message_text': 'Avtomobillar parametrlari.\nHolatni tanlang:',
    'rewrite_current_advert_parameter': 'Tahrirlash',
    'backward': '◂ Orqaga ▸',
    'delete': 'O‘chirish',
    'add': 'Qo‘shish',
    'return_main_menu': 'Menyuda',
    'translate_param_caption': '<blockquote>DIQQAT! Rus tilidagi sarlavhalar o‘zbek tili foydalanuvchilari uchun tarjima qilinadi.</blockquote>\n'
}

advert_params_captions_uz = {
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