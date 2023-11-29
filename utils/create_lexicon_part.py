async def create_lexicon_part(lexicon_part_abc, buttons_captions):
    message_text = lexicon_part_abc.message_text
    buttons_callback_data = lexicon_part_abc.buttons_callback_data
    buttons_width = lexicon_part_abc.width
    if buttons_captions:
        lexicon_part = {'message_text': message_text, 'buttons': {f'{str(buttons_callback_data)}{string_model.id}': string_model.name for string_model in buttons_captions}}
        lexicon_part['buttons']['width'] = buttons_width
        return lexicon_part

