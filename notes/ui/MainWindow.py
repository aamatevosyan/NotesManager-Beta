import os
import pathlib

import jsonpickle
from PyQt5.QtGui import QIcon, QCloseEvent
from PyQt5.QtWidgets import QAction, QMenu, QMainWindow, QWidget, QVBoxLayout, QDialog, QFileDialog

from notes import *
from notes.ui.Ui_MainWindow import Ui_MainWindow
from notes.ui.ext import Find
from notes.ui.notebookfilterdialog import NotebookFilterDialog
from notes.ui.notebookfilteredwidget import NotebookFilteredTreeWidget
from notes.ui.notebooktreewidget import NotebookTreeWidget
from notes.ui.noteviewmanager import NoteViewManager


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent: QWidget, *args):
        super(MainWindow, self).__init__(parent)

        self.setupUi(self)

        self.splitter.setCollapsible(0, False)
        self.splitter.setCollapsible(1, False)

        with open("settings.json", mode="r") as f:
            self.settings = jsonpickle.decode(f.read())

        notebook = None

        self.noteViewManager = NoteViewManager(self.notesTabWidget, notebook)

        self.mainTreeWidget = NotebookTreeWidget(self.mainTab, self.noteViewManager)
        self.filteredTreeWidget = NotebookFilteredTreeWidget(self.filteredTab, self.noteViewManager)

        self.mainTab.setLayout(QVBoxLayout())
        self.filteredTab.setLayout(QVBoxLayout())

        self.notesTabWidget.setTabsClosable(True)
        self.notesTabWidget.setMovable(True)

        self.mainTab.layout().addWidget(self.mainTreeWidget)
        self.filteredTab.layout().addWidget(self.filteredTreeWidget)

        self.initActions()
        self.initMenubar()
        self.setup()
        self.beforeClose()

        if len(args) == 0:
            pass
        elif len(args) == 1:
            self.open_notebook(args[0])
        elif len(args) == 2:
            self.open_notebook(args[0])
            self.noteViewManager.openNote(self.noteViewManager.notebook.get_note_by_uuid(args[1]))

    def setup(self):
        self.app_name = "Notes Manager"
        self.recent_files = set()
        self.recent_files_config_path = "recent_files.json"

        self.app_settings_path = "app_settings.json"

        with open(self.app_settings_path, "r") as f:
            self.app_settings = jsonpickle.decode(f.read())

        if not pathlib.Path(self.recent_files_config_path).exists():
            with open(self.recent_files_config_path, "w") as f:
                f.write(jsonpickle.encode(self.recent_files))

        with open(self.recent_files_config_path, "r") as f:
            self.recent_files = jsonpickle.decode(f.read())
        self.updateRecent()

    def beforeClose(self):
        if hasattr(self, "filename"):
            del self.filename

        self.noteViewManager.saveChanges()
        self.noteViewManager.closeAll()

        self.mainTreeWidget.clear()
        self.filteredTreeWidget.clear()
        self.centralwidget.setVisible(False)
        self.centralwidget.setEnabled(False)

        self.editMenu.setEnabled(False)
        self.saveAction.setEnabled(False)
        self.saveAsAction.setEnabled(False)
        self.closeFileAction.setEnabled(False)

    def afterOpen(self):
        self.centralwidget.setVisible(True)
        self.centralwidget.setEnabled(True)

        self.editMenu.setEnabled(True)
        self.saveAction.setEnabled(True)
        self.saveAsAction.setEnabled(True)
        self.closeFileAction.setEnabled(True)

    def initActions(self):

        self.newAction = QAction(QIcon("icons/new.png"), "New", self)
        self.newAction.setShortcut("Ctrl+N")
        self.newAction.setStatusTip("Create a new document from scratch.")
        self.newAction.triggered.connect(self.new)

        self.openAction = QAction(QIcon("icons/open.png"), "Open file", self)
        self.openAction.setStatusTip("Open existing document")
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.triggered.connect(self.open)

        self.saveAction = QAction(QIcon("icons/save.png"), "Save", self)
        self.saveAction.setStatusTip("Save document")
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.save)

        self.closeFileAction = QAction("Close", self)
        self.closeFileAction.setStatusTip("Close opened file")
        # self.closeAction.setShortcut("Ctrl+Shift+P")
        self.closeFileAction.triggered.connect(self.closeFile)

        self.exitAction = QAction("Exit", self)
        self.exitAction.setStatusTip("Exit programm")
        # self.closeAction.setShortcut("Ctrl+Shift+P")
        self.exitAction.triggered.connect(self.exit)

        self.findAction = QAction(QIcon("icons/find.png"), "Find and replace", self)
        self.findAction.setStatusTip("Find and replace words in your document")
        self.findAction.setShortcut("Ctrl+F")
        self.findAction.triggered.connect(self.findAndReplace)

        self.filterAction = QAction(QIcon("icons/find.png"), "Filter notes", self)
        self.filterAction.setStatusTip("Filters notes in notebook")
        # self.filterAction.setShortcut("Ctrl+F")
        self.filterAction.triggered.connect(self.filterNotes)

        self.cutAction = QAction(QIcon("icons/cut.png"), "Cut to clipboard", self)
        self.cutAction.setStatusTip("Delete and copy text to clipboard")
        self.cutAction.setShortcut("Ctrl+X")
        self.cutAction.triggered.connect(self.cut)

        self.copyAction = QAction(QIcon("icons/copy.png"), "Copy to clipboard", self)
        self.copyAction.setStatusTip("Copy text to clipboard")
        self.copyAction.setShortcut("Ctrl+C")
        self.copyAction.triggered.connect(self.copy)

        self.pasteAction = QAction(QIcon("icons/paste.png"), "Paste from clipboard", self)
        self.pasteAction.setStatusTip("Paste text from clipboard")
        self.pasteAction.setShortcut("Ctrl+V")
        self.pasteAction.triggered.connect(self.paste)

        self.undoAction = QAction(QIcon("icons/undo.png"), "Undo last action", self)
        self.undoAction.setStatusTip("Undo last action")
        self.undoAction.setShortcut("Ctrl+Z")
        self.undoAction.triggered.connect(self.undo)

        self.redoAction = QAction(QIcon("icons/redo.png"), "Redo last undone thing", self)
        self.redoAction.setStatusTip("Redo last undone thing")
        self.redoAction.setShortcut("Ctrl+Y")
        self.redoAction.triggered.connect(self.redo)

        self.setDarkThemeAction = QAction("Set dark theme", self)
        self.setDarkThemeAction.setStatusTip("Sets the main theme to dark one.")
        self.setDarkThemeAction.triggered.connect(self.setDarkTheme)

        self.setLightThemeAction = QAction("Set light theme", self)
        self.setLightThemeAction.setStatusTip("Sets the main theme to light one.")
        self.setLightThemeAction.triggered.connect(self.setLightTheme)

    def initMenubar(self):

        menubar = self.menuBar()

        fileMenu = menubar.addMenu("File")
        editMenu = menubar.addMenu("Edit")
        viewMenu = menubar.addMenu("View")
        # helpMenu = menubar.addMenu("Help")

        self.fileMenu = fileMenu
        self.editMenu = editMenu
        self.helpMenu = helpMenu
        self.viewMenu = viewMenu

        # Add the most important actions to the menubar

        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        self.recentFilesMenu = QMenu("Recent Files")
        fileMenu.addMenu(self.recentFilesMenu)

        self.clearRecentAction = QAction("Clear recent files", self)
        self.clearRecentAction.triggered.connect(self.clearRecent)

        fileMenu.addSeparator()

        fileMenu.addAction(self.saveAction)

        self.saveAsAction = QAction(QIcon("icons/save.png"), "Save As", self)
        self.saveAsAction.setStatusTip("Save as document")
        self.saveAsAction.triggered.connect(self.saveAs)
        fileMenu.addAction(self.saveAsAction)

        # fileMenu.addSeparator()

        # fileMenu.addAction(self.printAction)
        # fileMenu.addAction(self.previewAction)

        fileMenu.addSeparator()
        fileMenu.addAction(self.closeFileAction)

        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)

        editMenu.addAction(self.undoAction)
        editMenu.addAction(self.redoAction)
        editMenu.addAction(self.cutAction)
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addAction(self.findAction)
        editMenu.addAction(self.filterAction)

        viewMenu.addAction(self.setLightThemeAction)
        viewMenu.addAction(self.setDarkThemeAction)

    def setDarkTheme(self):
        self.setTheme("dark")

    def setLightTheme(self):
        self.setTheme("light")

    def setTheme(self, theme: str):
        self.app_settings["app_theme"] = theme
        with open(self.app_settings_path, "w") as f:
            f.write(jsonpickle.encode(self.app_settings))

    def filterNotes(self):
        self.noteViewManager.saveChanges()
        dialog = NotebookFilterDialog(parent=self, notebook=self.noteViewManager.notebook)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            self.filteredTreeWidget.load_notebook(dialog.filteredNoteBook)
            self.navigationTabWidget.setCurrentIndex(1)

    def new(self):

        filename = QFileDialog.getSaveFileName(self, 'New File', ".", "Notebook files(*.nbf)")[0]

        if filename:
            if os.path.exists(filename):
                os.remove(filename)

            Notebook.create_empty_notebook(filename, self.settings)
            self.open_notebook(filename)

    def add_recent(self, filename):
        self.recent_files.add(filename)
        self.updateRecent()

    def open_notebook(self, filename):
        self.beforeClose()

        self.notebook = Notebook.from_file(filename)
        self.add_recent(filename)
        self.setWindowTitle(self.app_name + " - " + filename)
        self.filename = filename

        self.afterOpen()

        self.mainTreeWidget.load_notebook(self.notebook)
        self.noteViewManager.notebook = self.notebook

    def open(self):

        self.filename = QFileDialog.getOpenFileName(self, 'Open File', ".", "Notebook files(*.nbf)")[0]

        if self.filename:
            self.open_notebook(self.filename)
            # self.updateRecent()

    def save(self):
        if not hasattr(self, "filename"):
            return

        if not self.filename:
            self.filename = QFileDialog.getSaveFileName(self, 'Save File', ".", "Notebook files(*.nbf)")[0]

        if self.filename:

            # Append extension if not there yet
            if not self.filename.endswith(".nbf"):
                self.filename += ".nbf"

            self.noteViewManager.saveChanges()
            self.notebook.save_to_file(self.filename)

            self.changesSaved = True

    def saveAs(self):
        filename = QFileDialog.getSaveFileName(self, 'Save File', ".", "(*.nbf)")[0]

        if filename:

            # Append extension if not there yet
            if not filename.endswith(".nbf"):
                filename += ".nbf"

            import uuid
            self.noteViewManager.saveChanges()
            notebook = self.notebook.shallow_clone()
            notebook.uuid = str(uuid.uuid1())
            notebook.save_to_file(filename)

            # self.changesSaved = True

    def clearRecent(self):
        self.recent_files = set()
        self.updateRecent()

    def updateRecent(self):
        with open(self.recent_files_config_path, "w") as f:
            f.write(jsonpickle.encode(self.recent_files))

        self.recentFilesMenu.clear()
        for recent_file in self.recent_files:
            action = QAction(recent_file, self)
            action.triggered.connect(lambda checked, recent_file=recent_file:
                                     self.open_notebook(recent_file))
            self.recentFilesMenu.addAction(action)

        self.recentFilesMenu.addSeparator()
        self.recentFilesMenu.addAction(self.clearRecentAction)

    def closeFile(self):
        self.save()
        self.beforeClose()

    def exit(self):
        pass

    def cut(self):
        if (self.noteViewManager.tabWidget.count() > 0):
            self.noteViewManager.getCurrentNoteContentEdit().cut()

    def copy(self):
        if (self.noteViewManager.tabWidget.count() > 0):
            self.noteViewManager.getCurrentNoteContentEdit().copy()

    def paste(self):
        if (self.noteViewManager.tabWidget.count() > 0):
            self.noteViewManager.getCurrentNoteContentEdit().paste()

    def redo(self):
        if (self.noteViewManager.tabWidget.count() > 0):
            self.noteViewManager.getCurrentNoteContentEdit().redo()

    def undo(self):
        if (self.noteViewManager.tabWidget.count() > 0):
            self.noteViewManager.getCurrentNoteContentEdit().undo()

    def findAndReplace(self):
        if (self.noteViewManager.tabWidget.count() > 0):
            Find(self, self.noteViewManager.getCurrentNoteContentEdit()).show()

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.closeFile()
