import csv
import os
from datetime import datetime
import json

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


DATE_FORMAT = '%d-%m-%Y'


class Task:
    def __init__(self, id, title, description="", done=False, priority="Средний", due_date=None):
        self.id = id
        self.title = title
        self.description = description
        self.done = done
        self.priority = priority
        self.due_date = due_date

    def __repr__(self):
        return f"Task(id={self.id}, title='{self.title}', done={self.done}, priority='{self.priority}', due_date='{self.due_date}')"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "done": self.done,
            "priority": self.priority,
            "due_date": self.due_date
        }


class TaskManager:
    def __init__(self, tasks_file='tasks.json'):
        self.tasks_file = tasks_file
        self.load_task()

    def load_task(self):
        try:
            with open(self.tasks_file, 'r') as file:
                try:
                    self.tasks = [Task(**task_data) for task_data in json.load(file)]
                except json.JSONDecodeError:
                    print('Неверный формат файла tasks.json')
                    self.tasks = []
        except FileNotFoundError:
            print('Файл не существует')
            self.tasks = []

    def save_tasks(self):
        with open(self.tasks_file, 'w', encoding='utf-8') as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)

    def add_task(self):
        title = input("Введите название задачи: ")
        if not title:
            print("Название задачи не может быть пустым.")
            return
        description = input("Введите описание задачи (можно оставить пустым): ")
        priority = input("Установите приоритет ('Высокий', 'Средний', 'Низкий'): ") or "Средний"
        due_date_str = input("Введите срок выполнения задачи (ДД-ММ-ГГГГ, можно оставить пустым): ")
        due_date = datetime.strptime(due_date_str, DATE_FORMAT).date() if due_date_str else None

        new_id = len(self.tasks) + 1 if self.tasks else 1
        new_task = Task(new_id, title, description, priority=priority, due_date=due_date)
        self.tasks.append(new_task)
        self.save_tasks()
        print("Задача добавлена.")

    def list_tasks(self, filter_status=None, filter_priority=None, filter_due_date=None):
        filtered_tasks = self.filter_tasks(filter_status, filter_priority, filter_due_date)

        if not filtered_tasks:
            print("Список задач пуст.")
            return
        for task in filtered_tasks:
            status = "Выполнено" if task.done else "Не выполнено"
            print(
                f"ID: {task.id}, Название: {task.title}, Статус: {status}, Приоритет: {task.priority}, Срок: {task.due_date}")

    def filter_tasks(self, status=None, priority=None, due_date=None):
        filtered_tasks = self.tasks
        if status:
            filtered_tasks = [task for task in filtered_tasks if
                              (task.done and status == 'Выполнено') or (not task.done and status == 'Не выполнено')]
        if priority:
            filtered_tasks = [task for task in filtered_tasks if task.priority == priority]
        if due_date:
            try:
                due_date_obj = datetime.strptime(due_date, DATE_FORMAT).date()
                filtered_tasks = [task for task in filtered_tasks if task.due_date == due_date_obj]
            except ValueError:
                print("Неверный формат даты.")
                return []
        return filtered_tasks

    def mark_as_done(self):
        task_id = int(input("Введите ID задачи для отметки как выполненной: "))
        task = self.find_task(task_id)
        if task:
            task.done = True
            self.save_tasks()
            print("Задача отмечена как выполненная.")
        else:
            print("Задача не найдена.")

    def edit_task(self):
        """Редактирует существующую задачу."""
        task_id = int(input("Введите ID задачи для редактирования: "))
        task = self.find_task(task_id)
        if task:
            task.title = input(f"Новое название ({task.title}): ") or task.title
            task.description = input(f"Новое описание ({task.description}): ") or task.description
            task.priority = input(f"Новый приоритет ({task.priority}): ") or task.priority
            due_date_str = input(f"Новый срок (ДД-ММ-ГГГГ, оставьте пустым для сохранения текущего срока): ")
            task.due_date = due_date_str if due_date_str else task.due_date
            self.save_tasks()
            print("Задача обновлена.")
        else:
            print("Задача не найдена.")

    def delete_task(self):
        task_id = int(input("Введите ID задачи для удаления: "))
        task = self.find_task(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            print("Задача удалена.")
        else:
            print("Задача не найдена.")

    def find_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def import_from_csv(self, filepath):
        import csv
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    new_task = Task(int(row['id']), row['title'], row['description'], row['done'] == 'True',
                                    row['priority'], row['due_date'])
                    self.tasks.append(new_task)
            self.save_tasks()
            print("Данные импортированы из CSV.")
        except FileNotFoundError:
            print(f"Ошибка: файл {filepath} не найден.")
        except Exception as e:
            print(f"Ошибка при импорте из CSV: {e}")

    def export_to_csv(self, filepath):
        import csv
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["id", "title", "description", "done", "priority", "due_date"])
                for task in self.tasks:
                    writer.writerow([task.id, task.title, task.description, task.done, task.priority, task.due_date])
            print("Данные экспортированы в CSV.")
        except Exception as e:
            print(f"Ошибка при экспорте в CSV: {e}")


