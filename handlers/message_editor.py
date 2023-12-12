from typing import Set

from aiogram.types import chat, CallbackQuery, InputMediaPhoto, InputFile, FSInputFile
from aiogram.exceptions import TelegramBadRequest

from handlers.callback_handlers.buy_part.language_callback_handler import InlineCreator, redis_data
from utils.lexicon_utils.Lexicon import LEXICON


class TravelEditor:
    @staticmethod
    async def edit_message(lexicon_key: str, request, delete_mode=False, media_markup_mode=False, send_chat=None, my_keyboard=None, need_media_caption=False, save_media_group=False, delete_media_group_mode = False, reply_message=None,
                           button_texts: Set[str] = None, callback_sign: str = None, lexicon_cache=True, reply_mode = False, lexicon_part: dict = None, bot=None, media_group=None, seller_boot=None, dynamic_buttons=False):
        '''Высылальщик сообщений
        [reply_mode[bool]]: Работает только при удалении сообщений '''
        keyboard = None
        print('load_photos editor??: ', media_group)
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
            await request.answer()
        else:
            message_object = request

        if not bot:
            bot = message_object.bot

        if not send_chat:
            send_chat_id = message_object.chat.id
        else:
            send_chat_id = send_chat

        chat_object = message_object.chat
        # ic(save_media_group, media_group, delete_media_group_mode)
        if (not media_group and not save_media_group) or (delete_media_group_mode):
            ic()
            media_group_message = await redis_data.get_data(key=user_id + ':last_media_group', use_json=True)
            if not media_group_message:
                media_group_message = await redis_data.get_data(key=user_id + ':seller_media_group_messages', use_json=True)
            ic(media_group_message)
            if media_group_message:
                if isinstance(media_group_message, int):
                    try:
                        await bot.delete_message(chat_id=send_chat_id, message_id=media_group_message)
                    except:
                        pass
                    await redis_data.delete_key(key=user_id + ':last_media_group')

                else:
                    for message_id in media_group_message:
                        try:
                            await bot.delete_message(chat_id=send_chat_id, message_id=message_id)

                        except TelegramBadRequest:
                            pass
                        try:
                            await redis_data.delete_key(key=user_id + ':last_media_group')
                        except:
                            pass
        media_message_id = None
        if not media_group:
            media_message_id = await redis_data.get_data(key=user_id + ':last_media_group', use_json=True)
            if reply_message:
                media_message_id = reply_message
            elif media_message_id:
                media_message_id = media_message_id[0]


        if not my_keyboard:
            if button_texts:
                keyboard = await InlineCreator.create_markup(lexicon_part,
                                                             button_texts=button_texts, callback_sign=callback_sign, dynamic_buttons=dynamic_buttons)
            elif lexicon_part.get('width') or lexicon_part.get('buttons'):
                keyboard = await InlineCreator.create_markup(lexicon_part, dynamic_buttons=dynamic_buttons)
        else:
            keyboard = my_keyboard

        '''Идут методы работы с сообщениями'''

        message_text = lexicon_part['message_text']

        if delete_mode and last_message_id and not media_group:
            try:
                await chat.Chat.delete_message(self=chat_object, message_id=last_message_id)
                print('delete_if delete_mode and last_message_id:')
            except:
                pass
            if reply_mode:
                print('reply_mode2')
                new_message = await message_object.reply(text=message_text, reply_markup=keyboard)
            elif not media_group:
                print('NOreply_mode2')
                new_message = await message_object.answer(text=message_text, reply_to_message_id=media_message_id, reply_markup=keyboard)

        else:
            if media_group:
                '''Медиагруппа в чужой чат - идёт без кнопок'''

                if not reply_mode and media_group:
                    print('if not reply_mode and media_group:')

                    # Получение album_id
                    album_id = next(iter(media_group), None) if isinstance(media_group, dict) else None

                    print(album_id)

                    if send_chat or need_media_caption:
                        # Определение списка файлов
                        file_list = media_group[album_id] if album_id else media_group

                        file_list = file_list[:5]
                        ic(file_list)

                        # Создание объектов для отправки
                        caption_photo = [
                            InputMediaPhoto(media=file_data['id'] if '/' not in file_data['id'] else FSInputFile(file_data['id']) if isinstance(file_data, dict) else file_data,
                                            caption=lexicon_part['message_text'])
                            for file_data in file_list[:2]]

                        new_album = [InputMediaPhoto(media=file_data['id'] if '/' not in file_data['id'] else FSInputFile(file_data['id']) if isinstance(file_data, dict) else file_data)
                                     for file_data in file_list[1:]]

                        new_album.insert(0, caption_photo[0])  # Добавление фото с подписью в начало альбома

                        new_media_message = await bot.send_media_group(chat_id=send_chat_id, media=new_album)


                        await redis_data.set_data(key=user_id+':last_media_group',
                                                  value=[media_message.message_id
                                                         for media_message in new_media_message])
                        print('post ', new_album)

                    else:
                        if album_id:
                            if len(media_group) > 5:
                                media_group[album_id] = media_group[album_id][:5]
                            # ic(media_group)
                            # new_album = [InputMediaPhoto(media=file_data['id']) for file_data in media_group[album_id]]
                            media_group = media_group[album_id]
                        else:
                            if len(media_group) > 5:
                                media_group = media_group[:5]

                        if len(media_group) > 5:
                            media_group = media_group[:5]

                        new_album = [InputMediaPhoto(media=file_data['id'] if '/' not in file_data['id'] else FSInputFile(file_data['id'])) for file_data in media_group]

                        print('post ', new_album)
                        new_media_message = await bot.send_media_group(chat_id=send_chat_id, media=new_album)
                        new_message = await bot.send_message(chat_id=send_chat_id, text=lexicon_part['message_text'],
                                                             reply_markup=keyboard,
                                                             reply_to_message_id=new_media_message[0].message_id)
                        await redis_data.set_data(key=user_id+':last_media_group',
                                                  value=[media_message.message_id
                                                         for media_message in new_media_message])

            if reply_mode:
                print('if reply_mode')
                print('ph: ', media_group)
                if not seller_boot:
                    redis_reply_key=str(request.from_user.id) + ':last_user_message'
                elif seller_boot:
                    print('YESSM')
                    redis_reply_key = str(request.from_user.id) + ':last_seller_message'
                print("YESRM")
                last_user_message = await redis_data.get_data(key=redis_reply_key)
                print('reply_mode2')
                #new_message = await message_object.reply(text=message_text, reply_markup=keyboard)
                try:
                    new_message = await bot.send_message(chat_id=send_chat_id, reply_to_message_id=last_user_message, text=message_text, reply_markup=keyboard)
                except TelegramBadRequest:
                    await travel_editor.edit_message(request=request, lexicon_key=lexicon_key,
                                                              lexicon_part=lexicon_part, bot=bot)
                print('new_repl', last_message_id)
                #await redis_data.set_data(redis_key, new_message.message_id)
                
            if last_message_id:
                if not media_group and need_media_caption:
                    new_media_message = await bot.send_message(chat_id=send_chat_id, reply_to_message_id=media_message_id, text=lexicon_part['message_text'])
                    await redis_data.set_data(key=user_id + ':last_media_group',
                                              value=new_media_message.message_id)
                if not media_group:
                    try:
                        #await message_object.edit_text(text=message_text, reply_markup=keyboard)
                        print('if last_message_id:if not media_group')
                        return await bot.edit_message_text(chat_id=send_chat_id, message_id=last_message_id, text=message_text, reply_markup=keyboard)

                    except Exception as ex:
                        if message_object.chat.id == send_chat_id:
                            pass
                        else:
                            return await bot.send_message(chat_id=send_chat_id, reply_to_message_id=media_message_id, text=message_text, reply_markup=keyboard)


                if not send_chat:
                    try:
                        await chat.Chat.delete_message(self=chat_object, message_id=last_message_id)
                        print('delete_if_last_message_id')
                    except:
                        pass

            print('load_photos editor2??: ', media_group)
            if not reply_mode and keyboard and not media_group:
                print('if not reply_mode and keyboard')
                ic(send_chat_id, media_message_id, message_text, keyboard)
                #new_message = await message_object.answer(text=message_text, reply_markup=keyboard)
                new_message = await bot.send_message(chat_id=send_chat_id, reply_to_message_id=media_message_id, text=message_text, reply_markup=keyboard)
            print('new_send', last_message_id)

        if new_message:
            await redis_data.set_data(redis_key, new_message.message_id)

            print('add+message = ', new_message.message_id)



travel_editor = TravelEditor()