# 📚 Student Habit & Deadline Tracker

A simple desktop application built with **Python, Tkinter, and SQLite** to help students manage their daily habits and academic deadlines in one place.

## ✨ Features

### 📈 Habit Tracker
- Add new habits
- Set daily/weekly targets
- Track completed progress
- Update existing habits
- Delete habits
- Automatically shows Completed/Pending status

### 📅 Deadline Manager
- Add assignment or project deadlines
- Categorize deadlines
- Mark tasks as completed
- Update deadline details
- Delete deadlines

## 🛠️ Technologies Used

- Python
- Tkinter (GUI)
- SQLite3 (Database)
- ttk Widgets

## 📂 Project Structure

```
Python Student Tracker/
│
├── Python_cp_final_draft.py   # Main application
├── student.db                 # SQLite database
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.x installed

### Run the Project

```bash
python Python_cp_final_draft.py
```

The application will automatically create the required database tables if they do not already exist.

## 📸 Main Modules

### Habit Tracker
- Create habits
- Set target values
- Track completed progress
- View completion status

### Deadline Tracker
- Store important deadlines
- Select category
- Mark deadlines as completed
- Update/Delete deadlines

## 🗄️ Database

The project uses SQLite with two tables:

### habits
- id
- name
- target
- done

### deadlines
- id
- title
- category
- ddate
- status

## 🎯 Future Improvements

- Login system
- Charts and analytics
- Dark/Light mode
- Notifications and reminders
- Calendar integration
- Export data to Excel/PDF

## 👨‍💻 Author

Developed as a Python desktop application project for students using Tkinter and SQLite.

## 📄 License

This project is intended for educational purposes.