task = TaskManager()


def task_manager():
    while True:
        choice = int(input("Выберите действие:\n"
                           "1. Добавить задачу\n"
                           "2. Посмотреть список задач\n"
                           "3. Отметить задачу как выполненную\n"
                           "4. Редактировать задачу\n"
                           "5. Удалить задачу\n"
                           "6. Импорт из CSV\n"
                           "7. Экспорт в CSV\n"
                           "0. Выход\n"))
        if choice == 1:
            task.add_task()
        elif choice == 2:
            filter_status = input("Фильтровать по статусу ('Выполнено', 'Не выполнено', 'Все'): ") or None
            filter_priority = input("Фильтровать по приоритету ('Высокий', 'Средний', 'Низкий', 'Все'): ") or None
            filter_due_date = input("Фильтровать по сроку (ДД-ММ-ГГГГ, 'Все'): ") or None
            task.list_tasks(filter_status, filter_priority, filter_due_date)
        elif choice == 3:
            task.mark_as_done()
        elif choice == 4:
            task.edit_task()
        elif choice == 5:
            task.delete_task()
        elif choice == 6:
            filepath = input("Введите путь к CSV-файлу для импорта: ")
            task.import_from_csv(filepath)
        elif choice == 7:
            filepath = input("Введите путь к CSV-файлу для экспорта: ")
            task.export_to_csv(filepath)
        elif choice == 0:
            break
        else:
            print("Неверное действие.")


class Contact:
    def __init__(self, id, name, phone=None, email=None):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email

    def __repr__(self):
        return f"Contact(id={self.id}, name='{self.name}', phone='{self.phone}', email='{self.email}')"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email
        }


class ContactManager:
    def __init__(self, contacts_file='contacts.json'):
        self.contacts_file = contacts_file
        self.load_task()

    def load_task(self):
        try:
            with open(self.contacts_file, 'r') as file:
                try:
                    self.contacts = [Contact(**contact_data) for contact_data in json.load(file)]
                except json.JSONDecodeError:
                    print('Неверный формат файла tasks.json')
                    self.contacts = []
        except FileNotFoundError:
            print('Файл не существует')
            self.contacts = []

    def add_contact(self):
        name = input('Введите имя контакта: ')
        if not name:
            return 'Имя не может быть пустым.'
        phone = input('Введите номер телефона: ')
        email = input("Введите email контакта:")
        new_id = len(self.contacts) + 1 if self.contacts else 1
        new_contact = Contact(new_id, name, phone, email)
        self.contacts.append(new_contact)
        self.save_contact()
        return 'Контакт создан.'

    def save_contact(self):
        with open(self.contacts_file, 'w', encoding='utf-8') as file:
            json.dump([contact.to_dict() for contact in self.contacts], file, indent=4)

    def edit_contact(self):
        contact_id = (input("Введите имя или номер контакта: "))
        contact = self.find_contact(contact_id)
        if contact:
            contact.name = input(f'Новое имя ({contact.name}):') or contact.name
            contact.phone = input(f'Новый номер телефона ({contact.phone}):') or contact.phone
            contact.email = input(f'Новый email ({contact.email}):') or contact.email
            self.save_contact()
            print("Контакт обновлен.")
        else:
            print("Контакт не найден.")

    def delete_contact(self):
        contact_id = (input("Введите имя или номер контакта: "))
        contact = self.find_contact(contact_id)
        if contact:
            self.contacts.remove(contact)
            self.save_contact()
            print('Контакт удален.')
        else:
            print("Контакт не найден.")

    def find_contact(self, contact_name):
        for сontact in self.contacts:
            if сontact.name == contact_name or сontact.phone == contact_name:
                return contact
        return None

    def find_and_show_contact(self):
        contact_id = (input("Введите имя или номер контакта: "))
        сontact = self.find_contact(contact_id)
        if сontact:
            print(f"Имя: {сontact.name}\nНомер: {contact.phone}\nemail: {contact.email}\n")
        else:
            print("Контакт не найден.")

    def import_from_csv(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.contacts.append(Contact(int(row['id']), row['name'], row['phone'], row['email']))
            self.save_contact()
            print('Данные импортированы из CSV')
        except FileNotFoundError:
            print('Файл CSV не найден.')
        except Exception as e:
            print(f'Ошибка при импорте из CSV: {e}')

    def export_to_csv(self, filepath):
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file)
                writer.writerow(['id', 'name', 'phone', 'email'])
                for contact in self.contacts:
                    writer.writerow([contact.id, contact.name, contact.phone, contact.email])
            print('Данные экспортированы в CSV.')
        except Exception as e:
            print(f'Ошибка при экспорте в CSV: {e}')


