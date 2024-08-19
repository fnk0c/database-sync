from abc import ABC, abstractmethod

from database_sync.domain.entities.settings import Settings


class SettingsRepository(ABC):
    @abstractmethod
    def get_settings(self) -> Settings:
        pass
