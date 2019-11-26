# import sqlite3
import pymysql
from decouple import config
import logging


logger = logging.getLogger('warframe')

def u_prefix(_id, prefix):
    cur = conn.cursor()
    sql = """UPDATE guild_settings SET prefix=%s WHERE id=%s"""
    cur.execute(sql, (prefix, _id,))
    conn.commit()
    cur.close()
    
def i_prefix(values):
    cur = conn.cursor()
    sql = """INSERT INTO guild_settings(id, prefix) VALUES(%s, %s)"""
    cur.execute(sql, values)
    conn.commit()
    cur.close()

def read_prefix(_id: int):
    cur = conn.cursor()
    sql = """SELECT prefix FROM guild_settings WHERE id=%s"""
    cur.execute(sql, (_id,))
    rows = cur.fetchall()[0][0]
    cur.close()
    return rows

def read_settings(_id):
    sql = """SELECT to_delete, delay FROM guild_settings WHERE id=%s"""
    cur = conn.cursor()
    cur.execute(sql, (_id,))
    rows = cur.fetchall()[0]
    cur.close()
    return rows[0], rows[1]

def i_guild_settings(_id: int, prefix: str, to_delete: int, delay: int):
    cur = conn.cursor()
    sql = """INSERT INTO guild_settings(id, prefix, to_delete, delay)
    VALUES(%s, %s, %s, %s)"""
    cur.execute(sql, (_id, prefix, to_delete, delay, ))
    conn.commit()
    cur.close()

def read_table(*selector):
    selector = ', '.join(selector)
    sql = """SELECT %s FROM `guild_settings`"""
    cur = conn.cursor()
    cur.execute(sql, (selector,))
    conn.commit()
    rows = cur.fetchall()
    cur.close()
    return rows

def u_guild_settings(_id: int, to_delete: int, delay: int):
    cur = conn.cursor()
    sql = """UPDATE guild_settings SET 
            to_delete=%s,
            delay=%s
            WHERE id=%s"""
    cur.execute(sql, (to_delete, delay, _id, ))
    conn.commit()
    cur.close()

def d_guild(_id):
    cur = conn.cursor()
    sql = """DELETE FROM guild_settings WHERE id=%s"""
    cur.execute(sql, (_id,))
    logger.info(_id, 'removed')
    conn.commit()
    cur.close()

try:
    conn = pymysql.connect(
                    host=config('db_host'),
                    user=config('user'),
                    password=config('password'),
                    db=config('db')
                    )
except pymysql.Error as error:
    logger.error(error, exc_info=True)
    logger.info('Connection closed')
