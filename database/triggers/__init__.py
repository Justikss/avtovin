import logging

from . import phonenumber_unique_controller



async def create_trigger_unique_phone_number(manager):
    sql_create_function = """
    CREATE OR REPLACE FUNCTION unique_phone_number()
    RETURNS TRIGGER AS $$
    DECLARE
        phone TEXT;
    BEGIN
        FOREACH phone IN ARRAY NEW.phone_number
        LOOP
            IF (SELECT COUNT(*) FROM продавцы WHERE phone_number @> ARRAY[phone]) > 0 THEN
                RAISE EXCEPTION 'Номер телефона % уже существует в таблице', phone;
            END IF;
        END LOOP;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """

    sql_create_trigger = """
    CREATE TRIGGER check_phone_number_uniqueness
    BEFORE INSERT OR UPDATE ON продавцы
    FOR EACH ROW EXECUTE FUNCTION unique_phone_number();
    """

    await manager.execute_sql(sql_create_function)
    await manager.execute_sql(sql_create_trigger)
    logging.info('Триггер unique_phone_number подключён')