import csv
import uuid
from datetime import datetime
import json

'''print('Добро пожаловать в Персональный помощник!\n'
      'Выберите действие:\n'
      '1. Управление заметками\n'
      '2. Управление задачами\n'
      '3. Управление контактами\n'
      '4. Управление финансовыми записями\n'
      '5. Калькулятор\n'
      '6. Выход')'''

TIMESTAMP_FORMAT = '%d-%m-%Y %H:%M:%S'


class Note:
    def __init__(self, id, title, content, timestamp=None):
        self.id = id
        self.title = title
        self.content = content
        self.timestamp = timestamp if timestamp else datetime.now().strftime(TIMESTAMP_FORMAT)

    def __repr__(self):
        return f'Note(id: {self.id}, title: {self.title}, content: {self.content}, timestamp: {self.timestamp})'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'timestamp': self.timestamp
        }


class NoteManager:
    def __init__(self, notes_file='notes.json'):
        self.notes_file = notes_file
        self.load_notes()

    def load_notes(self):
        try:
            with open(self.notes_file, 'r') as file:
                try:
                    self.notes = [Note(**note_data) for note_data in json.load(file)]
                except json.JSONDecodeError:
                    print('Неверный формат файла notes.json')
                    self.notes = []
        except FileNotFoundError:
            print('Файл не существует')
            self.notes = []

    def save_note(self):
        with open(self.notes_file, 'w') as f:
            json.dump([note.to_dict() for note in self.notes], f, indent=4)

    def create_note(self):
        title = input('Введите заголовок заметки: ')
        if not title:
            return 'Заголовок не может быть пустым.'
        content = input('Введите содержимое заметки: ')
        new_id = len(self.notes) + 1 if self.notes else 1
        new_note = Note(new_id, title, content)
        self.notes.append(new_note)
        self.save_note()
        return 'Заметка создана.'

    def list_notes(self):
        if not self.notes:
            print('Список заметок пуст.')
            return
        for note in self.notes:
            print(f'ID: {note.id},\nЗаголовок: {note.title}, \nДата: {note.timestamp}\n ')

    def view_note(self):
        note_id = int(input("Введите id заметки: "))
        note = self.find_note(note_id)
        if note:
            print(f"Заголовок: {note.title}\nСодержимое: {note.content}\nДата: {note.timestamp}\n")
        else:
            print("Заметка не найдена.")

    def edit_note(self):
        note_id = int(input("Введите id заметки: "))
        note = self.find_note(note_id)
        if note:
            note.title = input(f'Новый заголовок ({note.title}):') or note.title
            note.content = input(f'Новое содержимое ({note.content}):') or note.content
            note.timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
            self.save_note()
            print("Заметка обновлена.")
        else:
            print("Заметка не найдена.")

    def delete_note(self):
        note_id = int(input("Введите id заметки: "))
        note = self.find_note(note_id)
        if note:
            self.notes.remove(note)
            self.save_note()
            print('Заметка удалена.')
        else:
            print("Заметка не найдена.")

    def find_note(self, note_id):
        for note in self.notes:
            if note.id == note_id:
                return note
        return None

    def import_from_csv(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.notes.append(Note(int(row['id']), row['title'], row['content'], row['timestamp']))
            self.save_note()
            print('Данные импортированы из CSV')
        except FileNotFoundError:
            print('Файл CSV не найден.')
        except Exception as e:
            print(f'Ошибка при импорте из CSV: {e}')

    def export_to_csv(self, filepath):
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file)
                writer.writerow(['id', 'title', 'content', 'timestamp'])
                for note in self.notes:
                    writer.writerow([note.id, note.title, note.content, note.timestamp])
            print('Данные экспортированы в CSV.')
        except Exception as e:
            print(f'Ошибка при экспорте в CSV: {e}')


manager = NoteManager()


def note_manager():
    while True:
        action = input("Выберите действие:\n"
                       "1. Создать заметку\n"
                       "2. Просмотреть список заметок\n"
                       "3. Просмотреть заметку\n"
                       "4. Редактировать заметку\n"
                       "5. Удалить заметку\n"
                       "6. Импорт из CSV\n"
                       "7. Экспорт в CSV\n"
                       "0. Выход\n")

        if action == '1':
            manager.create_note()
        elif action == '2':
            manager.list_notes()
        elif action == '3':
            manager.view_note()
        elif action == '4':
            manager.edit_note()
        elif action == '5':
            manager.delete_note()
        elif action == '6':
            filepath = input("Введите путь к CSV-файлу для импорта: ")
            manager.import_from_csv(filepath)
        elif action == '7':
            filepath = input("Введите путь к CSV-файлу для экспорта: ")
            manager.export_to_csv(filepath)
        elif action == '0':
            break
        else:
            print("Неверное действие.")


class Task:
    pass



class Calculator:

    def posterror(self, expression):
        try:
            print(eval(expression))
        except ValueError as e:
            raise ValueError(f"Ошибка: {e}. Пожалуйста, введите выражение в формате 'число оператор число'.") from None
        except ZeroDivisionError as e:
            raise ZeroDivisionError(f"Ошибка: {e}") from None
        except Exception as e:
            raise Exception(f"Произошла неизвестная ошибка: {e}") from None


calculator = Calculator()


def calculate():
    while True:
        try:
            expression = input("Введите арифметическое выражение (или 'exit' для выхода): ")
            if expression.lower() == 'exit':
                break
            result = calculator.posterror(expression)
            #print(f"Результат: {result}")
        except (ValueError, ZeroDivisionError, Exception) as e:
            print(e)

if __name__ == "__main__":
    calculate()