import pathlib

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from notes import *


class NotebookPreviewTreeWidget(QTreeWidget):
    root_icon_path = str(pathlib.Path("icons/notebook.png"))
    section_icon_path = str(pathlib.Path("icons/section.png"))
    subsection_icon_path = str(pathlib.Path("icons/subsection.png"))

    def __init__(self, parent=None):
        super(QTreeWidget, self).__init__(parent)

        self.setHeaderLabel("Notebook")
        self.currentItemChanged.connect(self.onCurrentItemChanged)

    def add_root(self):
        self.root_child = QTreeWidgetItem()
        self.root_child.setText(0, "Root")
        self.root_child.setIcon(0, QIcon(self.root_icon_path))
        self.root_child.setFlags(Qt.ItemIsEnabled)

        self.invisibleRootItem().addChild(self.root_child)
        self.root_child.setExpanded(True)
        self.invisibleRootItem().setExpanded(True)

    def load_notebook(self, notebook: Notebook):
        self.notebook: Notebook = notebook.shallow_clone()
        self.notebook = self.notebook.remove_empty_sections()
        self.load_widget(notebook)

    def load_item(self, item: QTreeWidgetItem, value):

        for subvalue in value:
            child = QTreeWidgetItem()
            item.addChild(child)
            child.data_container = subvalue
            child.setText(0, subvalue.name)
            child.setExpanded(True)
            child.setFlags(Qt.ItemIsEnabled)

            if type(subvalue) is Note:
                self.notebook.category_base.get_icon(subvalue.category)
                icon = self.notebook.category_base.get_icon(subvalue.category)
                child.setIcon(0, icon)
                child.setFlags(child.flags() | Qt.ItemIsSelectable)
            elif type(subvalue) is Subsection:
                child.setIcon(0, QIcon(self.subsection_icon_path))
                self.load_item(child, subvalue)
            else:
                child.setIcon(0, QIcon(self.section_icon_path))
                self.load_item(child, subvalue)

    def load_widget(self, notebook: Notebook):
        self.clear()
        self.add_root()

        self.notebook = notebook
        self.load_item(self.root_child, notebook)

    def onCurrentItemChanged(self, current: QTreeWidgetItem, previous: QTreeWidgetItem) -> None:
        if hasattr(current, "data_container") and type(current.data_container) is Note:
            self.selectedNote = current.data_container
