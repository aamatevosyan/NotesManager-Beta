from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from notes import Note, Notebook


class NoteContentEdit(QTextBrowser):

    def __init__(self, parent: QWidget, notebook: Notebook, note: Note):
        super(QTextBrowser, self).__init__(parent)

        self.notebook = notebook
        self.note = note

        self.setReadOnly(False)
        self.setTextInteractionFlags(self.textInteractionFlags() | Qt.LinksAccessibleByMouse)
        self.setOpenLinks(False)
        self.setOpenExternalLinks(False)
        self.setAcceptRichText(True)
        self.setObjectName("text")
        self.setUndoRedoEnabled(True)
        self.setAutoFormatting(QTextEdit.AutoAll)

        self.setHtml(note.content)

    def saveChanges(self):
        self.note.content = self.toHtml()
