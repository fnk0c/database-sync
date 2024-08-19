from unittest import TestCase

from database_sync.domain.commands.sync_command import SyncCommand
from tests.infrastructure.services.doubles.database_service_stub import (
    InMemoryDatabaseServiceStub,
)


class TestSyncCommand(TestCase):
    def test_execute_with_data(self) -> None:
        # given
        prod_service = InMemoryDatabaseServiceStub()
        dev_service = InMemoryDatabaseServiceStub()
        ignore = []
        targets = ["database1", "database2"]
        command = SyncCommand(prod_service, dev_service)

        # when
        status = command.execute(targets, ignore)

        # then
        self.assertTrue(status, "sync command should return true")

    def test_execute_empty(self) -> None:
        # given
        prod_service = (
            InMemoryDatabaseServiceStub()
            .with_views([])
            .with_sequences([])
            .with_tables([])
        )
        dev_service = (
            InMemoryDatabaseServiceStub()
            .with_views([])
            .with_sequences([])
            .with_tables([])
        )
        ignore = []
        targets = ["database1", "database2"]
        command = SyncCommand(prod_service, dev_service)

        # when
        status = command.execute(targets, ignore)

        # then
        self.assertTrue(status, "sync command should return true")
