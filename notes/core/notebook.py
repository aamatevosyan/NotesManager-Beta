import os
import pathlib
import shutil
import tempfile
import zipfile
from typing import List
from uuid import uuid1

import html2text
import jsonpickle

from notes.core.attachmentbase import AttachmentBase
from notes.core.categorybase import CategoryBase
from notes.core.notebooksettings import NotebookSettings
from notes.core.tagbase import TagBase
from .section import Section

jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)


def remove_from_zip(zipfname, *filenames):
    tempdir = tempfile.mkdtemp()
    try:
        tempname = os.path.join(tempdir, 'new.zip')
        with zipfile.ZipFile(zipfname, 'r') as zipread:
            with zipfile.ZipFile(tempname, 'w') as zipwrite:
                for item in zipread.infolist():
                    if item.filename not in filenames:
                        data = zipread.read(item.filename)
                        zipwrite.writestr(item, data)
        shutil.move(tempname, zipfname)
    finally:
        shutil.rmtree(tempdir)


def get_removable_files(zipfname, *filenames):
    toRemove = []
    try:
        with zipfile.ZipFile(zipfname, 'r') as zipread:
            for item in zipread.infolist():
                if item.filename not in filenames:
                    toRemove.append(item.filename)
    finally:
        return toRemove


class Notebook:
    default_path = "notebook.json"

    def __init__(self, name: str, sections: List[Section], category_base: CategoryBase, tag_base: TagBase,
                 attachment_base: AttachmentBase, settings: NotebookSettings):
        self.attachment_base = attachment_base
        self.settings = settings
        self.category_base = category_base
        self.tag_base = tag_base
        self.sections = sections or []
        self.name = name or ""
        self.uuid = str(uuid1())

        jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)

    def __iter__(self):
        return iter(self.sections)

    @classmethod
    def create_empty_notebook(cls, filename: str, settings: NotebookSettings):
        with zipfile.ZipFile(filename, 'w') as file:
            pass

        notebook = cls("Notebook", [], CategoryBase(settings.categories()), TagBase({}), AttachmentBase(filename, []),
                       settings)
        notebook.save_to_file(filename)

    @classmethod
    def from_file(cls, filename: str):
        with zipfile.ZipFile(filename, "r") as zip_file:
            notebook: Notebook = jsonpickle.decode(zip_file.read(Notebook.default_path))

        notebook.attachment_base.filename = filename
        # notebook.attachment_base = AttachmentBase.from_file(filename)

        return notebook

    def shallow_clone(self):
        return jsonpickle.decode(jsonpickle.encode(self))

    def save_to_file(self, filename):

        if not pathlib.Path(filename).exists():
            with zipfile.ZipFile(filename, 'w') as file:
                pass

        to_remove = get_removable_files(filename, *self.attachment_base.getuuids())

        remove_from_zip(filename, *to_remove)

        with zipfile.ZipFile(filename, 'a') as new_zip:
            new_zip.writestr("notebook.json", jsonpickle.encode(self))

    def get_note_by_uuid(self, uuid: str):
        for section in self:
            for subsection in section:
                for note in subsection:
                    if note.uuid == uuid:
                        return note

    def remove_empty_sections(self):
        sections = []
        for section in self:
            subsections = []
            for subsection in section:
                if len(subsection.notes) > 0:
                    subsections.append(subsection)
            section.subsections = subsections

            if len(section.subsections) > 0:
                sections.append(section)
        self.sections = sections

        return self

    def filter_notes(self, note_filter: str, tags_filter: List[str]):
        for section in self.sections:
            for subsection in section.subsections:
                remove_id = []
                for i in range(len(subsection.notes)):
                    note = subsection.notes[i]
                    text = note.name + html2text.html2text(note.content)
                    tags = note.tags

                    if text.find(note_filter) == -1:
                        remove_id.append(i)
                    elif len(tags_filter) > 0 and not any(item in tags for item in tags_filter):
                        remove_id.append(i)

                notes = []
                for i in range(len(subsection.notes)):
                    if i not in remove_id:
                        notes.append(subsection.notes[i])
                subsection.notes = notes

        return self
