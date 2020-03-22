from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox, QMessageBox


class NameEditDialog(QDialog):

    def __init__(self, parent=None, name: str = None):
        super(QDialog, self).__init__(parent, Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint | Qt.WindowTitleHint)
        self.name = name

        self.setWindowTitle("Manage name")

        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)

        self.initUI()

    def initUI(self):

        layout = QVBoxLayout()

        self.nameEdit = QLineEdit()
        self.nameEdit.setPlaceholderText("Enter a name")
        self.nameEdit.setText(self.name)

        layout.addWidget(self.nameEdit)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.setCenterButtons(True)
        buttons.accepted.connect(self.onAccept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons, Qt.AlignCenter)

        self.setLayout(layout)

    def onAccept(self):
        if len(self.nameEdit.text()) == 0:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("Name can't be empty")
            msgBox.setWindowTitle("")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
        else:
            self.name = self.nameEdit.text()
            self.accept()
