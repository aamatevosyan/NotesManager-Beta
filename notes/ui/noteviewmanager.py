from time import strftime

from PyQt5.QtCore import QSize, Qt, QUrl, QUrlQuery
from PyQt5.QtGui import QIcon, QFont, QTextCharFormat, QTextCursor, QTextListFormat, QImage
from PyQt5.QtPrintSupport import QPrintPreviewDialog, QPrintDialog
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFontComboBox, QSpinBox, QAction, QToolBar, QColorDialog, \
    QDialog, QFileDialog, QMessageBox

from notes import Note, Notebook
from notes.ui.collapsiblebox import CollapsibleBox
from notes.ui.ext import WordCount, Table
from notes.ui.linkadddialog import LinkAddDialog
from notes.ui.noteattachmentsview import NoteAttachmentsView
from notes.ui.notecontentedit import NoteContentEdit
from notes.ui.notehistoryview import NoteHistoryView
from notes.ui.noteselectdialog import NoteSelectDialog
from notes.ui.tabwidget import TabWidget


class NoteViewManager:

    def __init__(self, tabWidget: TabWidget, notebook: Notebook):
        self.notebook = notebook
        self.tabWidget = tabWidget
        self.tabWidget.tabCloseRequested.connect(self.onTabCloseRequested)
        self.tabWidget.currentChanged.connect(self.onCurrentChanged)
        self.tabWidget.tabBarDoubleClicked.connect(self.onTabBarDoubleClicked)

    def openNote(self, note: Note):
        for i in range(self.tabWidget.count()):
            tab = self.tabWidget.widget(i)

            if tab.note.uuid == note.uuid:
                self.tabWidget.setCurrentIndex(i)
                return

        self.tabWidget.addTab(NoteView(None, self, note), note.name)
        self.tabWidget.setCurrentIndex(self.tabWidget.count() - 1)
        self.tabWidget.setTabIcon(self.tabWidget.currentIndex(), note.category.get_icon())

        self.tabWidget.colorTab(self.tabWidget.currentIndex(), note.notecolor)

    def saveChangesAt(self, index: int):
        self.tabWidget.widget(index).saveChanges()

    def saveChanges(self):
        for i in range(self.tabWidget.count()):
            self.saveChangesAt(index=i)

    def getCurrentNoteContentEdit(self):
        current: NoteView = self.tabWidget.currentWidget()
        return current.noteContentEdit

    def removeNote(self, note: Note):
        for i in range(self.tabWidget.count()):
            tab = self.tabWidget.widget(i)

            if tab.note.uuid == note.uuid:
                self.tabWidget.removeTab(i)
                return

    def updateIcon(self, note: Note):
        for i in range(self.tabWidget.count()):
            tab = self.tabWidget.widget(i)

            if tab.note.uuid == note.uuid:
                self.tabWidget.setTabIcon(i, note.category.get_icon())
                return

    def updateName(self, note: Note):
        for i in range(self.tabWidget.count()):
            tab = self.tabWidget.widget(i)

            if tab.note.uuid == note.uuid:
                self.tabWidget.setTabText(i, note.name)
                return

    def removeTab(self, index: int):
        self.tabWidget.removeTab(index)

    def closeAll(self):
        for i in range(self.tabWidget.count()):
            self.tabWidget.removeTab(0)

    def onTabCloseRequested(self, index: int):
        self.tabWidget.widget(index).saveChanges()
        self.removeTab(index)

    def onCurrentChanged(self, index: int):
        self.tabWidget.currentWidget()

    def onTabBarDoubleClicked(self, index: int):
        color = QColorDialog.getColor()

        name = color.name()
        print(name)

        if name != "#000000":
            tab = self.tabWidget.widget(index)
            tab.note.notecolor = name
            self.tabWidget.colorTab(self.tabWidget.currentIndex(), tab.note.notecolor)


