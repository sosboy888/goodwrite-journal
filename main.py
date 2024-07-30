import tkinter as tk
from tkinter import ttk
from datetime import datetime,date
import sqlite3

# Database setup
def setup_database():
    conn = sqlite3.connect('journal.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS entries (
                        date TEXT PRIMARY KEY,
                        entry TEXT
                      )''')
    conn.commit()
    conn.close()

# Function to insert bullet points
def insert_bullet():
    text_area.insert(tk.END, "• ")

# Function to display selected date's journal entry
def display_entry(event):
    selected_date = date_listbox.get(date_listbox.curselection())
    conn = sqlite3.connect('journal.db')
    cursor = conn.cursor()
    cursor.execute("SELECT entry FROM entries WHERE date = ?", (selected_date,))
    row = cursor.fetchone()
    text_area.delete("1.0", tk.END)
    if row:
        text_area.insert(tk.END, row[0])
    conn.close()

# Function to save the current journal entry
def save_entry():
    selected_date = date.today()
    current_entry = text_area.get("1.0", tk.END).strip()
    conn = sqlite3.connect('journal.db')
    cursor = conn.cursor()
    cursor.execute("REPLACE INTO entries (date, entry) VALUES (?, ?)", (selected_date, current_entry))
    conn.commit()
    conn.close()
    text_area.delete("1.0", tk.END)
    text_area.insert(tk.END, "Entry saved!")

# Function to load dates with entries from the database
def load_dates():
    conn = sqlite3.connect('journal.db')
    cursor = conn.cursor()
    cursor.execute("SELECT date FROM entries")
    dates = cursor.fetchall()
    for date in dates:
        date_listbox.insert(tk.END, date[0])
    conn.close()

# Function to start a new journal entry for today
def new_journal_entry():
    today = datetime.today().strftime('%Y-%m-%d')
    text_area.delete("1.0", tk.END)
    if today not in date_listbox.get(0, tk.END):
        date_listbox.insert(tk.END, today)
    date_listbox.selection_clear(0, tk.END)
    date_listbox.selection_set(tk.END)
    date_listbox.event_generate("<<ListboxSelect>>")

# Main application window
root = tk.Tk()
root.title("GoodWrite Journal")

# Configure the grid layout to make the GUI responsive
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)

# Sidebar for date selection
sidebar_frame = ttk.Frame(root)
sidebar_frame.grid(row=0, column=0, sticky="nsw", padx=10, pady=10)

# Listbox for dates
date_listbox = tk.Listbox(sidebar_frame, width=15)
date_listbox.pack(fill=tk.Y, expand=True)

# Bind selection event
date_listbox.bind("<<ListboxSelect>>", display_entry)

# Main area for journal entry
main_frame = ttk.Frame(root)
main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

# Configure the grid layout for main_frame
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(0, weight=1)

# Text area for journal
text_area = tk.Text(main_frame, wrap=tk.WORD, font=("Helvetica", 12))
text_area.grid(row=0, column=0, sticky="nsew")

# Scrollbar for text area
scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=text_area.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
text_area.config(yscrollcommand=scrollbar.set)

# Button frame for new journal and saving
button_frame = ttk.Frame(main_frame)
button_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")
button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=1)

# Button to start a new journal entry
new_journal_button = ttk.Button(button_frame, text="New Journal", command=new_journal_entry)
new_journal_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

# Button to save entry
save_button = ttk.Button(button_frame, text="Save", command=save_entry)
save_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

# Run the application
setup_database()
load_dates()
root.mainloop()