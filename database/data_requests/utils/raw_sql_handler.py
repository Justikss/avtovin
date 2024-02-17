
import aiopg

async def execute_raw_sql(query, fetch='all'):
    from database.db_connect import connect_data

    async with aiopg.create_pool(f'''postgresql://{connect_data['user']}:{connect_data['password']}@{connect_data['host']}:{connect_data['port']}/{connect_data['database']}''') as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query)
                match fetch:
                    case 'one':
                        result_row = await cur.fetchone()
                    case _:
                        result_row = await cur.fetchall()
                return result_row