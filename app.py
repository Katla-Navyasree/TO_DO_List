import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import json, os
from datetime import datetime, date
from tkinter import font as tkfont
from tkcalendar import Calendar  # You'll need to install this: pip install tkcalendar

FILENAME = "tasks.json"

# ---------------- Data Handling ----------------
def load_tasks():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            tasks = json.load(f)
            # Convert due_date strings back to date objects if needed
            for t in tasks:
                if "due_date" in t and t["due_date"]:
                    try:
                        t["due_date"] = datetime.fromisoformat(t["due_date"]).date()
                    except:
                        t["due_date"] = None
                if "created_at" in t:
                    try:
                        t["created_at"] = datetime.fromisoformat(t["created_at"])
                    except:
                        t["created_at"] = datetime.now()
                if "priority" not in t:
                    t["priority"] = "medium"
                if "list" not in t:
                    t["list"] = "Tasks"
            return tasks
    return []

def save_tasks(tasks):
    # Convert dates to strings for JSON
    serializable_tasks = []
    for t in tasks:
        task_copy = t.copy()
        if "due_date" in task_copy and task_copy["due_date"]:
            task_copy["due_date"] = task_copy["due_date"].isoformat()
        if "created_at" in task_copy:
            task_copy["created_at"] = task_copy["created_at"].isoformat()
        serializable_tasks.append(task_copy)
    with open(FILENAME, "w") as f:
        json.dump(serializable_tasks, f, indent=2)

