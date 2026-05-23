import pymysql

from src.utils import get_config

config = get_config()

SELECT_QUERY = "SELECT id, first_name FROM employees"
VIEW = "SELECT * FROM shop.view_test"


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
        """
        Простой вызов SELECT.

        SELECT id, first_name
        FROM employees
        """
        with self.connect.cursor() as cursor:
            cursor.execute(SELECT_QUERY)
            return cursor.fetchall()

    def view(self):
        """
        Вызов VIEW.

        CREATE VIEW `view_test` AS
        SELECT id, first_name
        FROM employees;
        """
        with self.connect.cursor() as cursor:
            cursor.execute(VIEW)
            return cursor.fetchall()

    def procedure_no_args_query(self):
        """
        Вызов хранимой процедуры без аргументов.

        CREATE PROCEDURE `procedure_no_args`()
        BEGIN
            SELECT id, first_name
            FROM employees;
        END
        """
        with self.connect.cursor() as cursor:
            cursor.callproc("procedure_no_args")
            return cursor.fetchall()

    def procedure_with_args(self):
        """
        Вызов процедуры с входным аргументом.

        CREATE PROCEDURE `procedure_with_args`(IN emp_id INT)
        BEGIN
            SELECT id, first_name
            FROM employees
            WHERE id = emp_id;
        END
        """
        with self.connect.cursor() as cursor:
            emp_id = 2
            args = (emp_id,)
            cursor.callproc("procedure_with_args", args)
            return cursor.fetchall()

    def procedure_with_args_and_return(self):
        """
        Вызов процедуры с входным и выходным параметрами.

        CREATE PROCEDURE `procedure_with_args_and_return`(IN emp_id INT, OUT p_first_name VARCHAR(255))
        BEGIN
            SELECT first_name INTO p_first_name
            FROM employees
            WHERE id = emp_id;
        END
        """
        with self.connect.cursor() as cursor:
            emp_id = 1
            # 0 используется как заглушка для OUT параметра.
            args = (emp_id, 0)
            cursor.callproc("procedure_with_args_and_return", args)
            """
            SELECT @_procedure_with_args_and_return_1

            Цифра 1 в вызове процедуры означает позицию выходного параметра:
            emp_id - 0
            p_first_name - 1
            """
            cursor.execute("SELECT @_procedure_with_args_and_return_1")
            return cursor.fetchall()

    def function_with_args(self):
        """
        Вызов хранимой функции с входным параметром.

        CREATE FUNCTION `сals_values`(a INT, b INT) RETURNS int
        BEGIN
            RETURN a + b;
        END

        Важный момент: хранимая функция может возвращать только 1 параметр из 1 записи.
        Если нужно вернуть более сложный обект то для этого надо использовать JSON или CONCAT,
            но в таком слуае уже проще использовать процедуру если входные параметры таие сложные.
        """
        with self.connect.cursor() as cursor:
            first_value = 1
            second_value = 2
            args = (first_value, second_value)
            cursor.execute("SELECT сals_values(%s, %s)", args)
            return cursor.fetchall()


db = Database()
