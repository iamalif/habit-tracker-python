# habit-tracker-python

A Python command-line application to track and log daily habits, 
built using Object-Oriented Programming (OOP) principles.

## About
This program allows users to create habits, log them as completed 
or not on any given date, and view summaries by day or custom date 
range. Data is persisted across sessions using two CSV files. Built 
as a personal OOP and CSV practice project.

## Features
- Two classes: Habit and HabitLog with private attributes
- Auto-incrementing unique IDs for both habits and logs
- Getter and setter methods for all attributes
- Add a new habit with name and description
- Delete a habit and all its associated logs
- List all habits
- Log a habit as completed or not for a given date
- Show all logs for a specific habit
- Show daily summary — all habits completed on a given date
- Show custom summary — all habits completed within a date range
- Save/load data across two CSV files for persistence between runs
- Boolean completion status correctly preserved across CSV save/load
- Input validation separated into a dedicated validators.py module
- Thoroughly commented and docstringed throughout for readability

## Project Structure
```
habit-tracker-python/
│
├── habit_tracker.py        ← main program
├── validators.py           ← input validation functions
├── habits_db.csv           ← habit records (auto-generated)
└── habit_logs_db.csv       ← habit log records (auto-generated)
```

## How to Run
```bash
python habit_tracker.py
```

## Built With
- Python 3
- OOP — two classes, private attributes, getter/setter methods
- CSV module for data persistence across two related files
- datetime module for date handling and validation
- Separated input validation module for clean, reusable code

## Data Persistence
Habit and log data are automatically saved to their respective CSV 
files after every operation and reloaded on next launch. Boolean 
completion values are correctly restored from CSV on each session.
