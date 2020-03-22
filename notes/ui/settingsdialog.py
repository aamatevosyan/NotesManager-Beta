from time import strftime

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from notes import NotebookSettings
from notes.core.config import ConfigManager


class NotebookSettingsDialog(QDialog):

    def __init__(self, parent=None, settings: NotebookSettings = None):
        super(QDialog, self).__init__(parent, Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint | Qt.WindowTitleHint)
        self.settings = settings
        self.setWindowTitle("Manage tags")

        self.config = ConfigManager()

        self.config.set_defaults({
            "Date insert format": settings.date_time_insert_format(),
            "Attachments view mode": settings.attachments_list_view_mode_string(),
            "Font family": settings.fontStyle(),
            "Font size": settings.fontSize()
        })

        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)

        self.initUI()

    def initUI(self):
        allLayout = QGridLayout()

        layout = QVBoxLayout()

        labelLayout = QVBoxLayout()
        allLayout.addWidget(QLabel("Date insert format"), 0, 0)
        allLayout.addWidget(QLabel("Attachments view mode"), 1, 0)
        allLayout.addWidget(QLabel("Font family"), 2, 0)
        allLayout.addWidget(QLabel("Font size"), 3, 0)

        self.dateFormatEdit = QComboBox()
        self.attachmentsViewModeEdit = QComboBox()
        self.fontFamilyEdit = QComboBox()
        self.fontSizeEdit = QSpinBox()

        self.dateformats = ["%A, %d. %B %Y %H:%M",
                            "%A, %d. %B %Y",
                            "%d. %B %Y %H:%M",
                            "%d.%m.%Y %H:%M",
                            "%d. %B %Y",
                            "%d %m %Y",
                            "%d.%m.%Y",
                            "%x",
                            "%X",
                            "%H:%M"]

        self.dateFormatMapper = {}

        for i in range(len(self.dateformats)):
            self.dateFormatMapper[strftime(self.dateformats[i])] = self.dateformats[i]

        self.dateFormatEdit.addItems(self.dateFormatMapper.keys())
        self.dateFormatEdit.setCurrentIndex(self.dateformats.index(self.config.get("Date insert format")))

        self.config.add_handler("Date insert format", self.dateFormatEdit, self.dateFormatMapper)

        self.attachmentsViewModeMapper = {
            "Icon": "icon",
            "List": "list"
        }

        self.attachmentsViewModeEdit.addItems(self.attachmentsViewModeMapper.keys())
        self.config.add_handler("Attachments view mode", self.attachmentsViewModeEdit,
                                mapper=self.attachmentsViewModeMapper)

        with open("fonts.txt", "r") as f:
            self.fontFamilyEdit.addItems(f.readlines())

        self.fontFamilyEdit.setCurrentText(self.config.get("Font family"))

        self.config.add_handler("Font family", self.fontFamilyEdit)

        self.fontSizeEdit.setMinimum(0)

        self.config.add_handler("Font size", self.fontSizeEdit)

        allLayout.addWidget(self.dateFormatEdit, 0, 1)
        allLayout.addWidget(self.attachmentsViewModeEdit, 1, 1)
        allLayout.addWidget(self.fontFamilyEdit, 2, 1)
        allLayout.addWidget(self.fontSizeEdit, 3, 1)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.setCenterButtons(True)
        buttons.accepted.connect(self.onAccept)
        buttons.rejected.connect(self.reject)

        tmpWidget = QWidget()
        tmpWidget.setLayout(allLayout)

        layout.addWidget(tmpWidget)
        layout.addWidget(buttons, Qt.AlignCenter)

        # allLayout.addWidget(labelWidget)
        # allLayout.addWidget(justWidget)

        self.setLayout(layout)

    def onAccept(self):
        self.updateSettings()
        self.close()

    def updateSettings(self):
        self.settings.setFontSize(self.config.get("Font size"))
        self.settings.setFontStyle(self.config.get("Font family"))
        self.settings.setAttachmentsViewMode(self.config.get("Attachments view mode"))
        self.settings.setDateFormat(self.config.get("Date insert format"))
