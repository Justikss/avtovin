from utils.lexicon_utils.admin_lexicon.admin_catalog_lexicon import return_main_menu
from utils.safe_dict_class import SafeDict

__ADMIN_CONTACTS_RU = {
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
    'choose_type': {'message_text': 'Выберите тип контакта технической поддержки:', 'buttons': {
        'ts_contact_type:telegram': 'Телеграм', 'ts_contact_type:number': 'Телефонный номер',
        **return_main_menu,
        'width': 1
    }},
    'output_contact': {'message_text': 'Контакт технической поддержки:\n{contact_entity}\n{contact}',
                       'delete_ts_contact': 'Удалить', 'edit_ts_contact': 'Изменить',
                       'admin_backward:review_profile': 'Назад', 'admin_backward:to_type_contacts': 'К типам контактов',
                       'width': 2},
    'add_new_contact': {'message_text': 'Введите {link} нового контакта:', 'buttons': {
        'admin_backward:start_add_new_contact': 'Назад',
        'width': 1
    }},
    'add_new_contact:number': 'Введите {link} нового контакта\n<b>В корректном формате номер телефона</b>:',
    'add_new_contact:@': 'Введите <b>{link}</b> нового контакта:',
    'add_new_contact:exists': 'Введите {link} нового контакта:\n<b>Введённый контакт уже существует.</b>',
    'add_new_contact:symbols': 'Введите {link} нового контакта:\n<b>Не более 100 символов.</b>',

    'confirmation_add_contact': {'message_text': 'Добавление нового контакта технической поддержки:\n{entity}\n{link}',
                                 'buttons': {
                                     'confirm_add_ts_contact': 'Подтвердить',
                                     'rewrite_ts_contact_link': 'Переписать',
                                     'admin_backward:confirmation_add_new_ts': 'Отмена',
                                     'width': 1
                                 }},
    'start_delete_contact': {'message_text': 'Удаление контакта технической поддержки:\n{entity}\n{link}', 'buttons': {
        'confirm_delete_contact': 'Подтвердить',
        'admin_backward:start_delete_ts_contact': 'Назад',
        'width': 1
    }},

    'start_rewrite_exists_contact': {'message_text': 'Редактирование {entity} {cur_link}\nВведите новый {link}:',
                                     'buttons': {'admin_backward:start_rewrite_ts_contact': 'Назад',
                                                 'width': 1}},

    'start_rewrite_exists_contact:number': 'Введите {link} редактируемого контакта: {cur_link}\n<b>В корректном формате номер телефона</b>:',
    'start_rewrite_exists_contact:@': 'Введите <b>{link}</b> редактируемого контакта: {cur_link}:',
    'start_rewrite_exists_contact:exists': 'Введите {link} редактируемого контакта: {cur_link}:\n<b>Введённый контакт уже существует.</b>',
    'start_rewrite_exists_contact:symbols': 'Введите {link} редактируемого контакта: {cur_link}:\n<b>Не более 100 символов.</b>',

    'confirmation_rewrite_exist_contact': {'message_text': 'Редактирование контакта технической поддержки\n{link} {cur_link}\nНа новое значение: {new_link}', 'buttons': {
        'confirm_rewrite_ts_contact': 'Подтвердить',
        'rewrite_rewriting_ts_contact': 'Ввести заново',
        'admin_backward:confirmation_rewrite_ts': 'Отменить',
        'width': 1
    }},



}
ADMIN_CONTACTS = SafeDict({'ru': __ADMIN_CONTACTS_RU,
                           'uz': 0})



class OutputTSContacts:
    def __init__(self):
        self.message_text = ADMIN_CONTACTS['active_contact_list']
        self.buttons_callback_data = 'review_ts_contact:'
        self.backward_command = {'add_ts_contact': ADMIN_CONTACTS['add'],
                                 'admin_backward:review_contacts_list': ADMIN_CONTACTS['backward'],
                                 'return_main_menu': ADMIN_CONTACTS['return_main_menu']}
        self.width = 1
        self.dynamic_buttons = 3

OutputTSContacts = OutputTSContacts()