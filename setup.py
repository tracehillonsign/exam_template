import sys
import subprocess
import argparse
from pathlib import Path


def setup_dependencies():
    print("[setup_dependencies] Начало установки зависимостей.")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "PyQt6", "pymysql"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )

        if result.returncode == 0:
            print("[setup_dependencies] Зависимости успешно установлены.")
            return 0
        else:
            print(
                f"[setup_dependencies] Ошибка установки (код {result.returncode}).\n"
                f"stdout: {result.stdout}\nstderr: {result.stderr}"
            )

            print(
                "[setup_dependencies] Попробуйте установить вручную: "
                f"{sys.executable} -m pip install PyQt6 pymysql"
            )
            return 1
    except Exception as e:
        print(f"[setup_dependencies] Не удалось запустить pip: {e}")
        return 2


def write_file(filename: str, content: str):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"[write_file] Файл '{filename}' создан.")
        return True
    except OSError as e:
        print(f"[write_file] Ошибка записи '{filename}': {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description=">> ? <<")
    parser.add_argument("--no-deps", action="store_true")

    args = parser.parse_args()

    """
	TODO:
		Создать логику для no_deps и skip-err.
	"""
    if not args.no_deps:
        if setup_dependencies() != 0:
            pass

    files = [
        ("main.py", MAIN_CONTENT),
        ("config.ini", CONFIG_CONTENT),
        ("src/interface.py", INTERFACE_CONTENT),
        ("src/database.py", DATABASE_CONTENT),
        ("src/utils.py", UTILS_CONTENT),
    ]

    Path("src").mkdir(exist_ok=True)

    success = True
    for name, content in files:
        if not write_file(name, content):
            success = False

    if success:
        print("[main] Установка шаблона закончена успешно.")
        return 0
    else:
        print("[main] Установка шаблона завершена с ошибками записи.")
        return 1


CONFIG_CONTENT = """
[database]
# Адрес сервера на котором находится БД.
host = localhost
# Имя пользователя.
user = root
# Пароль пользователя. Если пароля нет, оставьте пустым.
password =
# Название БД для подключения.
name =

[table]
# Количество столбцов выходной таблицы
columns = 1
# Имена колонок в формате: names = column1, column2, ...
names =
"""

MAIN_CONTENT = """
import sys
from PyQt6.QtWidgets import QApplication

from src.interface import App


def main():
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
"""

DATABASE_CONTENT = """
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

db = Database()
"""

INTERFACE_CONTENT = '''
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

        """INSERT DATA: установить нужный метод БД"""
        raw = db.YOUR_METHOD()

        for row, content in enumerate(raw):
            self.table.insertRow(row)

            """INSERT DATA: установить нужные столбцы вывода"""
            self.table.setItem(row, 0, QTableWidgetItem(str(content[0])))
            self.table.setItem(row, 1, QTableWidgetItem(content[1]))
'''

UTILS_CONTENT = '''
"""
Данный модуль, как и конфигурационный файл, не предназначены для использоваения
        на самом экзамене.

В данном случае они нужны только для упрощения настройки шаблона.
"""

import configparser
from dataclasses import dataclass
from typing import List


@dataclass
class DatabaseConf:
    host: str
    user: str
    password: str
    name: str


@dataclass
class TableConf:
    columns: int
    names: List[str]


@dataclass
class Config:
    database: DatabaseConf
    table: TableConf


def get_config() -> Config:
    config = configparser.ConfigParser()
    config.read("config.ini", encoding="utf-8")

    db_setup = DatabaseConf(
        host=config["database"]["host"],
        user=config["database"]["user"],
        password=config["database"]["password"],
        name=config["database"]["name"],
    )

    names_raw = config["table"].get("names", "")

    if names_raw.strip():
        names_list = [name.strip() for name in names_raw.split(",")]
    else:
        names_list = []

    table_setup = TableConf(columns=config.getint("table", "columns"), names=names_list)

    return Config(database=db_setup, table=table_setup)
'''

if __name__ == "__main__":
    print("Начало работы скрипта.")
    return_code = main()
    print("ВАЖНО: Перед началом использования настройте 'config.ini'. Что бы избежать проблем после написания кода.")
    print("Конец работы скрипта.")
    sys.exit(return_code)
