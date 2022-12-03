import log
from bot.db import sql_connect


def get_user_info(user_id, tg_id):
    conn = sql_connect.create_connection()
    cursor = conn.cursor()

    if user_id is None and tg_id is None:
        log.logger.error("Can't get user info without arguments")
        return

    cursor.execute("""
        SELECT user_id, tg_id, message_format, exclude_banks, exclude_methods
        FROM user 
        WHERE (user_id = ? or tg_id = ?) and deleted_flg = '0'
        """, (user_id, tg_id))
    row = cursor.fetchone()

    if row is None:
        log.logger.error("user_id: " + str(user_id) + " tg_id: " + str(tg_id) + " does not exist")

    cursor.close()
    conn.close()
    return row
