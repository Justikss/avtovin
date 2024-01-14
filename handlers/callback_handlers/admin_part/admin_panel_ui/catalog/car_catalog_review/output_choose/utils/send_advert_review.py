import importlib

from database.data_requests.statistic_requests.adverts_to_admin_view_status import \
    advert_to_admin_view_related_requester
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.car_catalog_review.output_choose.output_choose_brand_to_catalog_review import \
    choose_review_catalog_brand_admin_handler
from handlers.callback_handlers.sell_part.checkout_seller_person_profile import get_seller_name
from handlers.utils.create_advert_configuration_block import create_advert_configuration_block
from handlers.utils.message_answer_without_callback import send_message_answer

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
car_advert_requests_module = importlib.import_module('database.data_requests.car_advert_requests')


async def send_advert_review(request, state, admin_pagination_object, data_to_output, message_editor):
    ic(data_to_output)
    output_data = data_to_output[0]
    seller_data = await get_seller_name(output_data.seller, for_admin=True)
    if seller_data:
        if isinstance(seller_data, tuple):
            seller_data = seller_data[0]

        await advert_to_admin_view_related_requester.activate_view_status(output_data)

        lexicon_part = Lexicon_module.CATALOG_LEXICON['review_specific_advert_catalog']

        lexicon_part['buttons']['page_counter'] = lexicon_part['buttons']['page_counter'].format(
            start=admin_pagination_object.current_page,
            end=admin_pagination_object.total_pages
        )

        lexicon_part['message_text'] = lexicon_part['message_text'].format(advert_id=output_data.id,
                                                           seller_entity=seller_data)
        lexicon_part['message_text'] += await create_advert_configuration_block(advert_id=output_data)
        photo_album = await car_advert_requests_module.AdvertRequester.get_photo_album_by_advert_id(output_data)
        ic(photo_album)
        await message_editor.travel_editor.edit_message(request=request, lexicon_key='', lexicon_part=lexicon_part,
                                                        media_group=photo_album, dynamic_buttons=3)


        '''ниже специфические действия'''
        await state.update_data(current_catalog_advert_id=output_data.id)

    else:
        await send_message_answer(request, Lexicon_module.ADMIN_LEXICON['action_non_actuality'])
        await choose_review_catalog_brand_admin_handler(request, state)


