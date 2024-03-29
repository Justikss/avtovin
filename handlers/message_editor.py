import asyncio
import importlib
import traceback
from typing import Set

from aiogram.types import chat, CallbackQuery, InputMediaPhoto, InputFile, FSInputFile
from aiogram.exceptions import TelegramBadRequest, TelegramServerError

from config_data.config import anti_spam_duration
from handlers.callback_handlers.buy_part.language_callback_handler import InlineCreator, redis_data
from handlers.utils.delete_message import delete_message

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')


class TravelEditor:
    @staticmethod
    async def edit_message(lexicon_key: str, request, delete_mode=False, media_markup_mode=False, send_chat=None, my_keyboard=None, need_media_caption=False, save_media_group=False, delete_media_group_mode = False, reply_message=None,
                           button_texts: Set[str] = None, callback_sign: str = None, lexicon_cache=True, reply_mode = False, lexicon_part: dict = None, bot=None, media_group=None, seller_boot=None, dynamic_buttons=False):
        '''Высылальщик сообщений
        [reply_mode[bool]]: Работает только при удалении сообщений '''
        from utils.context_managers import ignore_exceptions

        async with ignore_exceptions():
            keyboard = None
            ic('load_photos editor??: ', media_group)
            user_id = str(request.from_user.id)
            ic('user_id =', user_id)
            new_message = None
            if not lexicon_part:
                lexicon_part = Lexicon_module.LEXICON[lexicon_key]
            redis_key = str(user_id) + ':last_message'
            last_message_id = await redis_data.get_data(redis_key)
            ic('last_mas', last_message_id)

            if isinstance(request, CallbackQuery):
                message_object = request.message
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
                    # if isinstance(media_group_message, int):
                    await delete_message(request, chat_id=send_chat_id, message_id=media_group_message)
                    await redis_data.delete_key(key=user_id + ':last_media_group')

            media_message_id = None
            if not media_group:
                media_message_id = await redis_data.get_data(key=user_id + ':last_media_group', use_json=True)
                if reply_message:
                    media_message_id = reply_message
                elif media_message_id:
                    media_message_id = media_message_id[0]
            ic(lexicon_part)
            # ic(lexicon_part.get('width') or lexicon_part.get('buttons'))

            if not my_keyboard:
                if button_texts:
                    keyboard = await InlineCreator.create_markup(lexicon_part,
                                                                 button_texts=button_texts, callback_sign=callback_sign, dynamic_buttons=dynamic_buttons)
                elif lexicon_part.get('width') or lexicon_part.get('buttons'):
                    keyboard = await InlineCreator.create_markup(lexicon_part, dynamic_buttons=dynamic_buttons)
                    ic(keyboard)
            else:
                keyboard = my_keyboard

            ic(keyboard)

            '''Идут методы работы с сообщениями'''
            if not isinstance(lexicon_part, dict):
                lexicon_part = {'message_text': lexicon_part}

            message_text = lexicon_part['message_text']

            if delete_mode and last_message_id and not media_group:
                ic('delete_if delete_mode and last_message_id:')
                await delete_message(request, message_id=last_message_id)

                if reply_mode:
                    ic('reply_mode2')
                    new_message = await message_object.reply(text=message_text, reply_markup=keyboard)
                elif not media_group:
                    ic(keyboard, message_text)
                    ic('NOreply_mode2')
                    try:
                        new_message = await message_object.answer(text=message_text, reply_to_message_id=media_message_id, reply_markup=keyboard)
                    except TelegramBadRequest:
                        new_message = await message_object.answer(text=message_text, reply_markup=keyboard)

            else:
                if media_group:
                    '''Медиагруппа в чужой чат - идёт без кнопок'''

                    if not reply_mode and media_group:
                        ic('if not reply_mode and media_group:')

                        # Получение album_id
                        album_id = next(iter(media_group), None) if isinstance(media_group, dict) else None

                        ic(album_id)

                        if send_chat or need_media_caption:
                            # Определение списка файлов
                            file_list = media_group[album_id] if album_id else media_group

                            file_list = file_list[:8]
                            ic(file_list)

                            # Создание объектов для отправки
                            caption_photo = [
                                InputMediaPhoto(media=file_data['id'] if '/' not in file_data['id'] else FSInputFile(file_data['id']) if isinstance(file_data, dict) else file_data,
                                                caption=lexicon_part['message_text'])
                                for file_data in file_list[:2]]

                            new_album = [InputMediaPhoto(media=file_data['id'] if '/' not in file_data['id'] else FSInputFile(file_data['id']) if isinstance(file_data, dict) else file_data)
                                         for file_data in file_list[1:]][:8]

                            new_album.insert(0, caption_photo[0])  # Добавление фото с подписью в начало альбома
                            ic(new_album)
                            try:
                                new_media_message = await bot.send_media_group(chat_id=send_chat_id, media=new_album)
                            except TelegramServerError:
                                # traceback.print_exc()

                                try:
                                    new_media_message = await bot.send_media_group(chat_id=send_chat_id, media=new_album)
                                except:
                                    # traceback.print_exc()
                                    pass
                            await redis_data.set_data(key=user_id+':last_media_group',
                                                      value=[media_message.message_id
                                                             for media_message in new_media_message])
                            ic('post ', new_album)

                        else:
                            ic(media_group, album_id)
                            if album_id:
                                media_group = media_group[album_id]
                            ic(media_group)
                            media_group = media_group[:8]
                            new_album = [InputMediaPhoto(media=file_data['id'] if '/' not in file_data['id'] else FSInputFile(file_data['id'])) for file_data in media_group]
                            ic('post ', new_album)
                            ic(len(new_album))
                            try:
                                new_media_message = await bot.send_media_group(chat_id=send_chat_id, media=new_album)
                            except TelegramServerError:
                                # traceback.print_exc()
                                try:
                                    new_media_message = await bot.send_media_group(chat_id=send_chat_id, media=new_album)

                                except:
                                    # traceback.print_exc()
                                    pass
                            ic(lexicon_part['message_text'])
                            await asyncio.sleep(anti_spam_duration)
                            new_message = await bot.send_message(chat_id=send_chat_id, text=lexicon_part['message_text'],
                                                                 reply_markup=keyboard,
                                                                 reply_to_message_id=new_media_message[0].message_id)
                            await redis_data.set_data(key=user_id+':last_media_group',
                                                      value=[media_message.message_id
                                                             for media_message in new_media_message])

                if reply_mode:
                    ic('if reply_mode')
                    if not seller_boot:
                        redis_reply_key=str(request.from_user.id) + ':last_user_message'
                    elif seller_boot:
                        redis_reply_key = str(request.from_user.id) + ':last_seller_message'
                    last_user_message = await redis_data.get_data(key=redis_reply_key)
                    #new_message = await message_object.reply(text=message_text, reply_markup=keyboard)
                    try:
                        new_message = await bot.send_message(chat_id=send_chat_id, reply_to_message_id=last_user_message, text=message_text, reply_markup=keyboard)
                    except TelegramBadRequest:
                        await travel_editor.edit_message(request=request, lexicon_key=lexicon_key,
                                                                  lexicon_part=lexicon_part, bot=bot)

                if last_message_id:
                    if not media_group and need_media_caption:
                        new_media_message = await bot.send_message(chat_id=send_chat_id, reply_to_message_id=media_message_id, text=lexicon_part['message_text'])
                        await redis_data.set_data(key=user_id + ':last_media_group',
                                                  value=new_media_message.message_id)
                    if not media_group:
                        try:
                            #await message_object.edit_text(text=message_text, reply_markup=keyboard)
                            ic('if last_message_id:if not media_group')
                            return await bot.edit_message_text(chat_id=send_chat_id, message_id=last_message_id, text=message_text, reply_markup=keyboard)

                        except Exception as ex:
                            if message_object.chat.id == send_chat_id:
                                pass
                            else:
                                return await bot.send_message(chat_id=send_chat_id, reply_to_message_id=media_message_id, text=message_text, reply_markup=keyboard)

                    if not send_chat:
                        ic('delete_if_last_message_id')
                        await delete_message(request, chat_id=send_chat_id, message_id=last_message_id)

                ic('load_photos editor2??: ', media_group)
                ic(reply_mode, keyboard)
                ic(not reply_mode and keyboard and not media_group)
                if not reply_mode and keyboard and not media_group:
                    ic('if not reply_mode and keyboard')
                    ic(send_chat_id, media_message_id, message_text, keyboard)
                    #new_message = await message_object.answer(text=message_text, reply_markup=keyboard)
                    new_message = await bot.send_message(chat_id=send_chat_id, reply_to_message_id=media_message_id, text=message_text, reply_markup=keyboard)

            if new_message:
                await redis_data.set_data(redis_key, new_message.message_id)



travel_editor = TravelEditor()