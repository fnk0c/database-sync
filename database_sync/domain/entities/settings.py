from dataclasses import dataclass


@dataclass
class DatabaseConnection:
    host: str
    port: int
    user: str
    password: str


@dataclass
class Ignore:
    database: str
    tables: list[str]


@dataclass
class Settings:
    production: DatabaseConnection
    development: DatabaseConnection
    ignore: list[Ignore]
    targets: list[str]
