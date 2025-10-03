import json
import os
from datetime import datetime

class TodoList:
    def __init__(self, filename='todos.json'):
        self.filename = filename
        self.tasks = self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        return []
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        with open(self.filename, 'w') as f:
            json.dump(self.tasks, f, indent=2)
    
    def add_task(self, description, priority='medium'):
        """Add a new task"""
        task = {
            'id': len(self.tasks) + 1,
            'description': description,
            'priority': priority,
            'completed': False,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.tasks.append(task)
        self.save_tasks()
        print(f"✓ Task added: {description}")
    
    def view_tasks(self, show_completed=False):
        """Display all tasks"""
        if not self.tasks:
            print("No tasks found!")
            return
        
        print("\n" + "="*60)
        print("YOUR TO-DO LIST")
        print("="*60)
        
        for task in self.tasks:
            if not show_completed and task['completed']:
                continue
            
            status = "✓" if task['completed'] else "○"
            priority_symbol = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task['priority'], "⚪")
            
            print(f"{status} [{task['id']}] {priority_symbol} {task['description']}")
            print(f"   Priority: {task['priority']} | Created: {task['created_at']}")
            if task['completed']:
                print(f"   Completed: ✓")
            print()
    
    def complete_task(self, task_id):
        """Mark a task as completed"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = True
                self.save_tasks()
                print(f"✓ Task {task_id} marked as completed!")
                return
        print(f"Task {task_id} not found!")
    
    def delete_task(self, task_id):
        """Delete a task"""
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                deleted = self.tasks.pop(i)
                self.save_tasks()
                print(f"✓ Task deleted: {deleted['description']}")
                return
        print(f"Task {task_id} not found!")
    
    def edit_task(self, task_id, new_description):
        """Edit a task description"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['description'] = new_description
                self.save_tasks()
                print(f"✓ Task {task_id} updated!")
                return
        print(f"Task {task_id} not found!")
    
    def clear_completed(self):
        """Remove all completed tasks"""
        original_count = len(self.tasks)
        self.tasks = [task for task in self.tasks if not task['completed']]
        self.save_tasks()
        removed = original_count - len(self.tasks)
        print(f"✓ Removed {removed} completed task(s)")


def display_menu():
    """Display the main menu"""
    print("\n" + "="*60)
    print("TO-DO LIST MENU")
    print("="*60)
    print("1. Add task")
    print("2. View tasks")
    print("3. View all tasks (including completed)")
    print("4. Complete task")
    print("5. Edit task")
    print("6. Delete task")
    print("7. Clear completed tasks")
    print("8. Exit")
    print("="*60)


def main():
    todo = TodoList()
    
    print("\n🎯 Welcome to Your To-Do List Manager!")
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-8): ").strip()
        
        if choice == '1':
            description = input("Enter task description: ").strip()
            if description:
                priority = input("Enter priority (high/medium/low) [default: medium]: ").strip().lower()
                if priority not in ['high', 'medium', 'low']:
                    priority = 'medium'
                todo.add_task(description, priority)
            else:
                print("Task description cannot be empty!")
        
        elif choice == '2':
            todo.view_tasks(show_completed=False)
        
        elif choice == '3':
            todo.view_tasks(show_completed=True)
        
        elif choice == '4':
            try:
                task_id = int(input("Enter task ID to complete: "))
                todo.complete_task(task_id)
            except ValueError:
                print("Invalid task ID!")
        
        elif choice == '5':
            try:
                task_id = int(input("Enter task ID to edit: "))
                new_desc = input("Enter new description: ").strip()
                if new_desc:
                    todo.edit_task(task_id, new_desc)
                else:
                    print("Description cannot be empty!")
            except ValueError:
                print("Invalid task ID!")
        
        elif choice == '6':
            try:
                task_id = int(input("Enter task ID to delete: "))
                todo.delete_task(task_id)
            except ValueError:
                print("Invalid task ID!")
        
        elif choice == '7':
            confirm = input("Clear all completed tasks? (y/n): ").lower()
            if confirm == 'y':
                todo.clear_completed()
        
        elif choice == '8':
            print("\n👋 Thank you for using To-Do List Manager. Goodbye!")
            break
        
        else:
            print("Invalid choice! Please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()

