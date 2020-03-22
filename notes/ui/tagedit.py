from typing import List

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class TagEdit(QDialog):

    def __init__(self, parent=None, tag: str = None, note_tags: List[str] = None):
        super(QDialog, self).__init__(parent, Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint | Qt.WindowTitleHint)
        self.tag = tag or ""
        self.note_tags = note_tags or []
        self.setWindowTitle("Manage tags")

        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)

        self.initUI()

    def initUI(self):

        layout = QVBoxLayout()

        self.tagEdit = QLineEdit()
        self.tagEdit.setPlaceholderText("Enter a tag")
        self.tagEdit.setText(self.tag)

        layout.addWidget(self.tagEdit)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.setCenterButtons(True)
        buttons.accepted.connect(self.onAccept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons, Qt.AlignCenter)

        self.setLayout(layout)

    def onAccept(self):
        if len(self.tagEdit.text()) == 0:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("Tag can't be empty")
            msgBox.setWindowTitle("")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
        elif self.tagEdit.text() in self.note_tags:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("There is a tag with the same name. Tags must be unique.")
            msgBox.setWindowTitle("")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
        else:
            self.tag = self.tagEdit.text()
            self.accept()
