from dataclasses import dataclass


@dataclass
class Database:
    tables: list[str]
    sequences: list[str]
    views: list[str]
