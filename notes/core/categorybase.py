from typing import List

from PyQt5.QtGui import QIcon

from notes.core.categorycolor import CategoryColor
from notes.core.notecategory import NoteCategory


class CategoryBase:

    def __init__(self, categories: List[NoteCategory]):
        self.categories = categories or []
        self.undefinedCategory = NoteCategory.get_undefined_category()

    def add(self, name: str, color: CategoryColor):
        category = NoteCategory(name, color)

        return self.add(category)

    def add(self, category: NoteCategory):
        if self.isvalid(category):
            self.categories.append(category)

        return category

    def remove(self, name: str, color: CategoryColor):
        category = NoteCategory(name, color)

        self.remove(category)

    def remove(self, category: NoteCategory):
        for el in self.categories:
            if el.name == category.name and el.color == category.color:
                self.categories.remove(el)

    def isvalid(self, name: str, color: CategoryColor):
        category = NoteCategory(name, color)
        return self.isvalid(category)

    def isvalid(self, category: NoteCategory):
        return len(category.name) != 0 and not any(map(lambda x: x.name == category.name, self.categories))

    def get_icon(self, category: NoteCategory) -> QIcon:
        if category in self.categories:
            return category.get_icon()
        else:
            return self.undefinedCategory.get_icon()

    def __iter__(self):
        return iter(self.categories)
