import pymysql

from src.utils import get_config

config = get_config()


class Database:
    def __init__(self):
        self.connect = pymysql.connect(
            host=config.database.host,
            user=config.database.user,
            password=config.database.password,
            database=config.database.name,
        )

    def close(self):
        self.connect.close()

    def get_all_users(self):
        with self.connect.cursor() as cursor:
            cursor.execute("select id, first_name from employees;")
            return cursor.fetchall()


db = Database()
