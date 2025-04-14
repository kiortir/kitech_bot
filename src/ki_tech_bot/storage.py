import ujson as json
from os import PathLike
from pathlib import Path

from pydantic import TypeAdapter


user_list_adapter = TypeAdapter(set[int])


class FsUserStorage:

    def __init__(self, path: PathLike):
        self.path = Path(path)
        self.id_list = set()
        if not self.path.exists():
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump([], f)
        else:
            with open(path, "r", encoding="utf-8") as f:
                self.id_list = user_list_adapter.validate_json(f.read())

    def add_user(self, user_id: int):
        self.id_list.add(user_id)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(list(self.id_list), f)

    def is_authorized(self, user_id: int) -> bool:
        return user_id in self.id_list
