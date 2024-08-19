import os
from unittest import TestCase

from database_sync.infrastructure.services.psql_database_service import (
    PsqlDatabaseService,
)
from tests.domain.builders.ignore_builder import IgnoreBuilder
from tests.infrastructure.builder.PsqlResponse import PsqlResponseBuilder
from tests.infrastructure.helpers.doubles.psql_connector_stub import (
    InMemoryPsqlConnector,
)


class TestPsqlDatabaseService(TestCase):
    def test_list_tables_empty(self) -> None:
        # given
        connector = InMemoryPsqlConnector()
        service = PsqlDatabaseService(connector)
        database = "test"

        # when
        service.connect(database)
        tables = service.list_tables(database)

        # then
        self.assertEqual(tables, [])

    def test_list_tables_data(self) -> None:
        # given
        data = PsqlResponseBuilder.fetch_all_response()
        connector = InMemoryPsqlConnector().with_data(data)
        service = PsqlDatabaseService(connector)
        database = "test"

        # when
        service.connect(database)
        tables = service.list_tables(database)

        # then
        self.assertEqual(len(tables), len(data))
        self.assertEqual(tables[0], data[0][0])

    def test_list_sequences_empty(self) -> None:
        # given
        connector = InMemoryPsqlConnector()
        service = PsqlDatabaseService(connector)
        database = "test"

        # when
        service.connect(database)
        tables = service.list_sequences(database)

        # then
        self.assertEqual(tables, [])

    def test_list_sequences_data(self) -> None:
        # given
        data = PsqlResponseBuilder.fetch_all_response()
        connector = InMemoryPsqlConnector().with_data(data)
        service = PsqlDatabaseService(connector)
        database = "test"

        # when
        service.connect(database)
        tables = service.list_sequences(database)

        # then
        self.assertEqual(len(tables), len(data))
        self.assertEqual(tables[0], data[0][0])

    def test_list_views_empty(self) -> None:
        # given
        connector = InMemoryPsqlConnector()
        service = PsqlDatabaseService(connector)
        database = "test"

        # when
        service.connect(database)
        tables = service.list_views(database)

        # then
        self.assertEqual(tables, [])

    def test_list_views_data(self) -> None:
        # given
        data = PsqlResponseBuilder.fetch_all_response()
        connector = InMemoryPsqlConnector().with_data(data)
        service = PsqlDatabaseService(connector)
        database = "test"

        # when
        service.connect(database)
        tables = service.list_views(database)

        # then
        self.assertEqual(len(tables), len(data))
        self.assertEqual(tables[0], data[0][0])

    def test_export_success(self) -> None:
        # given
        connector = InMemoryPsqlConnector()
        service = PsqlDatabaseService(connector)
        ignore = IgnoreBuilder.build_many()
        database = "database"

        # when
        service.export(database, ignore)

        # then
        files = os.listdir(".")
        self.assertIn(f"{database}.dump", files)
        os.remove(f"{database}.dump")

    def test_export_failure(self) -> None:
        # given
        connector = InMemoryPsqlConnector().with_dump_error()
        service = PsqlDatabaseService(connector)
        database = "database"

        # then
        with self.assertRaises(Exception):
            # when
            service.export(database, [])
