from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class LinkAddDialog(QDialog):

    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent, Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint | Qt.WindowTitleHint)
        self.setWindowTitle("Add link to note")

        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        self.setWindowIcon(QIcon("icons/insert_link.png"))

        # self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.linkAdressEdit = QLineEdit()
        self.linkAdressEdit.textChanged.connect(self.onLinkAdressChanged)
        self.linkAdressEdit.setPlaceholderText("Enter a link address")

        self.linkCaptionEdit = QLineEdit()
        self.linkCaptionEdit.textChanged.connect(self.onLinkCaptionChanged)
        self.linkCaptionEdit.setPlaceholderText("Enter a link caption")

        layout.addWidget(self.linkAdressEdit)
        layout.addWidget(self.linkCaptionEdit)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.setCenterButtons(True)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons, Qt.AlignCenter)

        self.setLayout(layout)

    def onLinkAdressChanged(self):
        self.linkAdress = self.linkAdressEdit.text()
        self.linkCaptionEdit.setText(self.linkAdress)

    def onLinkCaptionChanged(self):
        self.linkCaption = self.linkCaptionEdit.text()
