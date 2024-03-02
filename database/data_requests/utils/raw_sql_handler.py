import logging

import aiopg


async def execute_raw_sql(query, args=None, fetch='all', transaction=False):
    from database.db_connect import connect_data

    async with aiopg.create_pool(f'''postgresql://{connect_data['user']}:{connect_data['password']}@{connect_data['host']}:{connect_data['port']}/{connect_data['database']}''') as pool:
        async with pool.acquire() as conn:
            # Создаем курсор
            async with conn.cursor() as cur:
                # Если требуется транзакция, начинаем ее вручную
                if transaction:
                    await cur.execute("BEGIN")
                # Выполняем запрос
                await cur.execute(query, args)
                # Обработка возвращаемого результата
                if fetch == 'one':
                    result_row = await cur.fetchone()
                elif fetch == 'count':
                    result_row = cur.rowcount  # Возвращает количество обработанных строк
                else:
                    result_row = await cur.fetchall()

                # Если использовалась транзакция, подтверждаем изменения
                if transaction:
                    await cur.execute("COMMIT")

                logging.debug('Raw SQL handled: %s [%s]\nresult: %s', query, args, result_row)
                return result_row

async def execute_query(cur, query, args, fetch):
    await cur.execute(query, args)  # Используйте args для параметризованных запросов
    match fetch:
        case 'one':
            return await cur.fetchone()
        case 'count':
            return cur.rowcount  # Возвращает количество обработанных строк
        case _:
            return await cur.fetchall()
