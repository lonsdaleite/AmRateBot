import sqlite3
import bot.config


def create_connection():
    conn = sqlite3.connect(bot.config.SQLITE3_DB)
    conn.row_factory = sqlite3.Row
    return conn
