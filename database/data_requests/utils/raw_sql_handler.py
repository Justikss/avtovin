
import aiopg

async def get_top_advert_parameters(query):
    async with aiopg.create_pool('postgresql://postgres:red12red1212@localhost:5432/postgresDB') as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query)
                return [dict(row) for row in await cur.fetchall()]