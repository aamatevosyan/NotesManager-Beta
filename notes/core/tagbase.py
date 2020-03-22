from typing import Dict


class TagBase:

    def __init__(self, tags: Dict[str, int]):
        self.tags = tags or {}

    def __iter__(self):
        return iter(self.tags)

    def add(self, tag: str):
        if tag in self.tags:
            self.tags[tag] += 1
        else:
            self.tags[tag] = 1

    def remove(self, tag: str):
        if tag in self.tags:
            self.tags[tag] -= 1
            if self.tags[tag] == 0:
                self.tags.pop(tag)