# ---------------- GUI Application ----------------
class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("800x700")
        
        # Set minimum window size
        self.root.minsize(700, 600)

        self.tasks = load_tasks()
        self.current_list = "Tasks"
        self.editing_task_id = None
        self.dark_mode = False
        
        # Create custom lists
        self.lists = ["Tasks", "Personal", "Work", "Shopping"]
        self.update_lists_from_tasks()
        
        # Configure styles
        self.setup_styles()
        
        # Create UI
        self.create_ui()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Light theme colors
        self.light_bg_color = "#fafafa"
        self.light_card_color = "#ffffff"
        self.light_primary_color = "#1a73e8"
        self.light_text_color = "#202124"
        self.light_secondary_text = "#5f6368"
        self.light_border_color = "#dadce0"
        
        # Dark theme colors
        self.dark_bg_color = "#202124"
        self.dark_card_color = "#303134"
        self.dark_primary_color = "#8ab4f8"
        self.dark_text_color = "#e8eaed"
        self.dark_secondary_text = "#9aa0a6"
        self.dark_border_color = "#5f6368"
        
        # Set initial theme
        self.apply_light_theme()

    def apply_light_theme(self):
        self.bg_color = self.light_bg_color
        self.card_color = self.light_card_color
        self.primary_color = self.light_primary_color
        self.text_color = self.light_text_color
        self.secondary_text = self.light_secondary_text
        self.border_color = self.light_border_color
        self.dark_mode = False
        
        # Configure styles
        self.style.configure("TButton", font=("Segoe UI", 10), padding=8)
        self.style.configure("Primary.TButton", background=self.primary_color, foreground="white")
        self.style.configure("TLabel", font=("Segoe UI", 11), background=self.bg_color)
        self.style.configure("TEntry", font=("Segoe UI", 11))
        self.style.configure("TCombobox", font=("Segoe UI", 11))

    def apply_dark_theme(self):
        self.bg_color = self.dark_bg_color
        self.card_color = self.dark_card_color
        self.primary_color = self.dark_primary_color
        self.text_color = self.dark_text_color
        self.secondary_text = self.dark_secondary_text
        self.border_color = self.dark_border_color
        self.dark_mode = True
        
        # Configure styles
        self.style.configure("TButton", font=("Segoe UI", 10), padding=8)
        self.style.configure("Primary.TButton", background=self.primary_color, foreground="black")
        self.style.configure("TLabel", font=("Segoe UI", 11), background=self.bg_color)
        self.style.configure("TEntry", font=("Segoe UI", 11))
        self.style.configure("TCombobox", font=("Segoe UI", 11))

    def toggle_theme(self):
        if self.dark_mode:
            self.apply_light_theme()
        else:
            self.apply_dark_theme()
        self.refresh_ui()

    def refresh_ui(self):
        # Recreate the entire UI with new theme
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_ui()

    def create_ui(self):
        # Configure root background
        self.root.configure(bg=self.bg_color)
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)
        
        # Header
        header_frame = tk.Frame(main_container, bg=self.bg_color)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # App title
        title_font = tkfont.Font(family="Segoe UI", size=24, weight="normal")
        tk.Label(header_frame, text="To-Do List", font=title_font, 
                bg=self.bg_color, fg=self.text_color).pack(side=tk.LEFT)
        
        # Theme toggle button at top right
        theme_btn = ttk.Button(header_frame, text="🌙" if not self.dark_mode else "☀️", 
                              command=self.toggle_theme, width=3)
        theme_btn.pack(side=tk.RIGHT)
        
        # List selector
        list_frame = tk.Frame(main_container, bg=self.bg_color)
        list_frame.pack(fill=tk.X, pady=(0, 16))
        
        tk.Label(list_frame, text="List:", bg=self.bg_color, fg=self.secondary_text).pack(side=tk.LEFT)
        
        self.list_combobox = ttk.Combobox(list_frame, values=self.lists, state="readonly", width=15)
        self.list_combobox.set(self.current_list)
        self.list_combobox.pack(side=tk.LEFT, padx=(8, 0))
        self.list_combobox.bind("<<ComboboxSelected>>", self.on_list_changed)
        
        # Add new list button
        ttk.Button(list_frame, text="+ New List", command=self.add_new_list).pack(side=tk.LEFT, padx=(16, 0))
        
        # Task input card
        self.create_task_input_card(main_container)
        
        # Tasks frame
        self.create_tasks_display(main_container)

    def create_task_input_card(self, parent):
        self.input_card = tk.Frame(parent, bg=self.card_color, relief="flat", bd=1, 
                                  highlightbackground=self.border_color, highlightthickness=1)
        self.input_card.pack(fill=tk.X, pady=(0, 16))
        
        # Task entry
        self.task_entry = tk.Text(self.input_card, height=3, width=50, font=("Segoe UI", 11),
                                 bg=self.card_color, fg=self.text_color, relief="flat", 
                                 highlightthickness=0, wrap=tk.WORD)
        self.task_entry.pack(fill=tk.X, padx=16, pady=16)
        self.task_entry.insert("1.0", "Add a task...")
        self.task_entry.config(fg=self.secondary_text)
        self.task_entry.bind("<FocusIn>", self.on_task_entry_focus_in)
        self.task_entry.bind("<FocusOut>", self.on_task_entry_focus_out)
        
        # Options frame (initially hidden)
        self.options_frame = tk.Frame(self.input_card, bg=self.card_color)
        
        # Due date and priority
        options_top = tk.Frame(self.options_frame, bg=self.card_color)
        options_top.pack(fill=tk.X, padx=16, pady=(0, 8))
        
        tk.Label(options_top, text="Due date:", bg=self.card_color, fg=self.secondary_text).pack(side=tk.LEFT)
        
        # Due date frame with entry and calendar button
        due_date_frame = tk.Frame(options_top, bg=self.card_color)
        due_date_frame.pack(side=tk.LEFT, padx=(8, 16))
        
        self.due_date_entry = tk.Entry(due_date_frame, width=12, font=("Segoe UI", 10), 
                                      bg=self.card_color, fg=self.text_color, relief="solid", bd=1)
        self.due_date_entry.pack(side=tk.LEFT)
        
        # Calendar button
        calendar_btn = tk.Button(due_date_frame, text="📅", font=("Segoe UI", 12), relief="flat",
                               bg=self.card_color, fg=self.secondary_text, cursor="hand2",
                               command=self.show_calendar)
        calendar_btn.pack(side=tk.LEFT, padx=(4, 0))
        
        tk.Label(options_top, text="Priority:", bg=self.card_color, fg=self.secondary_text).pack(side=tk.LEFT)
        self.priority_combobox = ttk.Combobox(options_top, values=["low", "medium", "high"], 
                                             state="readonly", width=8)
        self.priority_combobox.set("medium")
        self.priority_combobox.pack(side=tk.LEFT, padx=8)
        
        # Buttons
        options_bottom = tk.Frame(self.options_frame, bg=self.card_color)
        options_bottom.pack(fill=tk.X, padx=16, pady=(0, 16))
        
        ttk.Button(options_bottom, text="Save", command=self.save_task).pack(side=tk.RIGHT, padx=(8, 0))
        ttk.Button(options_bottom, text="Cancel", command=self.cancel_edit).pack(side=tk.RIGHT)

    def show_calendar(self):
        """Show calendar popup for date selection"""
        # Create a top level window
        calendar_window = tk.Toplevel(self.root)
        calendar_window.title("Select Due Date")
        calendar_window.geometry("300x300")
        calendar_window.transient(self.root)
        calendar_window.grab_set()
        
        # Set theme-appropriate colors for calendar
        if self.dark_mode:
            bg_color = self.dark_card_color
            fg_color = self.dark_text_color
            select_bg = self.dark_primary_color
        else:
            bg_color = self.light_card_color
            fg_color = self.light_text_color
            select_bg = self.light_primary_color
        
        # Create calendar widget
        cal = Calendar(calendar_window, 
                      selectmode='day',
                      year=datetime.now().year,
                      month=datetime.now().month,
                      day=datetime.now().day,
                      background=bg_color,
                      foreground=fg_color,
                      selectbackground=select_bg,
                      normalbackground=bg_color,
                      weekendbackground=bg_color,
                      headersbackground=bg_color,
                      headersforeground=fg_color,
                      bordercolor=self.border_color,
                      selectforeground=bg_color)  # Text color on selected date
        
        cal.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Function to set the selected date
        def set_date():
            selected_date = cal.selection_get()
            # selection_get returns a date object, format to YYYY-MM-DD
            formatted_date = selected_date.strftime("%Y-%m-%d")
            self.due_date_entry.delete(0, tk.END)
            self.due_date_entry.insert(0, formatted_date)
            calendar_window.destroy()
        
        # Buttons frame
        btn_frame = tk.Frame(calendar_window, bg=bg_color)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Select", command=set_date).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=calendar_window.destroy).pack(side=tk.LEFT, padx=5)
        
        # Center the calendar window
        calendar_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (calendar_window.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (calendar_window.winfo_height() // 2)
        calendar_window.geometry(f"+{x}+{y}")

    def create_tasks_display(self, parent):
        # Tasks container
        tasks_container = tk.Frame(parent, bg=self.bg_color)
        tasks_container.pack(fill=tk.BOTH, expand=True)
        
        # Create a canvas with scrollbar for tasks
        self.canvas = tk.Canvas(tasks_container, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(tasks_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.bg_color)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        
        # Load tasks
        self.load_tasks_cards()

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def on_task_entry_focus_in(self, event):
        if self.task_entry.get("1.0", "end-1c") == "Add a task...":
            self.task_entry.delete("1.0", "end")
            self.task_entry.config(fg=self.text_color)
        
        # Show options frame
        self.options_frame.pack(fill=tk.X)
        self.input_card.pack(fill=tk.X, pady=(0, 16))  # Refresh layout

    def on_task_entry_focus_out(self, event):
        if not self.task_entry.get("1.0", "end-1c").strip():
            self.task_entry.insert("1.0", "Add a task...")
            self.task_entry.config(fg=self.secondary_text)
            
            # Hide options frame if not editing
            if self.editing_task_id is None:
                self.options_frame.pack_forget()
                self.input_card.pack(fill=tk.X, pady=(0, 16))  # Refresh layout

    def on_list_changed(self, event):
        self.current_list = self.list_combobox.get()
        self.load_tasks_cards()

    def add_new_list(self):
        new_list = simpledialog.askstring("New List", "Enter list name:")
        if new_list and new_list not in self.lists:
            self.lists.append(new_list)
            self.list_combobox['values'] = self.lists
            self.list_combobox.set(new_list)
            self.current_list = new_list
            self.load_tasks_cards()

    def update_lists_from_tasks(self):
        for task in self.tasks:
            if "list" in task and task["list"] not in self.lists:
                self.lists.append(task["list"])

    def load_tasks_cards(self):
        # Clear existing tasks
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Filter tasks for current list
        filtered_tasks = [t for t in self.tasks if t.get("list", "Tasks") == self.current_list]
        
        if not filtered_tasks:
            # Show empty state
            empty_label = tk.Label(self.scrollable_frame, text="No tasks in this list", 
                                  font=("Segoe UI", 14), bg=self.bg_color, fg=self.secondary_text)
            empty_label.pack(pady=40)
            return
        
        # Create task cards
        for i, task in enumerate(filtered_tasks):
            self.create_task_card(task, i)

    def create_task_card(self, task, index):
        card = tk.Frame(self.scrollable_frame, bg=self.card_color, relief="flat", bd=1,
                       highlightbackground=self.border_color, highlightthickness=1)
        card.pack(fill=tk.X, pady=(0, 8))
        
        # Main content frame
        content_frame = tk.Frame(card, bg=self.card_color)
        content_frame.pack(fill=tk.X, padx=16, pady=12)
        
        # Checkbox and task text
        top_frame = tk.Frame(content_frame, bg=self.card_color)
        top_frame.pack(fill=tk.X)
        
        # Checkbox
        check_var = tk.BooleanVar(value=task["completed"])
        checkbox = tk.Checkbutton(top_frame, variable=check_var, bg=self.card_color,
                                command=lambda t=task: self.toggle_task_completion(t))
        checkbox.pack(side=tk.LEFT)
        
        # Task text
        task_text = tk.Label(top_frame, text=task["task"], font=("Segoe UI", 11), 
                           bg=self.card_color, fg=self.text_color, anchor="w", justify=tk.LEFT)
        task_text.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 0))
        
        # Strike through if completed
        if task["completed"]:
            task_text.config(fg=self.secondary_text, font=("Segoe UI", 11, "overstrike"))
        
        # Edit and Delete buttons
        buttons_frame = tk.Frame(top_frame, bg=self.card_color)
        buttons_frame.pack(side=tk.RIGHT, padx=(8, 0))
        
        edit_btn = tk.Button(buttons_frame, text="✏️", font=("Segoe UI", 25), relief="flat",
                           bg=self.card_color, fg=self.secondary_text,
                           command=lambda t=task: self.edit_task(t))
        edit_btn.pack(side=tk.LEFT, padx=(0, 4))
        
        delete_btn = tk.Button(buttons_frame, text="🗑️", font=("Segoe UI", 25), relief="flat",
                             bg=self.card_color, fg=self.secondary_text,
                             command=lambda t=task: self.delete_task(t))
        delete_btn.pack(side=tk.LEFT)
        
        # Task details (due date, priority)
        if task.get("due_date") or task.get("priority") != "medium":
            details_frame = tk.Frame(content_frame, bg=self.card_color)
            details_frame.pack(fill=tk.X, pady=(8, 0))
            
            # Due date
            if task.get("due_date"):
                due_date = task["due_date"]
                due_color = "#ea4335" if due_date < date.today() and not task["completed"] else self.secondary_text
                due_label = tk.Label(details_frame, text=f"Due: {due_date}", font=("Segoe UI", 9),
                                   bg=self.card_color, fg=due_color)
                due_label.pack(side=tk.LEFT, padx=(24, 16))
            
            # Priority
            if task.get("priority") != "medium":
                priority_color = {
                    "low": "#0b8043",
                    "medium": "#8800ff", 
                    "high": "#e67c73"
                }.get(task["priority"], self.secondary_text)
                
                priority_label = tk.Label(details_frame, text=f"Priority: {task['priority']}", 
                                        font=("Segoe UI", 9), bg=self.card_color, fg=priority_color)
                priority_label.pack(side=tk.LEFT)

    def toggle_task_completion(self, task):
        task["completed"] = not task["completed"]
        save_tasks(self.tasks)
        self.load_tasks_cards()

    def edit_task(self, task):
        self.editing_task_id = id(task)
        self.task_entry.delete("1.0", "end")
        self.task_entry.insert("1.0", task["task"])
        self.task_entry.config(fg=self.text_color)
        
        # Set due date
        if task.get("due_date"):
            self.due_date_entry.delete(0, "end")
            self.due_date_entry.insert(0, task["due_date"].isoformat())
        else:
            self.due_date_entry.delete(0, "end")
        
        # Set priority
        self.priority_combobox.set(task.get("priority", "medium"))
        
        # Show options
        self.options_frame.pack(fill=tk.X)
        self.input_card.pack(fill=tk.X, pady=(0, 16))

    def delete_task(self, task):
        result = messagebox.askyesno("Delete Task", f"Are you sure you want to delete '{task['task']}'?")
        if result:
            # Remove task from tasks list
            self.tasks = [t for t in self.tasks if id(t) != id(task)]
            save_tasks(self.tasks)
            self.load_tasks_cards()

    def save_task(self):
        task_text = self.task_entry.get("1.0", "end-1c").strip()
        due_date_str = self.due_date_entry.get().strip()
        priority = self.priority_combobox.get()
        
        if not task_text:
            messagebox.showwarning("Warning", "Task cannot be empty!")
            return
        
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD.")
                return
        
        if self.editing_task_id:
            # Update existing task
            for task in self.tasks:
                if id(task) == self.editing_task_id:
                    task["task"] = task_text
                    task["due_date"] = due_date
                    task["priority"] = priority
                    break
            self.editing_task_id = None
        else:
            # Add new task
            self.tasks.append({
                "task": task_text,
                "completed": False,
                "due_date": due_date,
                "created_at": datetime.now(),
                "priority": priority,
                "list": self.current_list
            })
        
        save_tasks(self.tasks)
        self.cancel_edit()
        self.load_tasks_cards()

    def cancel_edit(self):
        self.editing_task_id = None
        self.task_entry.delete("1.0", "end")
        self.task_entry.insert("1.0", "Add a task...")
        self.task_entry.config(fg=self.secondary_text)
        self.due_date_entry.delete(0, "end")
        self.priority_combobox.set("medium")
        self.options_frame.pack_forget()
        self.input_card.pack(fill=tk.X, pady=(0, 16))

# ---------------- Run App ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()