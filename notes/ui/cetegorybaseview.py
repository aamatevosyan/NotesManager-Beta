from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from notes import *
from notes.ui.notecategoryedit import NoteCategoryEdit


class CategoryBaseView(QDialog):

    def __init__(self, parent=None, category_base: CategoryBase = None):
        super(QDialog, self).__init__(parent, Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint | Qt.WindowTitleHint)
        self.category_base = category_base
        self.setWindowTitle("Manage categories")

        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)

        self.initUI()

    def updateCategories(self):
        self.categoryListWidget.clear()
        for category in self.category_base.categories:
            name = category.name
            icon = category.get_icon()

            item = QListWidgetItem()
            item.setText(name)
            item.setIcon(icon)
            self.categoryListWidget.addItem(item)

    def initUI(self):

        layout = QVBoxLayout()

        self.categoryListWidget = QListWidget()

        self.updateCategories()

        layout.addWidget(self.categoryListWidget)

        addButton = QPushButton("Add")
        addButton.clicked.connect(self.addCategory)

        removeButton = QPushButton("Remove")
        removeButton.clicked.connect(self.removeCategory)

        layout.addWidget(addButton)
        layout.addWidget(removeButton)

        self.setLayout(layout)

    def addCategory(self):
        category = NoteCategory(name="Category", color=CategoryColor.AquamarineBlue)
        dialog = NoteCategoryEdit(parent=self, category=category, category_base=self.category_base)

        result = dialog.exec_()
        if result == QDialog.Accepted:
            self.category_base.categories.append(category)
            self.updateCategories()

    def removeCategory(self):
        category = self.category_base.categories[self.categoryListWidget.currentRow()]
        self.category_base.categories.remove(category)
        self.updateCategories()
