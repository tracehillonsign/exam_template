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