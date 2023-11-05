from typing import Set

from aiogram.types import Message, chat, CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from handlers.callback_handlers.buy_part.language_callback_handler import InlineCreator, redis_data
from utils.Lexicon import LEXICON


class TravelEditor:
    @staticmethod
    async def edit_message(lexicon_key: str, request, delete_mode=False, media_markup_mode=False,
                           button_texts: Set[str] = None, callback_sign: str = None, lexicon_cache=True, reply_mode = False, lexicon_part: dict = None, bot=None, photo=None, seller_boot=None):
        '''Высылальщик сообщений
        [reply_mode[bool]]: Работает только при удалении сообщений '''
        user_id = str(request.from_user.id)
        print('user_id =', user_id)
        new_message = None
        if not lexicon_part:
            lexicon_part = LEXICON[lexicon_key]
        redis_key = str(user_id) + ':last_message'
        last_message_id = await redis_data.get_data(redis_key)
        print('last_mas', last_message_id)

        if isinstance(request, CallbackQuery):
            message_object = request.message
        else:
            message_object = request

        if not bot:
            bot = message_object.bot


        chat_object = message_object.chat
        if button_texts:
            keyboard = await InlineCreator.create_markup(lexicon_part,
                                                         button_texts=button_texts, callback_sign=callback_sign)
        else:
            keyboard = await InlineCreator.create_markup(lexicon_part)

        message_text = lexicon_part['message_text']


        
        redis_key_current_lexicon = str(user_id) + ':current_lexicon_code'
        current_lexicon = await redis_data.get_data(key=redis_key_current_lexicon)
        if current_lexicon:
            redis_key_last_lexicon = str(user_id) + ':last_lexicon_code'
            await redis_data.set_data(redis_key_last_lexicon, current_lexicon)
            await redis_data.delete_key(redis_key_current_lexicon)

        if lexicon_cache:
            redis_key = str(user_id) + ':current_lexicon_code'
            await redis_data.set_data(redis_key, lexicon_key)

            redis_key = str(user_id) + ':last_message'

        if delete_mode and last_message_id:
            try:
                await chat.Chat.delete_message(self=chat_object, message_id=last_message_id)
            except:
                pass
            if reply_mode:
                print('reply_mode2')
                new_message = await message_object.reply(text=message_text, reply_markup=keyboard)
            else:
                print('NOreply_mode2')
                new_message = await message_object.answer(text=message_text, reply_markup=keyboard)

            print('new last', new_message.message_id)
        # elif media_markup_mode and formatted_config_output:
        #     await request.chat.bot.send_media_group(chat_id=request.chat.id,
        #                                                      media=formatted_config_output, reply_markup=keyboard)
        else:
            if photo:
                    try:
                        await message_object.delete()
                    except:
                        pass
                    if not reply_mode and photo:
                        print('NOTRM')
                        new_message = await bot.send_photo(chat_id=message_object.chat.id, photo=photo, caption=message_text, reply_markup=keyboard)

            if reply_mode:
                print('ph: ', photo)
                if not seller_boot:
                    redis_reply_key=str(request.from_user.id) + ':last_user_message'
                elif seller_boot:
                    print('YESSM')
                    redis_reply_key = str(request.from_user.id) + ':last_seller_message'
                print("YESRM")
                last_user_message = await redis_data.get_data(key=redis_reply_key)
                print('reply_mode2')
                #new_message = await message_object.reply(text=message_text, reply_markup=keyboard)
                new_message = await bot.send_message(chat_id=message_object.chat.id, reply_to_message_id=last_user_message, text=message_text, reply_markup=keyboard)
                print('new_repl', last_message_id)
                #await redis_data.set_data(redis_key, new_message.message_id)
                
            if last_message_id:
                if not photo:
                    try:
                        #await message_object.edit_text(text=message_text, reply_markup=keyboard)
                        return await bot.edit_message_text(chat_id=message_object.chat.id, message_id=last_message_id, text=message_text, reply_markup=keyboard)

                    except Exception as ex:
                        pass
                    
                try:
                    await chat.Chat.delete_message(self=chat_object, message_id=last_message_id)
                except:
                    pass    
                
            if not reply_mode and not photo:
                #new_message = await message_object.answer(text=message_text, reply_markup=keyboard)
                new_message = await bot.send_message(chat_id=message_object.chat.id, text=message_text, reply_markup=keyboard)
            print('new_send', last_message_id)
        
                    

                   

                    
                    #await redis_data.set_data(redis_key, new_message.message_id)
                    # print('SET: ', new_message.message_id)

        if new_message and not photo:
            await redis_data.set_data(redis_key, new_message.message_id)

            print('add+message = ', new_message.message_id)

travel_editor = TravelEditor()