contact = ContactManager()


def contact_manager():
    while True:
        action = int(input("Выберите действие:\n"
                           "1. Создать контакт\n"
                           "2. Редактировать контакт\n"
                           "3. Удалить контакт\n"
                           "4. Импорт из CSV\n"
                           "5. Экспорт в CSV\n"
                           '6. Поиск контакта по имени или номеру телефона\n'
                           "0. Выход\n"))

        if action == 1:
            contact.add_contact()
        elif action == 2:
            contact.edit_contact()
        elif action == 3:
            contact.delete_contact()
        elif action == 4:
            filepath = input("Введите путь к CSV-файлу для импорта: ")
            contact.import_from_csv(filepath)
        elif action == 5:
            filepath = input("Введите путь к CSV-файлу для экспорта: ")
            contact.export_to_csv(filepath)
        elif action == 6:
            #name = input('Введите имя или номер телефона контакта:\n')
            contact.find_and_show_contact()
        elif action == 0:
            break
        else:
            print("Неверное действие.")


DATE_FORMAT = '%d-%m-%Y'


class FinanceRecord:
    def __init__(self, id, amount, category, date, description=""):
        self.id = id
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    def __repr__(self):
        return f"FinanceRecord(id={self.id}, amount={self.amount}, category='{self.category}', date='{self.date}', description='{self.description}')"

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "description": self.description
        }