class NoteView(QWidget):

    def __init__(self, parent: QWidget, noteViewManager: NoteViewManager, note: Note):
        super(QWidget, self).__init__(parent)

        self.noteViewManager = noteViewManager
        self.note = note
        self.notebook = self.noteViewManager.notebook
        self.setLayout(QVBoxLayout(self))

        self.lay = self.layout()

        self.noteContentEdit = NoteContentEdit(self, self.notebook, note)
        self.noteContentEdit.anchorClicked.connect(self.onAnchorClicked)

        self.attachmentsView = NoteAttachmentsView(self, self.notebook, note)

        self.attachmentsBox = CollapsibleBox(title="Attachments")

        tmpLay = QVBoxLayout()
        tmpLay.addWidget(self.attachmentsView)
        self.attachmentsBox.setContentLayout(tmpLay)
        self.attachmentsBox.setContentsMargins(0, 0, 0, 0)

        self.initFormatbar()

        self.fontBox.setCurrentFont(self.notebook.settings.font())
        self.fontSize.setValue(self.notebook.settings.font().pointSize())

        self.noteContentEdit.currentCharFormatChanged.connect(self.onCurrentCharFormatChanged)

        self.lay.addWidget(self.noteContentEdit)
        self.lay.addWidget(self.attachmentsBox)

    def initFormatbar(self):

        self.fontBox = QFontComboBox()
        self.fontBox.setCurrentFont(self.noteContentEdit.font())
        self.fontBox.currentFontChanged.connect(lambda font: self.noteContentEdit.setCurrentFont(font))

        # self.families = list(self.fontBox.itemText(i) for i in range(self.fontBox.count()))
        #
        # with open("fonts.txt", "w") as f:
        #     for name in self.families:
        #         f.write(name + "\r\n")

        self.fontSize = QSpinBox()
        self.fontSize.setValue(self.noteContentEdit.fontPointSize())
        self.fontSize.adjustSize()
        self.fontSize.setSuffix(" pt")

        self.fontSize.valueChanged.connect(lambda size: self.noteContentEdit.setFontPointSize(size))

        fontColor = QAction(QIcon("icons/font-color.png"), "Change font color", self)
        fontColor.triggered.connect(self.fontColorChanged)

        boldAction = QAction(QIcon("icons/bold.png"), "Bold", self)
        boldAction.triggered.connect(self.bold)

        italicAction = QAction(QIcon("icons/italic.png"), "Italic", self)
        italicAction.triggered.connect(self.italic)

        underlAction = QAction(QIcon("icons/underline.png"), "Underline", self)
        underlAction.triggered.connect(self.underline)

        strikeAction = QAction(QIcon("icons/strike.png"), "Strike-out", self)
        strikeAction.triggered.connect(self.strike)

        superAction = QAction(QIcon("icons/superscript.png"), "Superscript", self)
        superAction.triggered.connect(self.superScript)

        subAction = QAction(QIcon("icons/subscript.png"), "Subscript", self)
        subAction.triggered.connect(self.subScript)

        alignLeft = QAction(QIcon("icons/align-left.png"), "Align left", self)
        alignLeft.triggered.connect(self.alignLeft)

        alignCenter = QAction(QIcon("icons/align-center.png"), "Align center", self)
        alignCenter.triggered.connect(self.alignCenter)

        alignRight = QAction(QIcon("icons/align-right.png"), "Align right", self)
        alignRight.triggered.connect(self.alignRight)

        alignJustify = QAction(QIcon("icons/align-justify.png"), "Align justify", self)
        alignJustify.triggered.connect(self.alignJustify)

        indentAction = QAction(QIcon("icons/indent.png"), "Indent Area", self)
        indentAction.setShortcut("Ctrl+Tab")
        indentAction.triggered.connect(self.indent)

        dedentAction = QAction(QIcon("icons/dedent.png"), "Dedent Area", self)
        dedentAction.setShortcut("Shift+Tab")
        dedentAction.triggered.connect(self.dedent)

        backColor = QAction(QIcon("icons/highlight.png"), "Change background color", self)
        backColor.triggered.connect(self.highlight)

        bulletAction = QAction(QIcon("icons/bullet.png"), "Insert bullet List", self)
        bulletAction.setStatusTip("Insert bullet list")
        bulletAction.setShortcut("Ctrl+Shift+B")
        bulletAction.triggered.connect(self.bulletList)

        numberedAction = QAction(QIcon("icons/number.png"), "Insert numbered List", self)
        numberedAction.setStatusTip("Insert numbered list")
        numberedAction.setShortcut("Ctrl+Shift+L")
        numberedAction.triggered.connect(self.numberList)

        dateTimeAction = QAction(QIcon("icons/calender.png"), "Insert current date/time", self)
        dateTimeAction.setStatusTip("Insert current date/time")
        dateTimeAction.setShortcut("Ctrl+D")
        dateTimeAction.triggered.connect(self.insertDateTime)

        wordCountAction = QAction(QIcon("icons/count.png"), "See word/symbol count", self)
        wordCountAction.setStatusTip("See word/symbol count")
        wordCountAction.setShortcut("Ctrl+W")
        wordCountAction.triggered.connect(self.wordCount)

        tableAction = QAction(QIcon("icons/table.png"), "Insert table", self)
        tableAction.setStatusTip("Insert table")
        tableAction.setShortcut("Ctrl+T")
        tableAction.triggered.connect(self.insertTable)

        imageAction = QAction(QIcon("icons/image.png"), "Insert image", self)
        imageAction.setStatusTip("Insert image")
        imageAction.setShortcut("Ctrl+Shift+I")
        imageAction.triggered.connect(self.insertImage)

        linkAction = QAction(QIcon("icons/insert_link.png"), "Insert link", self)
        linkAction.setStatusTip("Insert link")
        # linkAction.setShortcut("Ctrl+Shift+L")
        linkAction.triggered.connect(self.insertLink)

        linkNoteAction = QAction(QIcon("icons/insert_note_link.png"), "Insert note link", self)
        linkNoteAction.setStatusTip("Insert note link")
        # linkAction.setShortcut("Ctrl+Shift+L")
        linkNoteAction.triggered.connect(self.insertNoteLink)

        attachAction = QAction(QIcon("icons/attach.png"), "Insert attachment", self)
        attachAction.setStatusTip("Insert attachment")
        attachAction.triggered.connect(self.insertAttachment)

        printAction = QAction(QIcon("icons/print.png"), "Print document", self)
        printAction.setStatusTip("Print document")
        printAction.setShortcut("Ctrl+P")
        printAction.triggered.connect(self.printHandler)

        previewAction = QAction(QIcon("icons/preview.png"), "Page view", self)
        previewAction.setStatusTip("Preview page before printing")
        previewAction.setShortcut("Ctrl+Shift+P")
        previewAction.triggered.connect(self.preview)

        viewHistoryAction = QAction(QIcon("icons/history.png"), "Show history", self)
        viewHistoryAction.setStatusTip("View note content history")
        viewHistoryAction.setShortcut("Ctrl+H")
        viewHistoryAction.triggered.connect(self.showHistory)

        self.formatbar = QToolBar("Format")
        self.formatbar.setIconSize(QSize(16, 16))

        self.lay.addWidget(self.formatbar)

        self.formatbar.addWidget(self.fontBox)
        self.formatbar.addWidget(self.fontSize)

        self.formatbar.addSeparator()

        self.formatbar.addAction(fontColor)
        self.formatbar.addAction(backColor)

        self.formatbar.addSeparator()

        self.formatbar.addAction(boldAction)
        self.formatbar.addAction(italicAction)
        self.formatbar.addAction(underlAction)
        self.formatbar.addAction(strikeAction)
        self.formatbar.addAction(superAction)
        self.formatbar.addAction(subAction)

        self.formatbar.addSeparator()

        self.formatbar.addAction(alignLeft)
        self.formatbar.addAction(alignCenter)
        self.formatbar.addAction(alignRight)
        self.formatbar.addAction(alignJustify)

        self.formatbar.addSeparator()

        self.formatbar.addAction(indentAction)
        self.formatbar.addAction(dedentAction)

        self.formatbar.addSeparator()

        self.formatbar.addAction(bulletAction)
        self.formatbar.addAction(numberedAction)

        self.formatbar.addSeparator()

        self.formatbar.addAction(wordCountAction)
        self.formatbar.addAction(tableAction)
        self.formatbar.addAction(dateTimeAction)
        self.formatbar.addAction(imageAction)

        self.formatbar.addSeparator()

        self.formatbar.addAction(linkAction)
        self.formatbar.addAction(linkNoteAction)
        self.formatbar.addAction(attachAction)

        self.formatbar.addSeparator()

        self.formatbar.addAction(viewHistoryAction)
        self.formatbar.addAction(previewAction)
        self.formatbar.addAction(printAction)

    def saveChanges(self):
        self.noteContentEdit.saveChanges()

    def fontColorChanged(self):

        # Get a color from the text dialog
        color = QColorDialog.getColor()

        # Set it as the new text color
        self.noteContentEdit.setTextColor(color)

    def highlight(self):

        color = QColorDialog.getColor()

        self.noteContentEdit.setTextBackgroundColor(color)

    def bold(self):

        if self.noteContentEdit.fontWeight() == QFont.Bold:

            self.noteContentEdit.setFontWeight(QFont.Normal)

        else:

            self.noteContentEdit.setFontWeight(QFont.Bold)

    def italic(self):

        state = self.noteContentEdit.fontItalic()

        self.noteContentEdit.setFontItalic(not state)

    def underline(self):

        state = self.noteContentEdit.fontUnderline()

        self.noteContentEdit.setFontUnderline(not state)

    def strike(self):

        # Grab the text's format
        fmt = self.noteContentEdit.currentCharFormat()

        # Set the fontStrikeOut property to its opposite
        fmt.setFontStrikeOut(not fmt.fontStrikeOut())

        # And set the next char format
        self.noteContentEdit.setCurrentCharFormat(fmt)

    def superScript(self):

        # Grab the current format
        fmt = self.noteContentEdit.currentCharFormat()

        # And get the vertical alignment property
        align = fmt.verticalAlignment()

        # Toggle the state
        if align == QTextCharFormat.AlignNormal:

            fmt.setVerticalAlignment(QTextCharFormat.AlignSuperScript)

        else:

            fmt.setVerticalAlignment(QTextCharFormat.AlignNormal)

        # Set the new format
        self.noteContentEdit.setCurrentCharFormat(fmt)

    def subScript(self):

        # Grab the current format
        fmt = self.noteContentEdit.currentCharFormat()

        # And get the vertical alignment property
        align = fmt.verticalAlignment()

        # Toggle the state
        if align == QTextCharFormat.AlignNormal:

            fmt.setVerticalAlignment(QTextCharFormat.AlignSubScript)

        else:

            fmt.setVerticalAlignment(QTextCharFormat.AlignNormal)

        # Set the new format
        self.noteContentEdit.setCurrentCharFormat(fmt)

    def alignLeft(self):
        self.noteContentEdit.setAlignment(Qt.AlignLeft)

    def alignRight(self):
        self.noteContentEdit.setAlignment(Qt.AlignRight)

    def alignCenter(self):
        self.noteContentEdit.setAlignment(Qt.AlignCenter)

    def alignJustify(self):
        self.noteContentEdit.setAlignment(Qt.AlignJustify)

    def indent(self):

        # Grab the cursor
        cursor = self.noteContentEdit.textCursor()

        if cursor.hasSelection():

            # Store the current line/block number
            temp = cursor.blockNumber()

            # Move to the selection's end
            cursor.setPosition(cursor.anchor())

            # Calculate range of selection
            diff = cursor.blockNumber() - temp

            direction = QTextCursor.Up if diff > 0 else QTextCursor.Down

            # Iterate over lines (diff absolute value)
            for n in range(abs(diff) + 1):
                # Move to start of each line
                cursor.movePosition(QTextCursor.StartOfLine)

                # Insert tabbing
                cursor.insertText("\t")

                # And move back up
                cursor.movePosition(direction)

        # If there is no selection, just insert a tab
        else:

            cursor.insertText("\t")

    def handleDedent(self, cursor):

        cursor.movePosition(QTextCursor.StartOfLine)

        # Grab the current line
        line = cursor.block().text()

        # If the line starts with a tab character, delete it
        if line.startswith("\t"):

            # Delete next character
            cursor.deleteChar()

        # Otherwise, delete all spaces until a non-space character is met
        else:
            for char in line[:8]:

                if char != " ":
                    break

                cursor.deleteChar()

    def dedent(self):

        cursor = self.noteContentEdit.textCursor()

        if cursor.hasSelection():

            # Store the current line/block number
            temp = cursor.blockNumber()

            # Move to the selection's last line
            cursor.setPosition(cursor.anchor())

            # Calculate range of selection
            diff = cursor.blockNumber() - temp

            direction = QTextCursor.Up if diff > 0 else QTextCursor.Down

            # Iterate over lines
            for n in range(abs(diff) + 1):
                self.handleDedent(cursor)

                # Move up
                cursor.movePosition(direction)

        else:
            self.handleDedent(cursor)

    def bulletList(self):

        cursor = self.noteContentEdit.textCursor()

        # Insert bulleted list
        cursor.insertList(QTextListFormat.ListDisc)

    def numberList(self):

        cursor = self.noteContentEdit.textCursor()

        # Insert list with numbers
        cursor.insertList(QTextListFormat.ListDecimal)

    def insertTable(self):
        Table(parent=self, text=self.noteContentEdit).show()

    def insertDateTime(self):
        # Grab cursor
        cursor = self.noteContentEdit.textCursor()

        datetime = strftime(self.noteViewManager.notebook.settings.date_time_insert_format())

        # Insert the comboBox's current text
        cursor.insertText(datetime)

    def wordCount(self):

        wc = WordCount(self, self.noteContentEdit)
        wc.text = self.noteContentEdit

        wc.getText()

        wc.show()

    def insertHyperLynk(self, url: str):
        cursor = QTextCursor(self.noteContentEdit.document())
        format = QTextCharFormat()
        format.setAnchor(True)
        format.setAnchorHref(url)
        cursor.mergeBlockCharFormat(format)

    def insertLink(self):

        dialog = LinkAddDialog(self.noteContentEdit)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            cursor = self.noteContentEdit.textCursor()
            linkAdress = dialog.linkAdress
            linkCaption = dialog.linkCaption

            url = QUrl.fromUserInput(linkAdress)
            linkAdress = url.toString()
            cursor.insertHtml(f"<a href=\"{linkAdress}\" >{linkCaption}</a>")

    def insertNoteLink(self):
        cursor = self.noteContentEdit.textCursor()

        filename = QFileDialog.getOpenFileName(self.noteContentEdit, 'Open File', ".", "(*.nbf)")[0]

        if filename:
            notebook = Notebook.from_file(filename)
            dialog = NoteSelectDialog(parent=self, notebook=notebook)
            result = dialog.exec_()

            if result == QDialog.Accepted:
                url: QUrl = QUrl.fromLocalFile(filename)
                url.setScheme("notesmanager")
                query = QUrlQuery()
                query.addQueryItem("uuid", str(dialog.selectedNote.uuid))
                url.setQuery(query)
                cursor.insertHtml(f"<a href=\"{url.toString()}\" >{dialog.caption}</a>")

        # self.text.setReadOnly(True)
        # self.insertHyperLynk("www.google.com")

    def preview(self):

        # Open preview dialog
        preview = QPrintPreviewDialog()

        # If a print is requested, open print dialog
        preview.paintRequested.connect(lambda p: self.noteContentEdit.print_(p))

        preview.exec_()

    def printHandler(self):

        # Open printing dialog
        dialog = QPrintDialog()

        if dialog.exec_() == QDialog.Accepted:
            self.noteContentEdit.document().print_(dialog.printer())

    def showHistory(self):
        self.noteViewManager.saveChanges()

        dialog = NoteHistoryView(self, self.note)

        if dialog.exec_() == QDialog.Accepted:
            self.note.restore(dialog.restoreIndex)
            self.noteContentEdit.setHtml(self.note.content)

    def insertImage(self):

        # Get image file name
        # PYQT5 Returns a tuple in PyQt5
        filename = \
            QFileDialog.getOpenFileName(self.noteContentEdit, 'Insert image', ".",
                                        "Images (*.png *.xpm *.jpg *.bmp *.gif)")[
                0]

        if filename:

            # Create image object
            image = QImage(filename)

            # Error if unloadable
            if image.isNull():

                popup = QMessageBox(QMessageBox.Critical,
                                    "Image load error",
                                    "Could not load image file!",
                                    QMessageBox.Ok,
                                    self.noteContentEdit)
                popup.show()

            else:

                # from PIL import Image, ImageDraw
                import base64
                import os

                content_type = "image/" + os.path.splitext(filename)[1][1:]
                raw_data = base64.b64encode(open(filename, "rb").read())
                uri = ("data:" +
                       content_type + ";" +
                       "base64," + raw_data.decode())
                html_code = '<img src="' + uri + '"/>'
                print(html_code)

                cursor = self.noteContentEdit.textCursor()
                cursor.insertHtml(html_code)
                # random_filename = self.get_random_file_name(os.path.splitext(filename)[1][1:])
                # from shutil import copy
                # copy(filename, dst=random_filename)
                # cursor.insertImage(image, random_filename)
                # cursor.insertHtml(html)

    def onCurrentCharFormatChanged(self, format: QTextCharFormat) -> None:
        if format.isAnchor():
            new_format = QTextCharFormat()
            new_format.setFont(self.fontBox.currentFont())
            new_format.setFontPointSize(self.fontSize.value())
            self.noteContentEdit.setCurrentCharFormat(new_format)

    def onAnchorClicked(self, url: QUrl):
        from notes.ui.MainWindow import MainWindow
        import webbrowser

        host = url.host()
        print(url.scheme())
        scheme = url.scheme()

        if scheme == "http" or scheme == "https":
            webbrowser.open(url.toString())
        elif scheme == "notesmanager":
            url.setScheme("file")

            local_path = url.toLocalFile()
            query = QUrlQuery(url)
            uuid = query.queryItemValue("uuid")

            if local_path == self.notebook.attachment_base.filename:
                self.noteViewManager.openNote(self.noteViewManager.notebook.get_note_by_uuid(uuid))
            else:
                spawn = MainWindow(None, local_path, uuid)
                spawn.show()

    def insertAttachment(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFiles)

        filenames = dialog.getOpenFileNames(self, 'Insert attachments', ".")[0]

        self.attachmentsView.addAttachments(filenames)
