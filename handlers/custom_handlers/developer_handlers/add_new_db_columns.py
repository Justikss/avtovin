from aiogram.types import Message



async def add_db_columns(message: Message):
    await message.answer('pass')
    # from database.db_connect import database
    # await message.answer('start')
    # alter_table_commands = [
    #     '''ALTER TABLE "Продавцы" ADD COLUMN is_banned BOOLEAN DEFAULT FALSE''',
    #     '''ALTER TABLE "Продавцы" ADD COLUMN ban_reason TEXT''',
    #     '''ALTER TABLE "Продавцы" ADD COLUMN block_date TIMESTAMP''',
    #     '''ALTER TABLE "Пользователи" ADD COLUMN is_banned BOOLEAN DEFAULT FALSE''',
    #     # Используйте кавычки, если имя таблицы является зарезервированным словом
    #     '''ALTER TABLE "Пользователи" ADD COLUMN ban_reason TEXT''',
    #     '''ALTER TABLE "Пользователи" ADD COLUMN block_date TIMESTAMP''',
    #     '''DROP TABLE IF EXISTS banneduser''',
    #     '''DROP TABLE IF EXISTS bannedseller''',
    #     '''ALTER TABLE ViewedMailing ADD COLUMN send_datetime timestamp DEFAULT current_timestamp''',
    #     '''ALTER TABLE carcomplectation ADD COLUMN wired_state_id INTEGER REFERENCES carstate(id) ON DELETE SET NULL'''
    # ]
    #
    # # Выполнение команд
    # for command in alter_table_commands:
    #     database.execute_sql(command)
    # await message.answer('finish')
