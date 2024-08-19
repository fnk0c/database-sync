import logging
import os
from subprocess import PIPE, Popen
from time import sleep

import psycopg2

from database_sync.domain.entities.settings import DatabaseConnection


class PsqlConnector:
    def __init__(self, settings: DatabaseConnection) -> None:
        self.__settings = settings
        self.__logger = logging.getLogger("database_sync")

    def open_connection(self, database: str) -> psycopg2.connect:
        return psycopg2.connect(
            host=self.__settings.host,
            port=self.__settings.port,
            user=self.__settings.user,
            password=self.__settings.password,
            dbname=database,
        )

    def __set_pgpassword(self) -> None:
        os.environ["PGPASSWORD"] = self.__settings.password

    def __wait_for_process(self, process: Popen) -> None:
        while process.poll() is None:
            self.__logger.debug("waiting for dump to finish")
            sleep(2)  # nosemgrep: python.lang.best-practice.sleep.arbitrary-sleep

    def dump(self, database: str, extend_command: list[str], redirect_to: str) -> bool:
        success = True
        self.__set_pgpassword()
        connection_command: list[str] = [
            "pg_dump",
            "-h",
            self.__settings.host,
            "-p",
            str(self.__settings.port),
            "-U",
            self.__settings.user,
        ]
        target_command: list[str] = ["-Fc", database]
        command = connection_command + extend_command + target_command
        self.__logger.info(f"executing command: {' '.join(command)}")
        with open(redirect_to, "w") as f:
            result = Popen(command, stdout=f)

        self.__wait_for_process(result)
        if result.returncode != 0:
            self.__logger.error(f"failed to dump '{database}'")
            success = False

        return success

    def restore(self, database: str) -> int:
        command = [
            "pg_restore",
            "-h",
            self.__settings.host,
            "-p",
            str(self.__settings.port),
            "-U",
            self.__settings.user,
            "-d",
            database,
            f"{database}.dump",
        ]
        self.__logger.info(f"executing command: {' '.join(command)}")
        result = Popen(command, stdout=PIPE)
        self.__wait_for_process(result)

        return result.returncode
