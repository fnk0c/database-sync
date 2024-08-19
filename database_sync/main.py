import logging

from database_sync.domain.commands.sync_command import SyncCommand
from database_sync.domain.entities.settings import Settings
from database_sync.domain.services.database_service import DatabaseService
from database_sync.infrastructure.helpers.psql_connector import PsqlConnector
from database_sync.infrastructure.repositories.env_settings_repository import (
    EnvSettingsRepository,
)
from database_sync.infrastructure.services.psql_database_service import (
    PsqlDatabaseService,
)


class Main:
    def __logger(self) -> logging.Logger:
        msg_format = "%(asctime)s %(levelname)-8s %(name)-10s : %(message)s"

        logger = logging.getLogger("database_sync")
        logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter(msg_format))
        logger.addHandler(ch)
        logger.info("logger configured")

        return logger

    def __instantiate_services(
        self, settings: Settings
    ) -> tuple[DatabaseService, DatabaseService]:
        prod_connection = PsqlConnector(settings.production)
        dev_connection = PsqlConnector(settings.development)

        prod_db_service = PsqlDatabaseService(prod_connection)
        dev_db_service = PsqlDatabaseService(dev_connection)

        return prod_db_service, dev_db_service

    def start(self) -> None:
        logger = self.__logger()
        logger.info("getting execution settings and definitions")
        settings = EnvSettingsRepository().get_env_settings()
        prod_db_service, dev_db_service = self.__instantiate_services(settings)
        command = SyncCommand(prod_service=prod_db_service, dev_service=dev_db_service)
        logger.info("starting sync command")
        command.execute(settings.targets, settings.ignore)
        logger.info("sync command finished")


def main() -> None:
    Main().start()
