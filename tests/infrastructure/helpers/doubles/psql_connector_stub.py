from __future__ import annotations

import psycopg2
from faker import Faker
from faker.providers import misc

from database_sync.infrastructure.helpers.psql_connector import PsqlConnector


class Psycopg2Mock:
    def __init__(self) -> None:
        self.__data = []

    def with_data(self, data: list[tuple]) -> Psycopg2Mock:
        self.__data = data
        return self

    def connect(self, **kwargs: str) -> Psycopg2Mock:
        return self

    def cursor(self) -> Psycopg2Mock:
        return self

    def fetchall(self) -> list[tuple]:
        return self.__data

    def execute(self, *args: str) -> None:
        pass

    def commit(self) -> None:
        pass


class InMemoryPsqlConnector(PsqlConnector):
    def __init__(self) -> None:
        self.__fake = Faker()
        self.__fake.add_provider(misc)
        self.__dump_status = True
        self.__connection = Psycopg2Mock()

    def with_data(self, data: list[tuple]) -> InMemoryPsqlConnector:
        self.__connection.with_data(data)
        return self

    def with_dump_error(self) -> InMemoryPsqlConnector:
        self.__dump_status = False
        return self

    def open_connection(self, database: str) -> psycopg2.connect:
        return self.__connection

    def dump(self, database: str, extend_command: list[str], redirect_to: str) -> bool:
        if self.__dump_status:
            with open(redirect_to, "w") as f:
                f.write(self.__fake.unique.text())

        return self.__dump_status

    def restore(self, database: str) -> int:
        return self.__fake.unique.random_int()
