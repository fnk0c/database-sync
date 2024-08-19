import os

from dotenv import load_dotenv
from yaml import safe_load

from database_sync.domain.entities.settings import DatabaseConnection, Ignore, Settings


class EnvSettingsRepository:
    def __init__(self) -> None:
        load_dotenv()

    def __get_prod(self) -> DatabaseConnection:
        return DatabaseConnection(
            host=os.environ["PRODUCTION_HOST"],
            port=int(os.environ["PRODUCTION_PORT"]),
            user=os.environ["PRODUCTION_USERNAME"],
            password=os.environ["PRODUCTION_PASSWORD"],
        )

    def __get_dev(self) -> DatabaseConnection:
        return DatabaseConnection(
            host=os.environ["DEVELOPMENT_HOST"],
            port=int(os.environ["DEVELOPMENT_PORT"]),
            user=os.environ["DEVELOPMENT_USERNAME"],
            password=os.environ["DEVELOPMENT_PASSWORD"],
        )

    def __get_ingnore_list(self) -> list[Ignore]:
        with open(os.environ["CONFIG_FILE_PATH"]) as f:
            data = safe_load(f)

        return [
            Ignore(database=db["database"], tables=db["tables"])
            for db in data["ignore"]
        ]

    def __get_sync_target(self) -> list[str]:
        databases = os.environ["SYNC_TARGETS"]
        return [db.strip() for db in databases.split(",")]

    def get_env_settings(self) -> Settings:
        return Settings(
            production=self.__get_prod(),
            development=self.__get_dev(),
            ignore=self.__get_ingnore_list(),
            targets=self.__get_sync_target(),
        )
