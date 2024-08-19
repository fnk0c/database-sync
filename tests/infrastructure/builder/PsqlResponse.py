from faker import Faker


class PsqlResponseBuilder:
    FAKE = Faker()

    @classmethod
    def fetch_all_response(cls) -> list[tuple]:
        return [(cls.FAKE.word(),) for _ in range(10)]
