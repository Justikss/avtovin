from handlers.callback_handlers.admin_part.admin_panel_ui.advertisement_actions.mailing.mailing_storage.choose_specific_type import \
    request_choose_mailing_type
from handlers.utils.message_answer_without_callback import send_message_answer
from handlers.utils.send_any_medias import send_media
from utils.lexicon_utils.Lexicon import ADVERT_LEXICON, LEXICON
from utils.lexicon_utils.admin_lexicon.admin_lexicon import captions


async def send_mailing_review(request, state, admin_pagination_object, data_to_output, message_editor):
    if not data_to_output:
        await request_choose_mailing_type(request, state)
        await send_message_answer(request, LEXICON['non_actiallity'])
        return
    output_data = data_to_output[0]['__data__']
    lexicon_part = ADVERT_LEXICON['send_mailing_review']
    lexicon_part['message_text'] = lexicon_part['message_text'].format(
        mailing_recipients=captions[output_data['recipients_type']],
        mailing_date=str(output_data['scheduled_time']).split()[0],
        mailing_time=str(output_data['scheduled_time']).split()[-1]
    )
    lexicon_part['buttons']['page_counter'] = lexicon_part['buttons']['page_counter'].format(
    start=admin_pagination_object.current_page,
    end=admin_pagination_object.total_pages
    )
    mailing_messages = await send_media(request, media_info_list=output_data['media'], caption=output_data['text'])
    if mailing_messages:
        reply_mode = mailing_messages[0]
    else:
        reply_mode = None

    await message_editor.travel_editor.edit_message(request=request, lexicon_key='',
                                                    lexicon_part=lexicon_part, save_media_group=True,
                                                    dynamic_buttons=2, delete_mode=True,
                                                    reply_message=reply_mode)