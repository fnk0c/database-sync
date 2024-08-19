from faker import Faker

from database_sync.domain.entities.settings import Ignore


class IgnoreBuilder:
    FAKE = Faker()

    @classmethod
    def build(cls) -> Ignore:
        return Ignore(
            database=cls.FAKE.word(), tables=[cls.FAKE.word() for _ in range(5)]
        )

    @classmethod
    def build_many(cls, amount: int = 5) -> list[Ignore]:
        return [cls.build() for _ in range(amount)]
