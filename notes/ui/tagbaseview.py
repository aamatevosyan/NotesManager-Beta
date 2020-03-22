from typing import List

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from notes import *
from notes.ui.tagedit import TagEdit


class TagBaseView(QDialog):

    def __init__(self, parent=None, tags: List[str] = None, tag_base: TagBase = None):
        super(QDialog, self).__init__(parent, Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint | Qt.WindowTitleHint)
        self.tag_base = tag_base
        self.notebook = notebook
        self.tags = tags or []
        self.setWindowTitle("Manage tags")

        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)

        self.initUI()

    def updateTags(self):
        self.tagListWidget.clear()
        for tag in self.tags:
            item = QListWidgetItem()
            item.setText(tag)
            self.tagListWidget.addItem(item)

    def initUI(self):

        layout = QVBoxLayout()

        self.tagListWidget = QListWidget()

        self.updateTags()

        layout.addWidget(self.tagListWidget)

        addButton = QPushButton("Add")
        addButton.clicked.connect(self.addTag)

        removeButton = QPushButton("Remove")
        removeButton.clicked.connect(self.removeTag)

        layout.addWidget(addButton)
        layout.addWidget(removeButton)

        self.setLayout(layout)

    def addTag(self):
        tag = ""
        dialog = TagEdit(parent=self, tag=tag, note_tags=self.tags)

        result = dialog.exec_()
        if result == QDialog.Accepted:
            self.tag_base.add(dialog.tag)
            self.tags.append(dialog.tag)
            self.updateTags()

    def removeTag(self):
        tag = self.tags[self.tagListWidget.currentRow()]
        self.tag_base.remove(tag)
        self.tags.remove(tag)
        self.updateTags()
