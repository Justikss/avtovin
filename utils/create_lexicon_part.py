async def create_lexicon_part(lexicon_part_abc, buttons_captions, request=None, state=None, need_width=False, need_last_buttons=True):
    ic(lexicon_part_abc.__class__.__dict__)
    ic(lexicon_part_abc.__dict__)

    ic(lexicon_part_abc, buttons_captions)
    message_text = lexicon_part_abc.message_text
    buttons_callback_data = lexicon_part_abc.buttons_callback_data
    buttons_width = lexicon_part_abc.width
    ic(lexicon_part_abc.__class__.__name__)
    if ~isinstance(lexicon_part_abc, object) and lexicon_part_abc.__class__.__name__.startswith('load_commodity'):
        ic()
        ic(state)
        if hasattr(lexicon_part_abc, 'initializate'):
            ic(lexicon_part_abc.__dict__)
            await lexicon_part_abc.initializate(request, state)
            ic(lexicon_part_abc.__dict__)

    lexicon_part = {'message_text': message_text}
    lexicon_part['buttons'] = {}
    if buttons_captions:
        ic(buttons_captions)
        lexicon_part['buttons'] =  {f'{str(buttons_callback_data)}{string_model.id}': string_model.name for string_model in buttons_captions}
    if lexicon_part_abc.__dict__.get('last_buttons'):
        if need_last_buttons == True:
            iterable = lexicon_part_abc.last_buttons.items()
        elif need_last_buttons != False:
            iterable = need_last_buttons.items()
        else:
            iterable = None
        if iterable:
            for callback_data, caption in iterable:
                lexicon_part['buttons'][callback_data] = caption
    if need_width:
        lexicon_part['buttons']['width'] = buttons_width
    ic(lexicon_part)

    return lexicon_part

