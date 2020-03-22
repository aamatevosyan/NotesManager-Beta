from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from notes import Notebook
from notes.ui.notebookpreviewtreewidget import NotebookPreviewTreeWidget


class NoteSelectDialog(QDialog):

    def __init__(self, parent=None, notebook: Notebook = None):
        super(QDialog, self).__init__(parent, Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint | Qt.WindowTitleHint)
        self.notebook = notebook
        self.setWindowTitle("Select note")

        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        # self.setWindowIcon(QIcon("icons/insert_link.png"))

        # self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        self.initUI()

    def initUI(self):

        layout = QVBoxLayout()

        self.notePreviewWidget = NotebookPreviewTreeWidget()
        self.notePreviewWidget.load_notebook(self.notebook)

        layout.addWidget(self.notePreviewWidget)

        self.noteCaptionEdit = QLineEdit()
        self.noteCaptionEdit.setPlaceholderText("Enter caption for link")
        layout.addWidget(self.noteCaptionEdit)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.setCenterButtons(True)
        buttons.accepted.connect(self.onAccept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons, Qt.AlignCenter)

        self.setLayout(layout)

    def onAccept(self):
        if (len(self.noteCaptionEdit.text()) == 0):
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("Caption can't be empty")
            msgBox.setWindowTitle("")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
        elif not hasattr(self.notePreviewWidget, "selectedNote"):
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("Note isn't selected.")
            msgBox.setWindowTitle("")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
        else:
            self.selectedNote = self.notePreviewWidget.selectedNote
            self.caption = self.noteCaptionEdit.text()
            self.accept()
