from abc import ABC, abstractmethod

from database_sync.domain.entities.settings import Ignore


class DatabaseService(ABC):
    @abstractmethod
    def list_tables(self, database: str) -> list[str]:
        pass

    @abstractmethod
    def list_sequences(self, database: str) -> list[str]:
        pass

    @abstractmethod
    def list_views(self, database: str) -> list[str]:
        pass

    @abstractmethod
    def drop_tables(self, database: str, tables: list[str]) -> None:
        pass

    @abstractmethod
    def drop_sequences(self, database: str, sequences: list[str]) -> None:
        pass

    @abstractmethod
    def drop_views(self, database: str, views: list[str]) -> None:
        pass

    @abstractmethod
    def export(self, database: str, ignore: list[Ignore]) -> None:
        pass

    @abstractmethod
    def restore(self, database: str) -> None:
        pass

    @abstractmethod
    def connect(self, database: str) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass
