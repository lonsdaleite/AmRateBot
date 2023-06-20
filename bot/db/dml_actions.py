from datetime import datetime

import const
import log
from bot.db import sql_connect


def update_user_info(user_id, tg_id=None, message_format=None, exclude_banks=None, exclude_methods=None):
    if user_id is None:
        log.logger.error("Can not add a user info without user_id")
        return

    if tg_id is None and message_format is None and exclude_banks is None and exclude_methods is None:
        log.logger.error("Can't update user_id: " + str(user_id) + " info. No arguments passed.")
        return

    conn = sql_connect.create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT count(*) 
        FROM user 
        WHERE user_id = ? and deleted_flg = '0'
        """, (user_id,))

    if cursor.fetchone()[0] == 0:
        log.logger.error("user_id " + str(user_id) + " does not exist")
        cursor.close()
        conn.close()
        return

    if tg_id is not None:
        cursor.execute("""
            UPDATE user
            SET tg_id = ?
            WHERE user_id = ? and deleted_flg = '0'
            """, (tg_id, user_id))

    if message_format is not None:
        cursor.execute("""
            UPDATE user
            SET message_format = ?
            WHERE user_id = ? and deleted_flg = '0'
            """, (message_format, user_id))

    if exclude_banks is not None:
        if len(exclude_banks) == 0:
            exclude_banks_str = None
        else:
            exclude_banks_str = ",".join(exclude_banks)
        cursor.execute("""
            UPDATE user
            SET exclude_banks = ?
            WHERE user_id = ? and deleted_flg = '0'
            """, (exclude_banks_str, user_id))

    if exclude_methods is not None:
        if len(exclude_methods) == 0:
            exclude_methods_str = None
        else:
            exclude_methods_str = ",".join(exclude_methods)
        cursor.execute("""
            UPDATE user
            SET exclude_methods = ?
            WHERE user_id = ? and deleted_flg = '0'
            """, (exclude_methods_str, user_id))

    log.logger.info("user_id: " + str(user_id) + " tg_id: " + str(tg_id) + " info updated")

    conn.commit()
    cursor.close()
    conn.close()


def disable_user(user_id):
    if user_id is None:
        log.logger.error("Can not disable user without user_id")
        return

    conn = sql_connect.create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE user
        SET deleted_flg = '1'
        WHERE user_id = ?
        """, (user_id, ))

    log.logger.info("user_id: " + str(user_id) + " disabled")

    conn.commit()
    cursor.close()
    conn.close()


def add_user(tg_id=None):
    if tg_id is None:
        log.logger.error("Can not add a user without telegram id")
        return

    conn = sql_connect.create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, deleted_flg
        FROM user 
        WHERE tg_id = ?
        """, (tg_id,))

    row = cursor.fetchone()

    if row is None:
        cursor.execute("""
            SELECT coalesce(max(user_id), 0) + 1 
            FROM user 
            """)
        user_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO user (
               user_id, tg_id, message_format, exclude_banks, exclude_methods, deleted_flg, processed_dttm) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, tg_id, 'short',
                  ",".join(const.DEFAULT_EXCLUDE_BANKS), ",".join(const.DEFAULT_EXCLUDE_METHODS), '0', datetime.now()))

        log.logger.info("user_id: " + str(user_id) + " tg_id: " + str(tg_id) + " added")
    elif row['deleted_flg'] == '0':
        log.logger.error("tg_id: " + str(tg_id) + " already exists")
        cursor.close()
        conn.close()
        return None
    elif row['deleted_flg'] == '1':
        cursor.execute("""
            UPDATE user
            SET deleted_flg = '0'
            WHERE tg_id = ?
            """, (tg_id,))

        user_id = row['user_id']
        log.logger.info("tg_id: " + str(tg_id) + " enabled")

    conn.commit()
    cursor.close()
    conn.close()

    return user_id
