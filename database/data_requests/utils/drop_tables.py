import asyncio

from peewee import RawQuery

from database.db_connect import manager, database


async def drop_tables_except_one(table_to_keep):
    query = """
    DO $$
    DECLARE
        r RECORD;
    BEGIN
        FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename != %s)
        LOOP
            EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
        END LOOP;
    END
    $$;
    """
    database.execute_sql(query, params=(table_to_keep,))