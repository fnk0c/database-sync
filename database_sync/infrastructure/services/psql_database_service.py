import logging

import psycopg2

from database_sync.domain.entities.settings import Ignore
from database_sync.domain.services.database_service import DatabaseService
from database_sync.infrastructure.helpers.psql_connector import PsqlConnector
from database_sync.infrastructure.services.mappers.psql_mapper import PsqlMapper


class PsqlDatabaseService(DatabaseService):
    def __init__(self, connector: PsqlConnector) -> None:
        self.__connector = connector
        self.__cursor: psycopg2.cursor = None  # type: ignore
        self.__connection: psycopg2.extensions.connection = None  # type: ignore
        self.__logger = logging.getLogger("database_sync")

    def __execute_query(self, query: str) -> None:
        self.__logger.info(f"query: {query}")
        self.__cursor.execute(query)
        self.__connection.commit()

    def __execute_fetch(self, query: str) -> list[tuple]:
        self.__cursor.execute(query)
        data = self.__cursor.fetchall()
        return data

    def list_tables(self, database: str) -> list[str]:
        query = (
            "SELECT tablename FROM pg_tables "
            "WHERE schemaname = 'public' ORDER BY tablename;"
        )
        return PsqlMapper.map_to_list(self.__execute_fetch(query))

    def list_sequences(self, database: str) -> list[str]:
        query = (
            "SELECT sequence_name FROM information_schema.sequences "
            "WHERE sequence_schema = 'public'"
        )
        return PsqlMapper.map_to_list(self.__execute_fetch(query))

    def list_views(self, database: str) -> list[str]:
        query = (
            "select table_name from information_schema.views where "
            "table_schema = 'public' ORDER BY table_name"
        )
        return PsqlMapper.map_to_list(self.__execute_fetch(query))

    def drop_tables(self, database: str, tables: list[str]) -> None:
        for table in tables:
            query = f"DROP TABLE IF EXISTS {table} CASCADE;"
            self.__execute_query(query)

    def drop_sequences(self, database: str, sequences: list[str]) -> None:
        for sequence in sequences:
            query = f"DROP SEQUENCE IF EXISTS {sequence} CASCADE;"
            self.__execute_query(query)

    def drop_views(self, database: str, views: list[str]) -> None:
        for view in views:
            query = f"DROP VIEW IF EXISTS {view} CASCADE;"
            self.__execute_query(query)

    def export(self, database: str, ignore: list[Ignore]) -> None:
        ignore_command = []

        for entry in ignore:
            if entry.database != database:
                continue
            for table in entry.tables:
                self.__logger.warning(f"ignoring table '{table}' on export")
                ignore_command += ["--exclude-table", table]

        content = self.__connector.dump(database, ignore_command, f"{database}.dump")

        if not content:
            raise Exception("Error while dumping database")

    def restore(self, database: str) -> None:
        self.__connector.restore(database)

    def connect(self, database: str) -> None:
        self.__connection = self.__connector.open_connection(database)
        self.__cursor = self.__connection.cursor()

    def disconnect(self) -> None:
        self.__cursor.close()
