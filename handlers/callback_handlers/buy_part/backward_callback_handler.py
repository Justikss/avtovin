import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from handlers.callback_handlers.sell_part.commodity_requests.sellers_feedbacks.my_feedbacks_button import \
    CheckFeedbacksHandler
from handlers.callback_handlers.buy_part.language_callback_handler import redis_data, set_language
from handlers.callback_handlers.buy_part.FAQ_tech_support import tech_support_callback_handler
from handlers.state_handlers.choose_car_for_buy.hybrid_handlers import search_auto_callback_handler
from handlers.state_handlers.seller_states_handler.seller_registration.seller_registration_handlers import hybrid_input_seller_number, dealership_input_address
from handlers.callback_handlers.sell_part.start_seller_registration_callback_handlers import input_seller_name
from handlers.state_handlers.seller_states_handler.seller_registration.check_your_registration_config import check_your_config
from handlers.callback_handlers.sell_part.start_sell_button_handler import start_sell_callback_handler
from handlers.callback_handlers.sell_part import checkout_seller_person_profile
from handlers.state_handlers.seller_states_handler import seller_profile_branch
from handlers.callback_handlers.sell_part import commodity_requests

from states.seller_registration_states import HybridSellerRegistrationStates
from states.tariffs_to_seller import ChoiceTariffForSellerStates
from handlers.callback_handlers.sell_part.commodity_requests.output_sellers_requests import \
    output_sellers_requests_by_car_brand_handler


