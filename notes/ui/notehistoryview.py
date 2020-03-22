from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from notes import *
from notes.ui.noteentrieedit import EntrieEditDialog


class NoteHistoryView(QDialog):

    def __init__(self, parent=None, note: Note = None):
        super(QDialog, self).__init__(parent, Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint | Qt.WindowTitleHint)
        self.note = note
        self.history = note.history
        self.setWindowTitle("Manage history")

        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)

        self.initUI()

    def updateEntries(self):
        self.entriesListWidget.clear()
        for entrie in self.history:
            if (len(entrie) == 0):
                continue

            item = QListWidgetItem()
            item.setText(entrie[1] + " - " + entrie[2])
            self.entriesListWidget.addItem(item)

        if self.entriesListWidget.count() > 0:
            self.entriesListWidget.setCurrentRow(0)

    def initUI(self):

        layout = QVBoxLayout()

        self.entriesListWidget = QListWidget()
        self.entriesListWidget.itemDoubleClicked.connect(self.onItemDoubleClicked)

        self.updateEntries()

        layout.addWidget(self.entriesListWidget)

        addButton = QPushButton("Add")
        addButton.clicked.connect(self.addEntrie)

        removeButton = QPushButton("Remove")
        removeButton.clicked.connect(self.removeEntrie)

        restoreButton = QPushButton("Restore")
        restoreButton.clicked.connect(self.restoreEntrie)

        layout.addWidget(addButton)
        layout.addWidget(restoreButton)
        layout.addWidget(removeButton)

        self.setLayout(layout)

    def addEntrie(self):
        dialog = EntrieEditDialog(self, "History: " + str(self.entriesListWidget.count()))

        result = dialog.exec_()
        if result == QDialog.Accepted:
            self.note.backup(dialog.name)
            self.updateEntries()

    def restoreEntrie(self):
        if (self.entriesListWidget.count() > 0):
            self.restoreIndex = self.entriesListWidget.currentRow()
            self.accept()

    def removeEntrie(self):
        if (self.entriesListWidget.count() > 0):
            entrie = self.history[self.entriesListWidget.currentRow()]
            self.history.remove(entrie)
            self.updateEntries()

    def onItemDoubleClicked(self, item: QListWidgetItem):
        dialog = QDialog(self)

        entrie = self.history[self.entriesListWidget.currentRow()]
        text = QTextBrowser()
        text.setHtml(entrie[0])

        dialog.setWindowTitle(item.text())
        dialog.setLayout(QVBoxLayout())
        dialog.layout().addWidget(text)

        dialog.exec_()
