import json
import os
import shutil
from tkinter import messagebox


class StudyManager:

    def __init__(self):

        self.notes_folder = "data/study_notes"
        self.index_file = "data/study_index.json"

        os.makedirs(
            self.notes_folder,
            exist_ok=True
        )

        if not os.path.exists(self.index_file):

            with open(
                self.index_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    [],
                    file,
                    indent=4
                )

    def load_notes(self):

        with open(
            self.index_file,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    def save_notes(self, notes):

        with open(
            self.index_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                notes,
                file,
                indent=4
            )

    def add_pdf(self, file_path):

        filename = os.path.basename(file_path)

        destination = os.path.join(
            self.notes_folder,
            filename
        )

        shutil.copy2(
            file_path,
            destination
        )

        notes = self.load_notes()

        notes.append({
            "name": filename,
            "path": destination
        })

        self.save_notes(notes)

    def delete_pdf(self, note):

        if os.path.exists(note["path"]):

            os.remove(note["path"])

        notes = self.load_notes()

        if note in notes:
            notes.remove(note)

        self.save_notes(notes)

    def delete_note(self, index):

        notes = self.load_notes()

        if index < 0 or index >= len(notes):
            return

        note = notes[index]

        # Ask BEFORE deleting anything
        if not messagebox.askyesno(
            "Delete Note",
            "Delete the selected note?"
        ):
            return

        if os.path.exists(note["path"]):

            os.remove(note["path"])

        notes.pop(index)

        self.save_notes(notes)