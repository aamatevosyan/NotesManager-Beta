import pathlib

from PyQt5.QtGui import QIcon


class NoteAttachment:
    extensions_path = pathlib.Path("notes/core/icons/extensions/")

    def __init__(self, name: str, extension: str, uuid: str, file_size: int):
        self.extension = extension
        self.name = name
        self.uuid = uuid
        self.file_size = file_size

    def get_icon(self):
        filename = pathlib.Path.joinpath(NoteAttachment.extensions_path, self.extension + ".png")

        if not pathlib.Path.exists(filename):
            filename = pathlib.Path.joinpath(NoteAttachment.extensions_path, "_blank.png")

        filename = str(filename)
        return QIcon(filename)
