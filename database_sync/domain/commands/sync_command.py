import logging
from dataclasses import dataclass

from database_sync.domain.entities.database import Database
from database_sync.domain.entities.settings import Ignore
from database_sync.domain.services.database_service import DatabaseService


@dataclass
class Services:
    prod: DatabaseService
    dev: DatabaseService


class SyncCommand:
    def __init__(
        self, prod_service: DatabaseService, dev_service: DatabaseService
    ) -> None:
        self.__services = Services(prod=prod_service, dev=dev_service)
        self.__logger = logging.getLogger("database_sync")

    def __extract_db_info(self, database: str, prod: bool = True) -> Database:
        if prod:
            self.__logger.info(
                f"extracting data from '{database}' on production environment"
            )
            service = self.__services.prod
        else:
            self.__logger.info(
                f"extracting data from '{database}' on development environment"
            )
            service = self.__services.dev

        return Database(
            tables=service.list_tables(database),
            sequences=service.list_sequences(database),
            views=service.list_views(database),
        )

    def __find_orphans(self, production: Database, development: Database) -> Database:
        orphan_tables = list(
            filter(lambda table: table not in production.tables, development.tables)
        )
        orphan_seqs = list(
            filter(lambda seq: seq not in production.sequences, development.sequences)
        )
        orphan_views = list(
            filter(lambda view: view not in production.views, development.views)
        )

        return Database(tables=orphan_tables, sequences=orphan_seqs, views=orphan_views)

    def __clean_database(
        self,
        database: str,
        production: Database,
        orphans: Database,
        ignore: list[Ignore],
    ) -> None:
        self.__logger.info(f"dropping tables, sequences and views for '{database}'")
        all_tables = production.tables + orphans.tables
        all_sequences = production.sequences + orphans.sequences
        all_views = production.views + orphans.views

        for ignored in ignore:
            if database != ignored.database:
                continue
            for table in ignored.tables:
                if table in all_tables:
                    all_tables.remove(table)

        self.__services.dev.drop_tables(database, all_tables)
        self.__services.dev.drop_sequences(database, all_sequences)
        self.__services.dev.drop_views(database, all_views)

    def __sync_database(
        self,
        database: str,
        ignore: list[Ignore],
        production: Database,
        orphans: Database,
    ) -> None:
        self.__logger.info(f"exporting data for '{database}'")
        self.__services.prod.export(database, ignore)
        self.__clean_database(database, production, orphans, ignore)
        self.__logger.info(f"restoring data for '{database}'")
        self.__services.dev.restore(database)
        self.__logger.info(f"sync done for '{database}'")

    def execute(self, targets: list[str], ignore: list[Ignore]) -> bool:
        for database in targets:
            # Connects to target database
            self.__logger.info(f"connecting to '{database}'")
            self.__services.dev.connect(database)
            self.__services.prod.connect(database)

            # TODO: Check if is needed to have prod data
            prod_data = self.__extract_db_info(database)
            dev_data = self.__extract_db_info(database, prod=False)
            dev_orphans = self.__find_orphans(prod_data, dev_data)

            self.__sync_database(database, ignore, prod_data, dev_orphans)

            # Disconnects from target database
            self.__logger.info(f"disconnecting from '{database}'")
            self.__services.dev.disconnect()
            self.__services.prod.disconnect()

        return True
