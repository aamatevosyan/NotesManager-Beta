from typing import Dict

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QListView


class NotebookSettings:
    font_size = "font_size"
    font_style = "font_style"
    font_info = "font_info"
    attachments_view_mode = "attachments_view_mode"
    date_time_insert_style = "date_time_insert_style"
    note_categories = "note_categories"

    def __init__(self, settings: Dict):
        self.settings = settings

    def font(self) -> QFont:
        font = QFont()
        font.fromString(self.settings[NotebookSettings.font_info])
        return font

    def fontStyle(self):
        return self.font().family()

    def setFontStyle(self, style: str):
        font = QFont()
        font.fromString(self.settings[NotebookSettings.font_info])
        font.setFamily(style)

        self.settings[NotebookSettings.font_info] = font.toString()

    def setFontSize(self, size: str):
        font = QFont()
        font.fromString(self.settings[NotebookSettings.font_info])
        font.setPointSize(int(size))

        self.settings[NotebookSettings.font_info] = font.toString()

    def setAttachmentsViewMode(self, mode: str):
        self.settings[NotebookSettings.attachments_view_mode] = mode

    def setDateFormat(self, format: str):
        self.settings[NotebookSettings.date_time_insert_style] = format

    def fontSize(self):
        return self.font().pointSize()

    def attachments_list_view_mode(self):
        if self.settings[NotebookSettings.attachments_view_mode] == "icon":
            return QListView.IconMode
        else:
            return QListView.ListMode

    def attachments_list_icon_size(self):
        if self.settings[NotebookSettings.attachments_view_mode] == "icon":
            return QSize(100, 100)
        else:
            return QSize(32, 32)

    def attachments_list_view_mode_string(self):
        return self.settings[NotebookSettings.attachments_view_mode]

    def date_time_insert_format(self):
        return self.settings[NotebookSettings.date_time_insert_style]

    def categories(self):
        return self.settings[NotebookSettings.note_categories]
