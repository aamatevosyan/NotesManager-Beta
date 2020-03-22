from PyQt5.QtGui import QIcon

from notes.core.categorycolor import CategoryColor


class NoteCategory:

    def __init__(self, name: str, color: CategoryColor):
        self.color = color
        self.name = name

    @classmethod
    def get_undefined_category(cls):
        return cls("Undefined", CategoryColor.CatskillWhite)

    def get_icon(self) -> QIcon:
        return self.color.get_icon()