async def backward_button_handler(callback: CallbackQuery, state: FSMContext):
    '''Кнопка назад, ориентируется на запись в редис: прошлый лексикон код,

                                                        прошлое состояние'''
    inline_creator = importlib.import_module('keyboards.inline.kb_creator')  # Ленивый импорт
    redis_storage = importlib.import_module('utils.redis_for_language')  # Ленивый импорт

    ic(callback.data)

    if ':' in callback.data:
        mode = callback.data.split(':')
        mode = mode[1]
        ic(mode)
        if mode.startswith('seller_registration'):
            incorrect_case = mode.split('(')
            if incorrect_case:
                last_user_message = await redis_storage.redis_data.get_data(key=str(callback.from_user.id) + ':last_user_message')
                if last_user_message:
                    await redis_storage.redis_data.delete_key(key=str(callback.from_user.id) + ':last_user_message')
                    try:
                        await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=last_user_message)
                    except:
                        pass
                # delete_mode = True
                # await callback.message.delete()
            # else:
            #     delete_mode = False
            seller_mode = await redis_storage.redis_data.get_data(key=str(callback.from_user.id) + ':seller_registration_mode')
            edit_mode = await redis_storage.redis_data.get_data(key=str(callback.from_user.id) + ':can_edit_seller_registration_data')

            need_method = None
            need_state = None

            if edit_mode == 'true':
                await state.set_state(HybridSellerRegistrationStates.check_input_data)
                need_method = check_your_config

            elif mode.startswith('seller_registration_seller_person_name'):
                await state.clear()
                callback_method = start_sell_callback_handler
                
                
            elif mode.startswith('seller_registration_dealership_name'):
                await state.clear()
                callback_method = start_sell_callback_handler
                
                
            elif mode.startswith('seller_registration_number'):
                # if seller_mode == 'dealership':
                #     need_state = CarDealerShipRegistrationStates.input_dealship_name
                # elif seller_mode == 'person':
                #     need_state = PersonSellerRegistrationStates.input_fullname
                    
                await state.clear()
                need_method = input_seller_name  
                
                
            elif mode.startswith('seller_registration_dealership_address'):
                await state.set_state(HybridSellerRegistrationStates.input_number)
                need_method = hybrid_input_seller_number


            if need_method:
                await need_method(request=callback, state=state, from_backward_Delete_mode=True)
            elif callback_method:
                await callback_method(callback=callback, state=state)


        elif mode == 'support':
            await tech_support_callback_handler(callback=callback)

        elif mode == 'choose_car_category':
            print('choty')
            await search_auto_callback_handler(callback=callback, state=state)

        elif mode == 'set_language':
            await set_language(request=callback, set_languange=False)

        elif mode.startswith('user_registration'):

            last_user_message = int(
                await redis_storage.redis_data.get_data(key=str(callback.from_user.id) + ':last_user_message'))
            if last_user_message:
                try:
                    await callback.message.chat.delete_message(message_id=last_user_message)
                    await redis_storage.redis_data.delete_key(key=str(callback.from_user.id) + ':last_user_message')
                except TelegramBadRequest:
                    pass

            if mode == 'user_registration_number':
                buyer_registration_handlers_module = importlib.import_module('handlers.state_handlers.buyer_registration_handlers')

                await state.set_state(buyer_registration_handlers_module.BuyerRegistationStates.input_full_name)
                await buyer_registration_handlers_module.input_full_name(request=callback, state=state)
            elif mode == 'user_registration':
                await state.clear()
                try:
                    await callback.message.delete()
                except:
                    pass
                await set_language(callback=callback, set_languange=False)
            else:
                print("LEXICON_CACHA")
                lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

                user_id = callback.from_user.id
                redis_key = str(user_id) + ':last_lexicon_code'
                last_lexicon_code = await redis_data.get_data(redis_key)
                await state.clear()
                await callback.message.delete()
                lexicon_part = lexicon_module.LEXICON[last_lexicon_code]
                message_text = lexicon_part['message_text']
                keyboard = await inline_creator.InlineCreator.create_markup(lexicon_part)
                message_object = await callback.message.answer(text=message_text, reply_markup=keyboard)
                await redis_storage.redis_data.set_data(key=str(user_id) + ':last_message', value = message_object.message_id)

        elif mode == 'affordable_tariffs':
            ic()
            await state.clear()
            await checkout_seller_person_profile.output_seller_profile(callback=callback)

        elif mode == 'tariff_preview':
            await state.set_state(ChoiceTariffForSellerStates.choose_tariff)
            await seller_profile_branch.tariff_extension.output_affordable_tariffs_handler(callback=callback, state=state)
        
        elif mode == 'choose_payment_system':
            await state.set_state(ChoiceTariffForSellerStates.preview_tariff)
            await seller_profile_branch.selected_tariff_preview.tariff_preview_handler(callback=callback, state=state, backward_call=True)

        elif mode == 'sales_brand_choose':
            await commodity_requests.commodity_requests_handler.commodity_reqests_by_seller(callback=callback, state=state)

        elif mode == 'sales_order_review':
            await commodity_requests.my_requests_handler.seller_requests_callback_handler(callback=callback, state=state, delete_mode=True)

        elif mode in ('seller_start_delete_request', 'seller_delete_request', 'rewrite_price_by_seller'):


            car_brand = await redis_storage.redis_data.get_data(key=str(callback.from_user.id) + ':sellers_requests_car_brand_cache')
            await output_sellers_requests_by_car_brand_handler(callback, state, chosen_brand=car_brand)


        # elif mode == 'start_boot_new_car':
        #     edit_mode = await redis_storage.redis_data.get_data(key=str(callback.from_user.id) + ':can_edit_seller_boot_commodity')
        #     if edit_mode and edit_mode != 'null':
        #         print('EDITMOD ', edit_mode, type(edit_mode))
        #         await output_load_config_for_seller(request=callback, state=state)
        #     else:
        #         await commodity_requests.commodity_requests_handler.commodity_reqests_by_seller(callback)

        elif mode == 'seller__my_feedbacks':

            await commodity_requests.commodity_requests_handler.commodity_reqests_by_seller(callback, state=state, delete_mode=True)

        elif mode == 'check_feedbacks':
            ic()
            await CheckFeedbacksHandler.my_feedbacks_callback_handler(callback, state=state, delete_media_group_mode=True)
    else:
        print("LEXICON_CACHA")
        memory_data = await state.get_data()
        last_lexicon_code = memory_data.get('last_lexicon_code')
        if last_lexicon_code:
            if last_lexicon_code.endswith('(incorrect)'):
                last_lexicon_code = str(last_lexicon_code.split('(')[0])
            last_state = memory_data['last_state']
            await state.set_state(last_state)
            await state.update_data(last_lexicon_code=None)
        else:
            user_id = callback.from_user.id
            redis_key = str(user_id) + ':last_lexicon_code'
            last_lexicon_code = await redis_data.get_data(redis_key)
            await state.clear()


        # lexicon_part = LEXICON[last_lexicon_code]
        # message_text = lexicon_part['message_text']
        # keyboard = await inline_creator.InlineCreator.create_markup(lexicon_part)
        # await callback.message.edit_text(text=message_text, reply_markup=keyboard)
        message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
        await message_editor.travel_editor.edit_message(request=callback, lexicon_key=last_lexicon_code)
        await state.update_data(last_lexicon_code=None)
        await state.update_data(last_state=None)
