import pathlib

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from notes import *
from notes.ui.cetegorybaseview import CategoryBaseView
from notes.ui.nameeditdialog import NameEditDialog
from notes.ui.noteviewmanager import NoteViewManager
from notes.ui.settingsdialog import NotebookSettingsDialog
from notes.ui.tagbaseview import TagBaseView


class NotebookTreeWidget(QTreeWidget):
    root_icon_path = str(pathlib.Path("icons/notebook.png"))
    section_icon_path = str(pathlib.Path("icons/section.png"))
    subsection_icon_path = str(pathlib.Path("icons/subsection.png"))

    def __init__(self, parent=None, noteViewManager: NoteViewManager = None):
        super(QTreeWidget, self).__init__(parent)

        self.noteViewManager = noteViewManager
        self.register_signals()
        self.setHeaderLabel("Notebook")

    def add_root(self):
        self.root_child = QTreeWidgetItem()
        self.root_child.setText(0, "Root")
        self.root_child.setIcon(0, QIcon(self.root_icon_path))
        self.invisibleRootItem().addChild(self.root_child)
        self.root_child.setExpanded(True)
        self.invisibleRootItem().setExpanded(True)

    def register_signals(self):
        self.itemDoubleClicked.connect(self.onItemDoubleClicked)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.onCustomContextMenuRequested)

    def load_notebook(self, notebook: Notebook):
        self.notebook = notebook
        self.load_widget(notebook)

    def load_item(self, item: QTreeWidgetItem, value):

        for subvalue in value:
            child = QTreeWidgetItem()
            item.addChild(child)
            child.data_container = subvalue
            child.setText(0, subvalue.name)
            child.setExpanded(True)

            if type(subvalue) is Note:
                print(self.notebook.category_base)
                self.notebook.category_base.get_icon(subvalue.category)
                icon = self.notebook.category_base.get_icon(subvalue.category)
                print(icon)
                child.setIcon(0, icon)
            elif type(subvalue) is Subsection:
                child.setIcon(0, QIcon(self.subsection_icon_path))
                self.load_item(child, subvalue)
            else:
                child.setIcon(0, QIcon(self.section_icon_path))
                self.load_item(child, subvalue)

    def load_widget(self, notebook: Notebook):
        # for i in reversed(range(self.root_child.childCount())):
        #     self.root_child.removeChild(self.root_child.child(i))
        self.clear()
        self.add_root()

        self.notebook = notebook
        self.load_item(self.root_child, notebook)

    def openNote(self, note: Note):
        for i in range(self.root_child.childCount()):
            for j in range(self.root_child.child(i).childCount()):
                for k in range(self.root_child.child(i).child(j).childCount()):
                    current = self.root_child.child(i).child(j).child(k)
                    if hasattr(current, "data_container") and \
                            type(current.data_container) is Note and current.data_container == note:

                        self.note_attachments_view.clear()
                        if hasattr(self, "previous_note"):
                            self.previous_note.content = self.note_content_view.toHtml()
                        self.previous_note = current.data_container
                        self.note_attachments_view.load_attachments(current.data_container.attachments)
                        # for attachments
                        self.note_content_view.setText(current.data_container.content)
                        current.setSelected(True)

    def onItemChanged(self, item: QTreeWidgetItem, column: int) -> None:
        if hasattr(item, "data_container"):
            item.data_container.name = item.text(column)
            print(item.data_container.name)

    def onItemDoubleClicked(self, item: QTreeWidgetItem, column: int) -> None:
        if hasattr(item, "data_container") and type(item.data_container) is Note:
            self.noteViewManager.openNote(item.data_container)

    def onCurrentItemChanged(self, current: QTreeWidgetItem, previous: QTreeWidgetItem) -> None:
        if hasattr(current, "data_container") and type(current.data_container) is Note:
            self.note_attachments_view.clear()
            if hasattr(self, "previous_note"):
                self.previous_note.content = self.note_content_view.toHtml()
            self.previous_note = current.data_container
            self.note_attachments_view.load_attachments(current.data_container.attachments)
            # for attachments
            self.note_content_view.setText(current.data_container.content)

    def onCustomContextMenuRequested(self, point: QPoint):
        # Infos about the node selected.
        index = self.indexAt(point)

        if not index.isValid():
            return

        item: QTreeWidgetItem = self.itemAt(point)

        name = item.text(0)  # The text of the node.

        # We build the menu.
        menu = QMenu()

        if (hasattr(item, "data_container")):

            renameDataContainerAction = QAction("Rename")
            renameDataContainerAction.triggered.connect(lambda checked, item=item: self.renameItem(item))
            menu.addAction(renameDataContainerAction)

            if (type(item.data_container) == Section):

                newSubsectionAction = QAction("New subsection")
                newSubsectionAction.triggered.connect(lambda checked, item=item: self.newSubsection(item))
                menu.addAction(newSubsectionAction)

                menu.addSeparator()

                menu.addAction(renameDataContainerAction)

                removeSectionAction = QAction("Remove section")
                removeSectionAction.triggered.connect(lambda checked, item=item: self.removeSection(item))
                menu.addAction(removeSectionAction)

            elif (type(item.data_container) == Subsection):

                menu.addAction(renameDataContainerAction)

                removeSubsectionAction = QAction("Remove subsection")
                removeSubsectionAction.triggered.connect(lambda checked, item=item: self.removeSubsection(item))
                menu.addAction(removeSubsectionAction)

                menu.addSeparator()

                newNoteAction = QAction("New note")
                newNoteAction.triggered.connect(lambda checked, item=item: self.newNote(item))
                menu.addAction(newNoteAction)
            else:

                categoryMenu = QMenu("Change category")
                for category in self.notebook.category_base.categories:
                    print(category)
                    icon = self.notebook.category_base.get_icon(category)
                    action = QAction(icon, category.name, self)
                    action.triggered.connect(
                        lambda checked, item=item, category=category: self.changeCategory(item, category))
                    categoryMenu.addAction(action)
                menu.addMenu(categoryMenu)

                note: Note = item.data_container
                viewTagsAction = QAction("View tags", self)
                viewTagsAction.triggered.connect(lambda checked, note=note: self.viewTags(note))
                menu.addAction(viewTagsAction)

                menu.addMenu(categoryMenu)

                menu.addSeparator()
                menu.addAction(renameDataContainerAction)

                removeNoteAction = QAction("Remove note")
                removeNoteAction.triggered.connect(lambda checked, item=item: self.removeNote(item))
                menu.addAction(removeNoteAction)
        else:
            newSectionAction = QAction("New section")
            newSectionAction.triggered.connect(lambda checked, item=item: self.newSection())
            menu.addAction(newSectionAction)

            manageCategoriesAction = QAction("Manage categories")
            manageCategoriesAction.triggered.connect(lambda checked, item=item: self.manageCategories())
            menu.addAction(manageCategoriesAction)

            manageSettingsAction = QAction("Manage notebook settings")
            manageSettingsAction.triggered.connect(lambda checked, item=item: self.manageSettings())
            menu.addAction(manageSettingsAction)

        menu.exec_(self.mapToGlobal(point))

    def viewTags(self, note: Note):
        dialog = TagBaseView(parent=self, tags=note.tags, tag_base=self.notebook.tag_base)
        dialog.exec_()
        note.tags = dialog.tags

    def manageCategories(self):
        dialog = CategoryBaseView(parent=self, category_base=self.notebook.category_base)
        dialog.exec_()

    def manageSettings(self):
        dialog = NotebookSettingsDialog(self, self.notebook.settings)
        dialog.exec_()

    def newSection(self):
        self.notebook.sections.append(Section(name="New Section"))
        self.load_notebook(self.notebook)

    def removeSection(self, item: QTreeWidgetItem):
        section = item.data_container
        self.notebook.sections.remove(section)
        self.load_notebook(self.notebook)

    def newSubsection(self, item: QTreeWidgetItem):
        section = item.data_container
        section.subsections.append(Subsection(name="New Subsection"))
        self.load_notebook(self.notebook)

    def removeSubsection(self, item: QTreeWidgetItem):
        parent = item.parent()
        section = parent.data_container
        subsection = item.data_container
        section.subsections.remove(subsection)
        self.load_notebook(self.notebook)

    def newNote(self, item: QTreeWidgetItem):
        subsection = item.data_container
        subsection.notes.append(Note.get_empty_note())
        self.load_notebook(self.notebook)

    def removeNote(self, item: QTreeWidgetItem):
        parent = item.parent()
        subsection = parent.data_container
        note = item.data_container
        subsection.notes.remove(note)
        self.noteViewManager.removeNote(note)
        self.load_notebook(self.notebook)

    def changeCategory(self, item, category):
        note = item.data_container
        note.category = category
        self.noteViewManager.updateIcon(note)
        self.load_notebook(self.notebook)

    def renameItem(self, item: QTreeWidgetItem):
        name = item.data_container.name

        dialog = NameEditDialog(parent=self, name=name)

        result = dialog.exec_()
        if result == QDialog.Accepted:
            item.setText(0, dialog.name)
            item.data_container.name = dialog.name
            self.noteViewManager.updateName(item.data_container)
