from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from notes import Notebook
from notes.ui.notebookpreviewtreewidget import NotebookPreviewTreeWidget


class NotebookFilterDialog(QDialog):

    def __init__(self, parent=None, notebook: Notebook = None):
        super(QDialog, self).__init__(parent, Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint | Qt.WindowTitleHint)
        self.notebook: Notebook = notebook.shallow_clone()
        self.setWindowTitle("Filter notes")
        self.filteredNoteBook: Notebook = self.notebook.shallow_clone()
        self.setMinimumWidth(200)

        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        # self.setWindowIcon(QIcon("icons/insert_link.png"))

        # self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        self.initUI()

    def initUI(self):

        layout = QVBoxLayout()

        self.noteFilterEdit = QLineEdit()
        self.noteFilterEdit.setPlaceholderText("Enter a filtered expression")

        # self.tagsFilterEdit = QLineEdit()
        # self.tagsFilterEdit.setPlaceholderText("Enter a tags separated by ','")

        self.tagsListWidget = QListWidget()

        for tag in self.notebook.tag_base.tags:
            item = QListWidgetItem()
            item.setText(tag)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)

            self.tagsListWidget.addItem(item)

        self.notePreviewWidget = NotebookPreviewTreeWidget()
        self.notePreviewWidget.load_notebook(self.filteredNoteBook)

        layout.addWidget(self.noteFilterEdit)
        # layout.addWidget(self.tagsFilterEdit)

        if self.tagsListWidget.count() > 0:
            layout.addWidget(self.tagsListWidget)
        layout.addWidget(self.notePreviewWidget)

        self.filterButton = QPushButton("Filter")
        self.filterButton.clicked.connect(self.filter)

        layout.addWidget(self.filterButton)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)

        buttons.setCenterButtons(True)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons, Qt.AlignCenter)

        self.setLayout(layout)

    def getTags(self):
        tags = []
        for i in range(self.tagsListWidget.count()):
            item = self.tagsListWidget.item(i)
            if item.checkState() == Qt.Checked:
                tags.append(item.text())
        return tags

    def filter(self):
        noteFilter = self.noteFilterEdit.text()
        tagsFilter = self.getTags()
        self.filteredNoteBook: Notebook = self.notebook.shallow_clone()
        self.filteredNoteBook.filter_notes(noteFilter, tagsFilter)
        self.filteredNoteBook.remove_empty_sections()
        self.notePreviewWidget.load_notebook(self.filteredNoteBook)
