import smtplib
import time
import json
import sqlite3
import schedule 
from datetime import datetime, timedelta

def send_email(subject, body, to_email):
    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        sender_email = 'youremailid'
        send_password = 'yourpassword'
        
        message = f'Subject: {subject}\n\n{body}'
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, send_password)
            server.sendmail(sender_email, to_email, message)
            
            print(f"Email sent to {to_email}'")
            
    except Exception as e:
        print(f"Something went wrong: {e}")
        
class TodoList:
    def __init__(self, db_name='todo_list.db'):
        self.connection = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.connection:
            self.connection.execute('''        
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    task TEXT NOT NULL,
                    completed BOOLEAN NOT NULL,
                    priority TEXT,
                    due_date TEXT
                )
            ''')

    def clear_tasks(self):
        with self.connection:
            self.connection.execute('DELETE FROM tasks')
        print("All tasks cleared.")

    def add_task(self, task, priority='medium', due_date=None):
        with self.connection:
            self.connection.execute('''        
                INSERT INTO tasks (task, completed, priority, due_date)
                VALUES (?, ?, ?, ?)
            ''', (task, False, priority, due_date))
        print(f"Task added successfully: {task}")

    def complete_task(self, task_id):
        with self.connection:
            self.connection.execute('''        
                UPDATE tasks SET completed = ? WHERE id = ?
            ''', (True, task_id))
        print(f"Task completed no. : {task_id}")

    def delete_task(self, task_id):
        with self.connection:
            self.connection.execute('''        
                DELETE FROM tasks WHERE id = ?
            ''', (task_id,))
        print(f"Task deleted no. : {task_id}")

    def edit_task(self, task_id, new_task=None, new_priority=None, new_due_date=None):
        with self.connection:
            if new_task:
                self.connection.execute('''        
                    UPDATE tasks SET task = ? WHERE id = ?
                ''', (new_task, task_id))
            if new_priority:
                self.connection.execute('''        
                    UPDATE tasks SET priority = ? WHERE id = ?
                ''', (new_priority, task_id))
            if new_due_date:
                self.connection.execute('''        
                    UPDATE tasks SET due_date = ? WHERE id = ?
                ''', (new_due_date, task_id))
        print(f"Task edited: {task_id}")

    def show_tasks(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()
        if not tasks:
            print("None of the tasks are available")
        else:
            for task in tasks:
                status = '✓' if task[2] else '✗'
                print(f"{task[0]}: [{status}] {task[1]} (priority: {task[3]}) Due: {task[4]}")

    def search_tasks(self, keyword):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM tasks WHERE task LIKE ?', ('%' + keyword + '%',))
        tasks = cursor.fetchall()
        if not tasks:
            print("No matching tasks found")
        else:
            for task in tasks:
                status = '✓' if task[2] else '✗'
                print(f"{task[0]}: [{status}] {task[1]} (priority: {task[3]}) Due: {task[4]}")            

def schedule_appointment(date_time, task):
    def job():
        print(f"Appointment reminder: {task}")
        
    schedule.every().day.at(date_time.strftime("%H:%M")).do(job)
    print(f"Appointment scheduled for {date_time.strftime('%Y-%m-%d %H:%M')}: {task}")

if __name__ == "__main__":
    
    todo_list = TodoList()
    
    # Clear existing tasks
    todo_list.clear_tasks()
    
    # Add new tasks
    todo_list.add_task('Complete the assignment', 'high', '2024-10-10')
    todo_list.add_task('Buy skin care', 'low')
    todo_list.add_task('Physics Numericals', 'high', '2024-10-10')
    todo_list.add_task('Send the ppt to HR', 'high', '2024-10-12')

    todo_list.show_tasks()
    
    todo_list.complete_task(2)
    todo_list.complete_task(4)  
    
    todo_list.show_tasks()
    
    todo_list.edit_task(1, new_task='submit the maths assignment too', new_priority='high')
    
    todo_list.show_tasks()
    
    todo_list.delete_task(2)  
    
    todo_list.search_tasks('assignment')

    appointment_time = datetime.strptime('2024-10-10 05:23', '%Y-%m-%d %H:%M')
    schedule_appointment(appointment_time, 'Dentist appointment')
