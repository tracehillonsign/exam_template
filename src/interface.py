from PyQt6.QtWidgets import *

from src.database import db
from src.utils import get_config

config = get_config()


class App(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.table = QTableWidget()
        self.table.setColumnCount(config.table.columns)
        self.table.setHorizontalHeaderLabels(config.table.names)
        layout.addWidget(self.table)

        self.setup_table()

    def setup_table(self):
        self.table.setRowCount(0)
        users = db.get_all_users()

        for row, user in enumerate(users):
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(str(user[0])))
            self.table.setItem(row, 1, QTableWidgetItem(user[1]))
