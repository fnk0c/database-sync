class PsqlMapper:
    @staticmethod
    def map_to_list(raw: list[tuple]) -> list[str]:
        return [item[0] for item in raw]