class FinanceManager:
    def __init__(self, finance_file='finance.json'):
        self.finance_file = finance_file
        self.load_records()

    def load_records(self):
        try:
            with open(self.finance_file, 'r') as file:
                try:
                    self.records = [FinanceRecord(**finance_data) for finance_data in json.load(file)]
                except json.JSONDecodeError:
                    print('Неверный формат файла finance.json')
                self.records = []
        except FileNotFoundError:
            print('Файл не существует')
        self.records = []

    def save_records(self):
        with open(self.finance_file, 'w') as f:
            json.dump([record.to_dict() for record in self.records], f, indent=4)

    def add_record(self):
        amount = float(input("Введите сумму операции (положительное для дохода, отрицательное для расхода): "))
        category = input("Введите категорию операции: ")
        date_str = input("Введите дату операции (ДД-ММ-ГГГГ): ")
        description = input("Введите описание операции (необязательно): ")
        new_id = len(self.records) + 1
        try:
            record = FinanceRecord(new_id, amount, category, date_str, description)
            self.records.append(record)
            self.save_records()
            print("Запись добавлена.")
        except ValueError as e:
            print(f"Ошибка: {e}")

    def list_records(self, filter_date=None, filter_category=None):
        filtered_records = self.records

        if filter_date:
            try:
                filter_date_obj = datetime.strptime(filter_date, DATE_FORMAT).date()
                filtered_records = [record for record in filtered_records if record.date == filter_date_obj]
            except ValueError:
                print("Неверный формат даты.")
                return

        if filter_category:
            filtered_records = [record for record in filtered_records if record.category == filter_category]

        if not filtered_records:
            print("Список записей пуст.")
            return
        for record in filtered_records:
            print(
                f"ID: {record.id}, Сумма: {record.amount}, Категория: {record.category}, Дата: {record.date}, Описание: {record.description}")

    def generate_report(self, start_date_str, end_date_str):
        try:
            start_date = datetime.strptime(start_date_str, DATE_FORMAT).date()
            end_date = datetime.strptime(end_date_str, DATE_FORMAT).date()
        except ValueError:
            print("Неверный формат даты. Используйте ДД-ММ-ГГГГ.")
            return

        if start_date > end_date:
            print("Дата начала не может быть позже даты окончания.")
            return

        report_data = {'income': 0, 'expenses': 0, 'income_items': {}, 'expense_items': {}}

        for record in self.records:
            try:
                record_date = datetime.strptime(record.date, DATE_FORMAT).date()
            except ValueError:
                print(f"Ошибка: Неверный формат даты в записи с ID {record.id}.")
                continue

            if start_date <= record_date <= end_date:
                if record.amount >= 0:
                    report_data['income'] += record.amount
                    report_data['income_items'][record.category] = report_data['income_items'].get(record.category,
                                                                                                   0) + record.amount
                else:
                    report_data['expenses'] += abs(record.amount)
                    report_data['expense_items'][record.category] = report_data['expense_items'].get(record.category,
                                                                                                     0) + abs(
                        record.amount)

        print("\nОтчет о финансовой активности:")
        print(f"Период: {start_date_str} - {end_date_str}")
        print("\nДоходы:")
        if report_data['income']:
            for category, amount in report_data['income_items'].items():
                print(f"- {category}: {amount}")
            print(f"Итого доходов: {report_data['income']}")
        else:
            print("Доходы отсутствуют.")

        print("\nРасходы:")
        if report_data['expenses']:
            for category, amount in report_data['expense_items'].items():
                print(f"- {category}: {amount}")
            print(f"Итого расходов: {report_data['expenses']}")
        else:
            print("Расходы отсутствуют.")

        print(f"\nБаланс: {report_data['income'] - report_data['expenses']}")

    def import_from_csv(self, filepath):
        import csv
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    new_record = FinanceRecord(int(row['id']), float(row['amount']), row['category'], row['date'],
                                               row['description'])
                    self.records.append(new_record)
            self.save_records()
            print("Данные импортированы из CSV.")
        except FileNotFoundError:
            print(f"Ошибка: файл {filepath} не найден.")
        except Exception as e:
            print(f"Ошибка при импорте из CSV: {e}")

    def export_to_csv(self, filepath):
        import csv
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["id", "amount", "category", "date", "description"])
                for record in self.records:
                    writer.writerow([record.id, record.amount, record.category, record.date, record.description])
            print("Данные экспортированы в CSV.")
        except Exception as e:
            print(f"Ошибка при экспорте в CSV: {e}")


finance = FinanceManager()


def finance_manager():
    while True:
        action = int(input("Выберите действие:\n"
                           "1. Добавить запись\n"
                           "2. Просмотреть список записей\n"
                           "3. Сгенерировать отчет\n"
                           "4. Импорт из CSV\n"
                           "5. Экспорт в CSV\n"
                           "0. Выход\n"))

        if action == 1:
            finance.add_record()
        elif action == 2:
            filter_date = input("Фильтровать по дате (ДД-ММ-ГГГГ, оставить пустым для пропуска): ")
            filter_category = input("Фильтровать по категории (оставить пустым для пропуска): ")
            finance.list_records(filter_date, filter_category)
        elif action == 3:
            start_date = input("Введите начальную дату отчета (ДД-ММ-ГГГГ): ")
            end_date = input("Введите конечную дату отчета (ДД-ММ-ГГГГ): ")
            manager.generate_report(start_date, end_date)
        elif action == 4:
            filepath = input("Введите путь к CSV-файлу для импорта: ")
            finance.import_from_csv(filepath)
        elif action == 5:
            filepath = input("Введите путь к CSV-файлу для экспорта: ")
            finance.export_to_csv(filepath)
        elif action == 0:
            break
        else:
            print("Неверное действие.")


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
        except (ValueError, ZeroDivisionError, Exception) as e:
            print(e)


if __name__ == "__main__":
    while True:
        action = int(input('Добро пожаловать в Персональный помощник!\n'
                           'Выберите действие:\n'
                           '1. Управление заметками\n'
                           '2. Управление задачами\n'
                           '3. Управление контактами\n'
                           '4. Управление финансовыми записями\n'
                           '5. Калькулятор\n'
                           '0. Выход\n'))

        if action == 1:
            note_manager()
        elif action == 2:
            task_manager()
        elif action == 3:
            contact_manager()
        elif action == 4:
            finance_manager()
        elif action == 5:
            calculate()
        elif action == 0:
            break
        else:
            print("Неверное действие.")
