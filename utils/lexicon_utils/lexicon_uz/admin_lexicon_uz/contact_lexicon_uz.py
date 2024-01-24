return_main_menu = {'return_main_menu': 'Menyuga'}

ADMIN_CONTACTS_UZ = {
    'new_contact_caption_telegram': 'Yangi havola',
    'new_contact_caption_number': 'Yangi telefon raqami',
    'last_contact_caption_telegram': 'Oldingi havola',
    'last_contact_caption_number': 'Oldingi telefon raqami',
    'contact_type_telegram': 'Havola',
    'contact_type_number': 'Raqam',

    'contact_id_was_not_found': 'Kontakt ID topilmadi.',
    'successfully': 'Muvaffaqiyatli',
    'contact_type_or_id_was_not_found': 'Kontakt turi yoki uning ID aniqlanmadi',
    'contact_type_was_not_found': 'Kontakt turi aniqlanmadi',
    'link_name:telegram': 'Telegram foydalanuvchi nomi (@ belgisidan boshlab)',
    'link_name:number': 'Telefon raqami',
    'contact_was_not_found': 'Kontakt topilmadi',
    'telegram': 'Telegram',
    'number': 'Telefon raqami',
    'return_main_menu': 'Menyuga',
    'backward': 'Orqaga',
    'add': 'Qo\'shish',
    'active_contact_list': 'Faol kontaktlar ro\'yxati:',
    'choose_type': {'message_text': '<b>Texnik yordam kontakti turini tanlang:</b>', 'buttons': {
        'ts_contact_type:number': '📞 Telefon raqami', 'ts_contact_type:telegram': '📨 Telegram',
        **return_main_menu,
        'width': 1
    }},
    'output_contact': {'message_text': '''<b>Texnik yordam kontakti:</b>
───────────────
Kategoriya: <b>{contact_entity}</b>
{contact_type}: <b>{contact}</b>
───────────────''',
                       'delete_ts_contact': 'O\'chirish', 'edit_ts_contact': 'O\'zgartirish',
                       'admin_backward:review_profile': 'Kontaktlar', 'admin_backward:to_type_contacts': 'Kontakt turlariga',
                       'width': 2},
    'add_new_contact': {'message_text': '<b>Texnik yordam kontaktini qo\'shish:</b>\nYangi kontaktning {link} kiriting:', 'buttons': {
        'admin_backward:start_add_new_contact': 'Orqaga',
        'width': 1
    }},
    'add_new_contact:number': '\n<blockquote>Telefon raqamining to\'g\'ri formatida</blockquote>',
    'add_new_contact:@': '',
    'add_new_contact:@@': "\n<blockquote>' @ ' belgisi bitta nusxada bo'lishi kerak</blockquote>",

    'add_new_contact:exists':  '\n<blockquote>Kiritilgan kontakt allaqachon mavjud.</blockquote>',
    'add_new_contact:symbols':  '\n<blockquote>100 belgidan ko\'p emas.</blockquote>',

    'confirmation_add_contact': {'message_text': '<b>Texnik yordam kontaktini qo\'shish:</b>\n───────────────\nKategoriya: <b>{contact_entity}</b>\n{contact_type}: <b>{contact}</b>\n───────────────',
                                 'buttons': {
                                     'confirm_add_ts_contact': 'Tasdiqlash',
                                     'rewrite_ts_contact_link': 'Qayta yozish',
                                     'admin_backward:confirmation_add_new_ts': 'Bekor qilish',
                                     'width': 1
                                 }},
    'start_delete_contact': {'message_text': '<b>Texnik yordam kontaktini o\'chirish:</b>\n───────────────\nKategoriya: <b>{contact_entity}</b>\n{contact_type}: <b>{contact}</b>\n───────────────', 'buttons': {
        'confirm_delete_contact': 'Tasdiqlash',
        'admin_backward:start_delete_ts_contact': 'Orqaga',
        'width': 1
    }},

    'start_rewrite_exists_contact': {'message_text': '<b>Tahrirlash</b>:\n───────────────\nKategoriya: <b>{entity}</b> \n{contact_type}: <b>{cur_link}</b>\n───────────────\n<b>Yangi {link} kiriting:</b>',
                                     'buttons': {'admin_backward:start_rewrite_ts_contact': 'Orqaga',
                                                 'width': 1}},

    'start_rewrite_exists_contact:number': '\n<blockquote>Telefon raqamining to\'g\'ri formatida</blockquote>',
    'start_rewrite_exists_contact:@': '',
    'start_rewrite_exists_contact:exists': '\n<blockquote>Kiritilgan kontakt allaqachon mavjud.</blockquote>',
    'start_rewrite_exists_contact:symbols': '\n<blockquote>100 belgidan ko\'p emas.</blockquote>',

    'confirmation_rewrite_exist_contact': {'message_text': '<b>Tahrirlash</b>:\n───────────────\nKategoriya: <b>{entity}</b> \n{last_contact_caption}: <b>{cur_link}</b>\n{new_link_caption}: <b>{new_link}</b>\n───────────────\n', 'buttons': {
        'confirm_rewrite_ts_contact': 'Tasdiqlash',
        'rewrite_rewriting_ts_contact': 'Qaytadan kiriting',
        'admin_backward:confirmation_rewrite_ts': 'Bekor qilish',
        'width': 1
    }},
}
