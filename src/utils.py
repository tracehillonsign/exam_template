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

    table_setup = TableConf(columns=len(names_list), names=names_list)

    return Config(database=db_setup, table=table_setup)
