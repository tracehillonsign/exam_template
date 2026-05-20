import subprocess

def setup_dependencies():
	result = subprocess.run(['pip', 'install', 'PyQt6', 'pymysql'], capture_output=True, text=True, encoding='utf-8')

	if result.returncode == 0:
		print("[setup_dependencies] Зависимости установлены.")
		return 0
	else:
		print(f"[setup_dependencies] Неивестная ошибка установки: `{result.returncode}`.")
		print("[setup_dependencies] Попробуйте установить их командой: `pip install PyQt6 pymysql`")
		return 1

def write_file(name: str, content: str):
	with open(name, "wb") as file:
		file.write(content.encode("UTF-8"))

def main():
	setup_dependencies()
	
	write_file("database.py", DATABASE_CONTENT)
	write_file("interface.py", INTERFACE_CONTENT)
	write_file("main.py", MAIN_CONTENT)

	print("[main] Установка шаблона закончена.")

DATABASE_CONTENT = '''
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
'''

INTERFACE_CONTENT = '''
from PyQt6.QtWidgets import *

from database import db

COLUMN_COUNT = 0
HORIZONAL_LABELS = ["..", "..."]

class App(QWidget):
	def __init__(self):
		super().__init__()

		layout = QHBoxLayout()
		self.setLayout(layout)

		self.table = QTableWidget()
		self.table.setColumnCount(COLUMN_COUNT)
		self.table.setHorizontalHeaderLabels(HORIZONAL_LABELS)
		layout.addWidget(self.table)

		self.setup_table()

	def setup_table(self):
		self.table.setRowCount(0)

		""" Тут вы вставляйте нужный вам метод из базы данных. """
		records = db.YOUR_METHOD()
		for row, record in enumerate(records):
			self.table.insertRow(row)

			"""
				Второе чисто это порядковый номер столбца.
				В случае если нужно вставить число в таблицу то его нужно привести к строке.
			"""
			self.table.setItem(row, 0, QTableWidgetItem(str(record[0])))
'''

MAIN_CONTENT = '''
import sys
from PyQt6.QtWidgets import QApplication

from interface import App

def main():
	app = QApplication(sys.argv)
	window = App()
	window.show()
	sys.exit(app.exec())
	
if __name__ == "__main__":
	main()
'''

if __name__ == "__main__":
	print("Начало работы скрипта.")
	main()
	print("Конец работы скрипта.")