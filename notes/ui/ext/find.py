# PYQT5 PyQt4’s QtGui module has been split into PyQt5’s QtGui, QtPrintSupport and QtWidgets modules

from PyQt5 import QtGui, QtCore
from PyQt5 import QtWidgets


# PYQT5 QTextEdit, QDialog, QPushButton, QRadioButton, QGridLayout

class Find(QtWidgets.QDialog):
    def __init__(self, parent=None, text=None):

        QtWidgets.QDialog.__init__(self, parent)

        self.text = text
        self.parent = parent

        self.lastStart = 0

        self.initUI()

    def initUI(self):

        # Button to search the document for something
        findButton = QtWidgets.QPushButton("Find", self)
        findButton.clicked.connect(self.tryFind)

        # Button to replace the last finding
        replaceButton = QtWidgets.QPushButton("Replace", self)
        replaceButton.clicked.connect(self.replace)

        # Button to remove all findings
        allButton = QtWidgets.QPushButton("Replace all", self)
        allButton.clicked.connect(self.replaceAll)

        # The field into which to type the query
        self.findField = QtWidgets.QTextEdit()
        self.findField.resize(QtCore.QSize(250, 30))

        # The field into which to type the text to replace the
        # queried text
        self.replaceField = QtWidgets.QTextEdit()
        self.replaceField.resize(QtCore.QSize(250, 30))

        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(self.findField)
        # layout.addWidget(self.normalRadio,2,2)
        # layout.addWidget(regexRadio,2,3)
        layout.addWidget(findButton)

        layout.addWidget(self.replaceField)
        layout.addWidget(replaceButton)
        layout.addWidget(allButton)

        self.setGeometry(300, 300, 360, 250)
        self.setWindowTitle("Find and Replace")
        self.setLayout(layout)

        # By default the normal mode is activated
        # self.normalRadio.setChecked(True)

    def tryFind(self):

        # Grab the parent's text
        text = self.text.toPlainText()

        # And the text to find
        query = self.findField.toPlainText()

        # if self.normalRadio.isChecked():

        # Use normal string search to find the query from the
        # last starting position
        self.lastStart = text.find(query, self.lastStart + 1)

        # If the find() method didn't return -1 (not found)
        if self.lastStart >= 0:

            end = self.lastStart + len(query)

            self.moveCursor(self.lastStart, end)

        else:

            # Make the next search start from the begining again
            self.lastStart = 0

            self.text.moveCursor(QtGui.QTextCursor.End)

    def replace(self):
        # Grab the text cursor
        cursor = self.text.textCursor()

        # Security
        if cursor.hasSelection():
            # We insert the new text, which will override the selected
            # text
            cursor.insertText(self.replaceField.toPlainText())

            # And set the new cursor
            self.text.setTextCursor(cursor)

    def replaceAll(self):
        self.lastStart = 0

        self.tryFind()

        # Replace and find until self.lastStart is 0 again
        while self.lastStart:
            self.replace()
            self.tryFind()

    def moveCursor(self, start, end):
        # We retrieve the QTextCursor object from the parent's QTextEdit
        cursor = self.text.textCursor()

        # Then we set the position to the beginning of the last match
        cursor.setPosition(start)

        # Next we move the Cursor by over the match and pass the KeepAnchor parameter
        # which will make the cursor select the the match's text
        cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.KeepAnchor, end - start)

        # And finally we set this new cursor as the parent's
        self.text.setTextCursor(cursor)
