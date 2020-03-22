from PyQt5.QtCore import QPoint

from notes.ui.notebooktreewidget import NotebookTreeWidget
from notes.ui.noteviewmanager import NoteViewManager


class NotebookFilteredTreeWidget(NotebookTreeWidget):

    def __init__(self, parent=None, noteViewManager: NoteViewManager = None):
        super(NotebookFilteredTreeWidget, self).__init__(parent=parent, noteViewManager=noteViewManager)

    def onCustomContextMenuRequested(self, point: QPoint):
        pass
