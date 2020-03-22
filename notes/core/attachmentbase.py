import os
import tempfile
import zipfile
from typing import List
from uuid import uuid1

from notes.core.noteattachment import NoteAttachment


class AttachmentBase:

    # default_path = "attachments.json"

    def __init__(self, filename: str, attachments: List[NoteAttachment]):
        self.filename = filename or ""
        self.attachments = attachments or []

    def getuuids(self):
        uuids = []
        for attachment in self.attachments:
            uuids.append(attachment.uuid)
        return uuids

    def add(self, filename):
        if filename == self.filename:
            return None

        _id = str(uuid1())
        _info = os.stat(filename)
        base_name = os.path.basename(filename)
        extension = os.path.splitext(base_name)[1][1:]
        name = os.path.splitext(base_name)[0]
        _size = os.stat(filename).st_size

        attachment = NoteAttachment(name, extension, _id, _size)

        self.attachments.append(attachment)
        with zipfile.ZipFile(self.filename, 'a') as new_zip:
            new_zip.write(filename, _id)

        return attachment

    def remove(self, uuid: str):
        result: NoteAttachment = list(filter(lambda x: x.uuid == uuid, self.attachments))[0]

        self.attachments.remove(result)

    def save_to_file(self, filename: str, uuid: str):
        with zipfile.ZipFile(self.filename, "r") as zip_file:
            zipinfo = zip_file.getinfo(uuid)
            zipinfo.filename = os.path.basename(filename)
            zip_file.extract(uuid, os.path.dirname(filename))

    def open_with_default_app(self, uuid: str):
        result: NoteAttachment = list(filter(lambda x: x.uuid == uuid, self.attachments))[0]

        tmp_file = tempfile.NamedTemporaryFile(suffix="-" + result.name + "." + result.extension)
        tmp_file.close()

        self.save_to_file(tmp_file.name, uuid)

        os.startfile(tmp_file.name)
