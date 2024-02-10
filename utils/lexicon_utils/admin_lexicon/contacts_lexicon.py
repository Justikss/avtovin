from utils.lexicon_utils.admin_lexicon.admin_catalog_lexicon import return_main_menu
from utils.lexicon_utils.lexicon_uz.admin_lexicon_uz.contact_lexicon_uz import ADMIN_CONTACTS_UZ
from utils.safe_dict_class import SafeDict, SmartGetattr

__ADMIN_CONTACTS_RU = {
    'new_contact_caption_telegram': 'Новая ссылка',
    'new_contact_caption_number': 'Новый телефонный номер',
    'last_contact_caption_telegram': 'Прошлая ссылка',
    'last_contact_caption_number': 'Прошлый телефонный номер',
    'contact_type_telegram': 'Ссылка',
    'contact_type_number': 'Номер',

    'contact_id_was_not_found': 'ID контакта не найдено.',
    'successfully': 'Успешно',
    'contact_type_or_id_was_not_found': 'Тип контакта или его ID не распознаны',
    'contact_type_was_not_found': 'Тип контакта не распознаны',
    'link_name:telegram': 'Telegram username (начиная с символа @)',
    'link_name:number': 'Телефонный номер',
    'contact_was_not_found': 'Контакт не найден',
    'telegram': 'Телеграм',
    'number': 'Телефонный номер',
    'return_main_menu': 'В меню',
    'backward': 'Назад',
    'add': 'Добавить',
    'active_contact_list': 'Список активных контактов:',
    'choose_type': {'message_text': '<b>Выберите тип контакта технической поддержки:</b>', 'buttons': {
        'ts_contact_type:number': '📞 Телефонный номер', 'ts_contact_type:telegram': '📨 Телеграм',
        **return_main_menu,
        'width': 1
    }},
    'output_contact': {'message_text': '''<b>Контакт технической поддержки:</b>
───────────────
Категория: <b>{contact_entity}</b>
{contact_type}: <b>{contact}</b>
───────────────''',
                       'delete_ts_contact': 'Удалить', 'edit_ts_contact': 'Изменить',
                       'admin_backward:review_profile': 'Контакты', 'admin_backward:to_type_contacts': 'К типам контактов',
                       'width': 2},
    'add_new_contact': {'message_text': '<b>Добавление контакта технической поддержки:</b>\nВведите {link} нового контакта:', 'buttons': {
        'admin_backward:start_add_new_contact': 'Назад',
        'width': 1
    }},
    'add_new_contact:number': '\n<blockquote>В корректном формате номер телефона</blockquote>',
    'add_new_contact:@': '',
    'add_new_contact:@@': '\n<blockquote>Знак " @ " должен присутствовать в единичном экземпляре</blockquote>',
    'add_new_contact:exists':  '\n<blockquote>Введённый контакт уже существует.</blockquote>',
    'add_new_contact:symbols':  '\n<blockquote>Не более 100 символов.</blockquote>',

    'confirmation_add_contact': {'message_text': '<b>Добавление контакта технической поддержки:</b>\n───────────────\nКатегория: <b>{contact_entity}</b>\n{contact_type}: <b>{contact}</b>\n───────────────',
                                 'buttons': {
                                     'confirm_add_ts_contact': 'Подтвердить',
                                     'rewrite_ts_contact_link': 'Переписать',
                                     'admin_backward:confirmation_add_new_ts': 'Отмена',
                                     'width': 1
                                 }},
    'start_delete_contact': {'message_text': '<b>Удаление контакта технической поддержки:</b>\n───────────────\nКатегория: <b>{contact_entity}</b>\n{contact_type}: <b>{contact}</b>\n───────────────', 'buttons': {
        'confirm_delete_contact': 'Подтвердить',
        'admin_backward:start_delete_ts_contact': 'Назад',
        'width': 1
    }},

    'start_rewrite_exists_contact': {'message_text': '<b>Редактирование</b>:\n───────────────\nКатегория: <b>{entity}</b> \n{contact_type}: <b>{cur_link}</b>\n───────────────\n<b>Введите новый {link}:</b>',
                                     'buttons': {'admin_backward:start_rewrite_ts_contact': 'Назад',
                                                 'width': 1}},

    # 'start_rewrite_exists_contact:number': '\n<blockquote>В корректном формате номер телефона</blockquote>',
    # 'start_rewrite_exists_contact:@': '',
    # 'start_rewrite_exists_contact:exists': '\n<blockquote>Введённый контакт уже существует.</blockquote>',
    # 'start_rewrite_exists_contact:symbols': '\n<blockquote>Не более 100 символов.</blockquote>',

    'confirmation_rewrite_exist_contact': {'message_text': '<b>Редактирование</b>:\n───────────────\nКатегория: <b>{entity}</b> \n{last_contact_caption}: <b>{cur_link}</b>\n{new_link_caption}: <b>{new_link}</b>\n───────────────\n', 'buttons': {
        'confirm_rewrite_ts_contact': 'Подтвердить',
        'rewrite_rewriting_ts_contact': 'Ввести заново',
        'admin_backward:confirmation_rewrite_ts': 'Отменить',
        'width': 1
    }},



}
ADMIN_CONTACTS = SafeDict({'ru': __ADMIN_CONTACTS_RU,
                           'uz': ADMIN_CONTACTS_UZ})



class OutputTSContacts(SmartGetattr):
    def __init__(self):
        super().__init__()

        self.message_text = ADMIN_CONTACTS['active_contact_list']
        self.buttons_callback_data = 'review_ts_contact:'
        self.backward_command = {'add_ts_contact': ADMIN_CONTACTS['add'],
                                 'admin_backward:review_contacts_list': ADMIN_CONTACTS['backward'],
                                 'return_main_menu': ADMIN_CONTACTS['return_main_menu']}
        self.last_buttons = None
        self.width = 1
        self.dynamic_buttons = 3

OutputTSContacts = OutputTSContacts()