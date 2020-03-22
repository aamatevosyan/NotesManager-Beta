from typing import List
from uuid import uuid1

from .note import Note


class Subsection:

    def __init__(self, name: str = None, notes: List[Note] = None):
        self.notes = notes or []
        self.name = name or ""
        self.uuid = str(uuid1())

    def __iter__(self):
        return iter(self.notes)
