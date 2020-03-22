from typing import List
from uuid import uuid1

from .subsection import Subsection


class Section:

    def __init__(self, name: str = None, subsections: List[Subsection] = None):
        self.subsections = subsections or []
        self.name = name or ""
        self.uuid = str(uuid1())

    def __iter__(self):
        return iter(self.subsections)
