import importlib

from utils.lexicon_utils.admin_lexicon.admin_lexicon import captions


async def get_ban_notification_lexicon_part(activity, reason):
    admin_lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
    lexicon_part = admin_lexicon_module.ADMIN_LEXICON['user_ban_notification']
    ic(activity)
    ic(captions)
    ic(captions[activity])
    ic(lexicon_part['message_text'])
    message_text = lexicon_part['message_text'].format(activity=captions[activity], reason=reason)
    ic(message_text)
    correct_lexicon_part = {'message_text': message_text,
                            'buttons': {}}
    ic(correct_lexicon_part)
    ic(lexicon_part)
    for key, value in lexicon_part['buttons'].items():
        if key == 'close_ban_notification':
            key = f'{key}:{activity}'

        correct_lexicon_part['buttons'][key] = value


    return correct_lexicon_part
