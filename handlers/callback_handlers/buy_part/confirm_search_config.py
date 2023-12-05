import importlib
import traceback
from copy import copy

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from icecream import ic

from database.data_requests.car_advert_requests import AdvertRequester
from handlers.callback_handlers.hybrid_part import return_main_menu
from handlers.callback_handlers.sell_part.commodity_requests.sellers_feedbacks.my_feedbacks_button import \
    CheckFeedbacksHandler
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_cars_pagination_system.pagination_system_for_buyer import \
    BuyerCarsPagination
from states.buyer_offers_states import CheckActiveOffersStates
from utils.Lexicon import LEXICON
from database.data_requests.person_requests import PersonRequester
from utils.user_notification import send_notification_for_seller

# ic.disable()

async def get_keyboard_on_active_offer():
    inline_keyboard_creator_module = importlib.import_module('keyboards.inline.kb_creator')

    buttons = {key: value
               for key, value in LEXICON['chosen_configuration'].items()
               if key not in ('confirm_buy_settings:', 'message_text')}
    ic(buttons)
    keyboard = await inline_keyboard_creator_module.InlineCreator.create_markup(input_data=buttons)
    return keyboard

async def activate_offer_handler(callback: CallbackQuery, state: FSMContext, car_model, car_id, pagination_data):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    cached_requests_module = importlib.import_module('database.data_requests.offers_requests')

    insert_response = await cached_requests_module.OffersRequester.set_offer_model(buyer_id=callback.from_user.id,
                                                                                   car_id=car_id,
                                                                                   seller_id=car_model.seller.telegram_id)
    if not insert_response:
        await callback.answer(text=LEXICON['buy_configuration_error']['message_text'], show_alert=True)
    if car_model:
        choose_hybrid_handlers_module = importlib.import_module(
            'handlers.state_handlers.choose_car_for_buy.hybrid_handlers')

        data_for_seller = await CheckFeedbacksHandler.make_unpacked_data_for_seller_output(callback,
                                                                                           from_buyer=True,
                                                                                           viewed=False,
                                                                                           car_id=car_id)
        data_for_seller = data_for_seller[0]
        ic(data_for_seller)
        media_mode = True if data_for_seller.get('album') else False
        await send_notification_for_seller(callback, data_for_seller, media_mode=media_mode)
        await state.set_state(CheckActiveOffersStates.show_from_non_confirm_offers)
        formatted_cars_data = await choose_hybrid_handlers_module.get_cars_data_pack(callback=callback,
                                                                                     state=state,
                                                                                     car_models=await AdvertRequester.get_where_id(
                                                                                         car_id))

        iteration_pagination_data = copy(pagination_data['data'])
        ic(formatted_cars_data)
        ic(pagination_data)
        pagination_data['data'] = []
        for part in iteration_pagination_data:
            ic(part)
            if int(part['car_id']) == int(car_id):
                part = formatted_cars_data[0]
            pagination_data['data'].append(part)
        try:
            media_groups = await message_editor.redis_data.get_data(
                key=f'{str(callback.from_user.id)}:last_media_group',
                use_json=True)

            keyboard = await get_keyboard_on_active_offer()
            last_message_id = await message_editor.redis_data.get_data(
                key=f'{str(callback.from_user.id)}:last_message')
            ic(last_message_id)
            if not media_groups:

                await callback.bot.edit_message_text(chat_id=callback.message.chat.id, message_id=last_message_id,
                                                     text=formatted_cars_data[0]['message_text'], reply_markup=keyboard)

            else:
                media_group_message = media_groups[0]
                await callback.bot.edit_message_caption(chat_id=callback.message.chat.id, message_id=media_group_message,
                                                        caption=formatted_cars_data[0]['message_text'])
                await callback.bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=last_message_id,
                                                             reply_markup=keyboard)

        except Exception as ex:
            ic(ex)
            traceback.print_exc()
        callback_answer_text = LEXICON['order_was_created']
    else:
        callback_answer_text = LEXICON['seller_dont_exists']
    ic(callback_answer_text)
    await callback.answer(text=callback_answer_text, show_alert=True)

    return pagination_data


async def confirm_settings_handler(callback: CallbackQuery, state: FSMContext):
    '''Обработка подтверждения(от пользователя) поисковых настроек на покупку автомобиля'''
    cached_requests_module = importlib.import_module('database.data_requests.offers_requests')
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    # redis_data = importlib.import_module('utils.redis_for_language')
    car_dont_exists = False
    ic(callback.data)
    car_id = callback.data.split(':')[-1]

    pagination_data = await message_editor.redis_data.get_data(key=f'{str(callback.from_user.id)}:buyer_cars_pagination',
                                             use_json=True)

    car_model = await AdvertRequester.get_where_id(car_id)
    cached_data = None
    if car_model:

        cached_data = await cached_requests_module.CachedOrderRequests.get_cache(buyer_id=callback.from_user.id, car_id=car_id)
        if cached_data:
            cached_data = cached_data[0]
            ic(cached_data)
            await cached_requests_module.CachedOrderRequests.remove_cache(buyer_id=callback.from_user.id, car_id=car_id)
            cached_data = {'car_id': cached_data.car_id.id,
                           'message_text': cached_data.message_text,
                           'album': await AdvertRequester.get_photo_album_by_advert_id(cached_data.car_id)}

            # data_for_seller = await output_for_seller_formater(callback, cached_data)

            try:
                pagination_data = await activate_offer_handler(callback, state, car_model=car_model, car_id=car_id, pagination_data=pagination_data)
            except BufferError as ex:
                print(ex)
                insert_response = None
                await callback.answer(text=LEXICON['buy_configuration_error']['message_text'], show_alert=True)
            except Exception as ex:
                ic(ex)
                traceback.print_exc()

    if not cached_data or not car_model:
        car_dont_exists = True

        if not car_model:
            await callback.answer(text=LEXICON['car_was_withdrawn_from_sale'], show_alert=True)
        else:
            await callback.answer(text=LEXICON['buy_configuration_error']['message_text'], show_alert=True)


    ic(len(pagination_data['data']), cached_data, car_dont_exists)
    if not cached_data: #len(pagination_data['data']) <= 1 or
        await message_editor.redis_data.delete_key(key=f'{str(callback.from_user.id)}:buyer_cars_pagination')

        return await return_main_menu.return_main_menu_callback_handler(callback=callback, state=state)

    else:
        # data_part_to_delete = [data_part for data_part in pagination_data['data'] if int(data_part['car_id']) == int(car_id)]

        # ic(pagination_data['data'])
        # pagination_data['data'].pop(pagination_data['current_page']-1)
        # ic(pagination_data)


        await message_editor.redis_data.set_data(
            key=f'{str(callback.from_user.id)}:buyer_cars_pagination',
            value=pagination_data)

        # pagination = BuyerCarsPagination(**pagination_data)
        # pagination.pagination.current_page -= 1
        # ic(pagination_data['data'])
        # await pagination.send_page(callback, state, '+')



    # await redis_data.redis_data.set_data(key=f'{str(callback.from_user.id)}:buyer_nonconfirm_cars_cache',
    #                                        value=formatted_config_output)

    await callback.answer()
