from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from notes import *


class NoteCategoryEdit(QDialog):

    def __init__(self, parent=None, category: NoteCategory = None, category_base: CategoryBase = None):

        super(QDialog, self).__init__(parent, Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint | Qt.WindowTitleHint)
        self.category_base = category_base
        self.category = category
        self.setWindowTitle("Manage categories")

        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)

        self.initUI()

    def initUI(self):

        layout = QVBoxLayout()

        self.colorView = QListWidget()
        self.colorView.setIconSize(QSize(32, 32))
        self.colorView.setViewMode(QListView.IconMode)

        self.colorNames = []

        for color in CategoryColor:
            value = color.value
            self.colorNames.append(value)

            item = QListWidgetItem("")
            item.setIcon(color.get_icon())

            self.colorView.addItem(item)

        self.colorView.setCurrentRow(0)

        self.nameEdit = QLineEdit()
        self.nameEdit.setPlaceholderText("Enter a name for category")
        self.nameEdit.setText(self.category.name)

        layout.addWidget(self.colorView)
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
        if not self.category_base.isvalid(NoteCategory(name=self.nameEdit.text(), color=None)):
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("Name can't be repeated and cant't be empty.")
            msgBox.setWindowTitle("")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
        else:
            self.category.name = self.nameEdit.text()
            ind = self.colorView.currentRow()
            self.category.color = CategoryColor(self.colorNames[ind])
            self.accept()
