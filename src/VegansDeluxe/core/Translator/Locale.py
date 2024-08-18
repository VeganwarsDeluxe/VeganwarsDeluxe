from typing import Optional


class Locale:
    def __init__(self, code: str):
        self.code: str = code
        self.data: dict[str: str] = dict()

    def add_data(self, data: dict) -> None:
        for key, value in data.items():
            if key in self.data:
                raise Exception(f"Trying to add duplicate key {key}")
            self.data.update({key: value})

    def get_string(self, key: str) -> Optional[str]:
        return self.data.get(key, None)
