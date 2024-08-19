from faker import Faker

from database_sync.domain.entities.settings import Ignore
from database_sync.domain.services.database_service import DatabaseService


class InMemoryDatabaseServiceStub(DatabaseService):
    def __init__(self) -> None:
        fake = Faker()
        self.__views = [fake.word() for _ in range(5)]
        self.__sequences = [fake.word() for _ in range(5)]
        self.__tables = [fake.word() for _ in range(5)]

    def with_views(self, views: list[str]) -> "InMemoryDatabaseServiceStub":
        self.__views = views
        return self

    def with_sequences(self, sequences: list[str]) -> "InMemoryDatabaseServiceStub":
        self.__sequences = sequences
        return self

    def with_tables(self, tables: list[str]) -> "InMemoryDatabaseServiceStub":
        self.__tables = tables
        return self

    def list_tables(self, database: str) -> list[str]:
        return self.__tables

    def list_sequences(self, database: str) -> list[str]:
        return self.__sequences

    def list_views(self, database: str) -> list[str]:
        return self.__views

    def drop_tables(self, database: str, tables: list[str]) -> None:
        pass

    def drop_sequences(self, database: str, sequences: list[str]) -> None:
        pass

    def drop_views(self, database: str, views: list[str]) -> None:
        pass

    def export(self, database: str, ignore: list[Ignore]) -> None:
        pass

    def restore(self, database: str) -> None:
        pass

    def connect(self, database: str) -> None:
        pass

    def disconnect(self) -> None:
        pass
