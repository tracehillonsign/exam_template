import pymysql as sql

DATABASE_NAME = "shop"
DATABASE_PASSWORD = ""

class Database:
	def __init__(self):
		self.connect = sql.connect(
			host="localhost",
			user="root",
			password=DATABASE_PASSWORD,
			database=DATABASE_NAME
		)

	def close(self):
		self.connect.close()

	def get_users(self):
		""" Пример простейшего запроса на получение данных. """
		with self.connect.cursor() as cursor:
			cursor.execute("SELECT id, first_name FROM employees")
			return cursor.fetchall()

db = Database()