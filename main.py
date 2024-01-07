import json
import datetime


class Note:
    def __init__(self, id, title, body, created, last_modified):
        self.id = id
        self.title = title
        self.body = body
        self.created = created
        self.last_modified = last_modified


class NoteController:
    def __init__(self):
        self.notes = []

    def save_note(self, note):
        with open('notes.json', 'a') as file:
            json.dump(note.__dict__, file)
            file.write('\n')

    def read_notes(self):
        with open('notes.json', 'r') as file:
            for line in file:
                note_data = json.loads(line)
                note = Note(**note_data)
                self.notes.append(note)

    def add_note(self):
        id = input('Enter note ID: ')
        title = input('Enter note title: ')
        body = input('Enter note body: ')
        created = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        last_modified = created

        note = Note(id, title, body, created, last_modified)
        self.save_note(note)
        print('Note added successfully!')

    def edit_note(self):
        id = input('Enter note ID to edit: ')

        with open('notes.json', 'r+') as file:
            lines = file.readlines()
            file.seek(0)

            for line in lines:
                note_data = json.loads(line)
                note = Note(**note_data)

                if note.id == id:
                    title = input('Enter new title: ')
                    body = input('Enter new body: ')
                    last_modified = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    note.title = title
                    note.body = body
                    note.last_modified = last_modified

                self.save_note(note)
                file.write('\n')

        print('Note edited successfully!')

    def delete_note(self):
        id = input('Enter note ID to delete: ')

        with open('notes.json', 'r+') as file:
            lines = file.readlines()
            file.seek(0)

            for line in lines:
                note_data = json.loads(line)
                note = Note(**note_data)

                if note.id != id:
                    self.save_note(note)
                    file.write('\n')

            file.truncate()

        print('Note deleted successfully!')

    def filter_notes_by_date(self, start_date, end_date):
        filtered_notes = []

        for note in self.notes:
            note_date = datetime.datetime.strptime(note.created, '%Y-%m-%d %H:%M:%S')

            if start_date <= note_date <= end_date:
                filtered_notes.append(note)

        return filtered_notes


class NoteView:
    def display_notes(self, notes):
        for note in notes:
            print('ID:', note.id)
            print('Title:', note.title)
            print('Body:', note.body)
            print('Created:', note.created)
            print('Last Modified:', note.last_modified)
            print('---------------------------')

    def menu(self):
        print('Note App')
        print('---------------------------')
        print('1. Read notes')
        print('2. Add note')
        print('3. Edit note')
        print('4. Delete note')
        print('5. Filter notes by date')
        print('6. Exit')
        print('---------------------------')

        choice = input('Enter your choice: ')
        return choice

    def run(self):
        controller = NoteController()

        while True:
            choice = self.menu()

            if choice == '1':
                controller.read_notes()
                self.display_notes(controller.notes)
            elif choice == '2':
                controller.add_note()
            elif choice == '3':
                controller.edit_note()
            elif choice == '4':
                controller.delete_note()
            elif choice == '5':
                start_date = datetime.datetime.strptime(input('Enter start date (YYYY-MM-DD): '), '%Y-%m-%d')
                end_date = datetime.datetime.strptime(input('Enter end date (YYYY-MM-DD): '), '%Y-%m-%d')
                filtered_notes = controller.filter_notes_by_date(start_date, end_date)
                self.display_notes(filtered_notes)
            elif choice == '6':
                exit()
            else:
                print('Invalid choice. Please try again.')


view = NoteView()
view.run()
