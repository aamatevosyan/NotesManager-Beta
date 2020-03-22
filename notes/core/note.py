from time import strftime
from typing import List
from uuid import uuid1

import jsonpickle

from notes.core.noteattachment import NoteAttachment
from notes.core.notecategory import NoteCategory


class Note:
    max_history_size = 10

    def __init__(self, name: str, category: NoteCategory, tags: List[str], content: str,
                 attachments: List[NoteAttachment], history: List[List[str]], notecolor: str):
        self.notecolor = notecolor
        self.history = history
        self.category = category or NoteCategory.get_undefined_category()
        self.attachments = attachments or []
        self.content = content or ""
        self.tags = tags or []
        self.name = name or ""
        self.uuid = str(uuid1())

    @classmethod
    def get_empty_note(cls):
        return cls("Note", NoteCategory.get_undefined_category(), [], "", [], [], "")

    def shallow_clone(self):
        return jsonpickle.decode(jsonpickle.encode(self))

    def backup(self, name: str):
        if len(self.history) == Note.max_history_size - 1:
            self.remove(0)

        self.history.append([self.content, strftime("%A, %d. %B %Y %H:%M"), name])

    def restore(self, index: int):
        if 0 <= index < len(self.history):
            self.content = self.history[index][0]

    def remove(self, index: int):
        self.history.remove(self.history[index])
