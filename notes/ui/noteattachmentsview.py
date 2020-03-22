import os
from typing import List

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from notes import *


class NoteAttachmentsListWidget(QListWidget):
    dropped = pyqtSignal([list])

    def __init__(self, parent=None):
        super(QListWidget, self).__init__(parent)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color:transparent;")
        self.setUniformItemSizes(True)

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        data = e.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            e.acceptProposedAction()

    def dragMoveEvent(self, e: QDragMoveEvent) -> None:
        data = e.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            e.acceptProposedAction()

    def dropEvent(self, e):

        data = e.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            self.dropped.emit(list(map(lambda x: x.toLocalFile(), urls)))

    def contextMenuEvent(self, a0: QContextMenuEvent) -> None:
        point = a0.pos()

        if (not self.indexAt(point).isValid()):
            return

        menu = QMenu()

        menu.addAction(self.openAction)
        menu.addAction(self.deleteAction)
        menu.addAction(self.saveAsAction)
        menu.exec_(self.mapToGlobal(point))


class NoteAttachmentsView(QWidget):
    _iconProvider = QFileIconProvider()

    def __init__(self, parent: QWidget, notebook: Notebook, note: Note):
        super(QWidget, self).__init__(parent)

        self.note = note
        self.notebook = notebook

        self.attachmentsListWidget = NoteAttachmentsListWidget()

        self.register_signals()
        self.initActions()

        self.attachmentsListWidget.openAction = self.openAction
        self.attachmentsListWidget.saveAsAction = self.saveAsAction
        self.attachmentsListWidget.deleteAction = self.deleteAction

        self.attachmentsListWidget.setDragEnabled(True)
        self.attachmentsListWidget.setAcceptDrops(True)
        self.attachmentsListWidget.setResizeMode(QListWidget.Adjust)

        self.lay = QVBoxLayout()
        self.lay.addWidget(self.attachmentsListWidget)
        self.setLayout(self.lay)

        self.attachmentsListWidget.setViewMode(notebook.settings.attachments_list_view_mode())
        self.attachmentsListWidget.setIconSize(notebook.settings.attachments_list_icon_size())

        self.load_attachments()

    def initActions(self):
        self.openAction = QAction(QIcon("icons/open.png"), "Open attachment", self.attachmentsListWidget)
        self.openAction.setStatusTip("Open attachment")
        self.openAction.triggered.connect(self.openAttachment)

        self.deleteAction = QAction(QIcon("icons/delete.png"), "Delete attachment", self.attachmentsListWidget)
        self.deleteAction.setStatusTip("Delete attachment")
        self.deleteAction.triggered.connect(self.deleteAttachment)

        self.saveAsAction = QAction(QIcon("icons/save_alt.png"), "Save attachment", self.attachmentsListWidget)
        self.saveAsAction.setStatusTip("Save attachment")
        self.saveAsAction.triggered.connect(self.saveAsAttachment)

    def register_signals(self):
        self.attachmentsListWidget.itemDoubleClicked.connect(self.onItemDoubleClicked)
        self.attachmentsListWidget.dropped.connect(self.addAttachments)

        # self.attachmentsListWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.attachmentsListWidget.customContextMenuRequested.connect(self.onCustomContextMenuRequested)

    def load_attachments(self):
        self.attachmentsListWidget.clear()

        for attachment in self.note.attachments:
            if attachment == None:
                continue

            item = QListWidgetItem(attachment.name + "." + attachment.extension)

            icon = attachment.get_icon()
            item.setIcon(icon)

            self.attachmentsListWidget.addItem(item)

    def onItemDoubleClicked(self, item: QListWidgetItem) -> None:
        self.openAttachment()

    def addAttachments(self, filenames: List[str]):
        for filename in filenames:
            if os.path.exists(filename):
                attachment = self.notebook.attachment_base.add(filename)
                self.note.attachments.append(attachment)

        self.load_attachments()

    def insertAttachment(self):
        filename = \
            QFileDialog.getOpenFileName(self, 'Insert attachments', ".")[0]

        if filename:
            attachment = self.notebook.attachment_base.add(filename)
            self.note.attachments.append(attachment)

            self.load_attachments()

    def openAttachment(self):
        index = self.attachmentsListWidget.currentRow()
        attachment = self.note.attachments[index]

        self.notebook.attachment_base.open_with_default_app(attachment.uuid)

    def deleteAttachment(self):
        index = self.attachmentsListWidget.currentRow()
        attachment = self.note.attachments[index]

        self.note.attachments.remove(attachment)

        self.notebook.attachment_base.remove(attachment.uuid)

        self.load_attachments()

    def saveAsAttachment(self):

        index = self.attachmentsListWidget.currentRow()
        attachment = self.note.attachments[index]

        filename = QFileDialog.getSaveFileName(self, 'Save File', attachment.name, "(*." + attachment.extension + ")")[
            0]

        if filename:
            self.notebook.attachment_base.save_to_file(filename, attachment.uuid)
