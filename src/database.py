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

    def simple_select_query(self):
        with self.connect.cursor() as cursor:
            cursor.execute(SELECT_QUERY)
            return cursor.fetchall()
        
    def view_no_args_query(self):
        with self.connect.cursor() as cursor:
            cursor.execute(VIEW_NO_ARGS_QUERY)
            return cursor.fetchall()
        
    def procedure_no_args_query(self):
        with self.connect.cursor() as cursor:
            cursor.callproc("procedure_no_args")
            return cursor.fetchall()

    def procedure_with_args(self):
        with self.connect.cursor() as cursor:
            emp_id = 2
            args = (emp_id,)
            cursor.callproc("procedure_with_args", args)
            return cursor.fetchall()

    def procedure_with_args_and_return(self):
        with self.connect.cursor() as cursor:
            emp_id = 1
            # 0 используется как заглушка для OUT параметра.
            args = (emp_id, 0)
            cursor.callproc("procedure_with_args_and_return", args)
            cursor.execute("SELECT @_procedure_with_args_and_return_1")
            return cursor.fetchall()

    def function_with_args(self):
        with self.connect.cursor() as cursor:
            first_value = 1
            second_value = 2
            args = (first_value, second_value)
            cursor.execute("SELECT сals_values(%s, %s)", args)
            return cursor.fetchall()


db = Database()

SELECT_QUERY = """
SELECT id, first_name
FROM employees
"""

VIEW_NO_ARGS_QUERY = """
SELECT * FROM shop.view_no_args;
"""