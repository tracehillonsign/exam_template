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
        raw = db.get_all_users()

        for row, content in enumerate(raw):
            self.table.insertRow(row)
            for column, value in enumerate(content):
                self.table.setItem(row, column, QTableWidgetItem(str(value)))