
import aiopg

async def execute_raw_sql(query):
    async with aiopg.create_pool('postgresql://postgres:red12red1212@localhost:5432/postgresDB') as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query)
                result_row = await cur.fetchone()
                return result_row