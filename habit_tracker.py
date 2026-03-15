"""
Habit Tracker

Log daily habits (e.g. exercise, reading, water intake)
Mark habits as done/not done each day
Show weekly completion summary
Save/load to CSV
Good practice: date handling + CSV combined, similar to expense tracker but different enough to reinforce the concepts
"""

"""
Classes:
Class - Attributes
Habit - habit_id, name, description
HabitLog - log_id, habit_id, date, completed
Features:

Add a new habit
Delete a habit
List all habits
Log a habit as completed or not for a given date
Show all logs for a specific habit
Show daily summary — which habits were completed on a given date
Show custom completion summary
Save/load all data to/from CSV

Two CSV files:

habits_db.csv — stores habit definitions
habit_logs_db.csv — stores daily log entries
"""

from validators import *
from datetime import datetime
import csv

class Habit:
    # Class-level counter used to assign unique, auto-incrementing IDs to each habit
    counter = 0

    def __init__(self, name, description):
        # Increment the shared counter before assigning so IDs start at 1
        Habit.counter += 1
        self.__habit_id = Habit.counter  # Unique identifier for this habit
        self.__name = name
        self.__description = description

    def get_habit_id(self):
        return self.__habit_id

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def set_name(self, name):
        self.__name = name

    def set_description(self, description):
        self.__description = description

    def __str__(self):
        return f"Habit ID: {self.__habit_id}, Name: {self.__name}, Description: {self.__description}"

class HabitLog:
    # Class-level counter used to assign unique, auto-incrementing IDs to each log entry
    counter = 0

    def __init__(self, habit_id, date, completed):
        # Increment the shared counter before assigning so IDs start at 1
        HabitLog.counter += 1
        self.__log_id = HabitLog.counter  # Unique identifier for this log entry
        self.__habit_id = habit_id        # Links this log back to a specific Habit
        self.__date = date                # The date this log entry applies to
        self.__completed = completed      # Boolean: True if the habit was done that day

    def get_log_id(self):
        return self.__log_id

    def get_habit_id(self):
        return self.__habit_id

    def get_date(self):
        return self.__date

    def get_completed(self):
        return self.__completed

    def set_date(self, date):
        self.__date = date

    def set_completed(self, completed):
        self.__completed = completed

    def __str__(self):
        return f"Log ID: {self.__log_id}, Habit ID: {self.__habit_id}, Date: {self.__date}, Completed: {self.__completed}"


# In-memory stores for all habits and their log entries
habits = []
habit_logs = []

def add_habit():
    """Prompt the user for a habit name and description, create a Habit, and persist it."""
    name = get_non_empty_string("Add habit name: ")
    description = get_non_empty_string("Add habit description: ")
    habit = Habit(name, description)
    habits.append(habit)
    save_habit_to_csv()  # Immediately persist so the new habit survives a restart

def delete_habit():
    """Remove a habit and all of its associated log entries by habit ID."""
    if len(habits) == 0:
        print("No habits present.")
        return
    habit_id = get_positive_int("Enter habit ID: ")
    for habit in habits:
        if habit.get_habit_id() == habit_id:
            habits.remove(habit)
            # Also purge every log that references the deleted habit
            habit_logs[:] = [log for log in habit_logs if log.get_habit_id() != habit_id]
            save_habit_to_csv()
            return
    print("Habit not found.")

def list_all_habits():
    """Print every habit currently stored in memory."""
    if len(habits) == 0:
        print("No habits present.")
    else:
        for habit in habits:
            print(habit)

def log_habit():
    """Record whether a specific habit was completed on a given date."""
    habit_id = get_positive_int("Enter habit ID: ")
    # Verify the referenced habit actually exists before creating a log entry
    if not any(habit.get_habit_id() == habit_id for habit in habits):
        print("Habit not found.")
        return
    date = get_date("Enter date (YYYY-MM-DD): ")
    # Keep prompting until the user enters a valid yes/no answer
    while True:
        completed = get_non_empty_string("Is the habit completed? Enter 'Yes' or 'No'")
        if completed.lower() == "yes":
            completed = True
            break
        elif completed.lower() == "no":
            completed = False
            break
        else:
            print("Please enter either 'Yes' or 'No'")
            continue
    habit_log = HabitLog(habit_id, date, completed)
    habit_logs.append(habit_log)
    save_habit_logs_to_csv()  # Persist immediately so the entry survives a restart

def show_all_logs():
    """Display every log entry for a specific habit, identified by its ID."""
    habit_id = get_positive_int("Enter habit ID: ")
    # Filter the full log list down to only entries for the requested habit
    selected_habit_logs = [log for log in habit_logs if log.get_habit_id() == habit_id]
    if len(selected_habit_logs) == 0:
        print("No logs present for this habit.")
        return
    for log in selected_habit_logs:
        print(log)

def daily_summary():
    """Show all habits that were marked completed on a specific date."""
    date = get_date("Enter date (YYYY-MM-DD): ")
    # Collect only the logs whose date matches the requested date
    logs_on_date = [log for log in habit_logs if log.get_date() == date]
    if len(logs_on_date) == 0:
        print("No logs found for this date.")
        return
    print("Here are the habits completed on that day:")
    # Cross-reference logs with habit definitions to print readable habit info
    for log in logs_on_date:
        for habit in habits:
            if log.get_habit_id() == habit.get_habit_id() and log.get_completed() == True:
                print(habit)

def custom_summary():
    """Show all habits completed within a user-defined date range (inclusive)."""
    start_date = get_date("Enter start date (YYYY-MM-DD): ")
    end_date = get_date("Enter end date (YYYY-MM-DD): ")
    # Guard against an inverted range before doing any filtering
    if end_date < start_date:
        print("End date can't be earlier than start date.")
        return
    # Use chained comparison to keep only logs that fall within the range
    logs_on_date = [log for log in habit_logs if start_date <= log.get_date() <= end_date]
    if len(logs_on_date) == 0:
        print("No logs found within this date range.")
        return
    print("Here are the habits completed during this date range:")
    # Cross-reference logs with habit definitions to print readable habit info
    for log in logs_on_date:
        for habit in habits:
            if log.get_habit_id() == habit.get_habit_id() and log.get_completed() == True:
                print(habit)

def save_habit_to_csv():
    """Overwrite habits_db.csv with the current in-memory list of habits."""
    with open("habits_db.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Habit ID", "Name", "Description"])  # Header row
        for habit in habits:
            writer.writerow([
                habit.get_habit_id(),
                habit.get_name(),
                habit.get_description()
            ])

def load_habit_from_csv():
    """Read habits_db.csv and reconstruct Habit objects into the in-memory list.

    The counter is rewound to (ID - 1) before each Habit() call so that the
    auto-increment inside __init__ lands on the original saved ID.
    Silently does nothing if the file doesn't exist yet (first run).
    """
    try:
        with open("habits_db.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Rewind counter so the next Habit() call restores the original ID
                Habit.counter = int(row["Habit ID"]) - 1
                habit = Habit(row["Name"], row["Description"])
                habits.append(habit)
    except FileNotFoundError:
        pass  # First run — no CSV exists yet, start with an empty list

def save_habit_logs_to_csv():
    """Overwrite habit_logs_db.csv with the current in-memory list of log entries."""
    with open("habit_logs_db.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Log ID", "Habit ID", "Date", "Completed"])  # Header row
        for log in habit_logs:
            writer.writerow([
                log.get_log_id(),
                log.get_habit_id(),
                log.get_date(),
                log.get_completed()
            ])

def load_habit_logs_from_csv():
    """Read habit_logs_db.csv and reconstruct HabitLog objects into the in-memory list.

    The counter is rewound to (ID - 1) before each HabitLog() call so that the
    auto-increment inside __init__ lands on the original saved ID.
    The date string is parsed back to a date object, and the 'Completed' string
    is converted to a boolean via equality comparison.
    Silently does nothing if the file doesn't exist yet (first run).
    """
    try:
        with open("habit_logs_db.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Rewind counter so the next HabitLog() call restores the original ID
                HabitLog.counter = int(row["Log ID"]) - 1
                log = HabitLog(
                    int(row["Habit ID"]),
                    datetime.strptime(row["Date"], "%Y-%m-%d").date(),  # Parse string → date
                    row["Completed"] == "True"  # Convert stored string back to bool
                )
                habit_logs.append(log)
    except FileNotFoundError:
        pass  # First run — no CSV exists yet, start with an empty list

def user_menu():
    """Main interactive loop that displays the menu and routes user choices."""
    while True:
        print("\nEnter 1 to add habit")
        print("Enter 2 to delete habit")
        print("Enter 3 to list all habits")
        print("Enter 4 to log habit")
        print("Enter 5 to show all logs")
        print("Enter 6 to show daily summary")
        print("Enter 7 to show custom summary")
        print("Enter 0 to Exit\n")

        # Re-prompt until the user enters a value in the valid menu range
        while True:
            choice = get_positive_int("Type your choice and press enter: ")
            if 0 <= choice <= 7:
                break
            print("\nChoice needs to be between 0 to 7.")

        if choice == 1:
            add_habit()
        elif choice == 2:
            delete_habit()
        elif choice == 3:
            list_all_habits()
        elif choice == 4:
            log_habit()
        elif choice == 5:
            show_all_logs()
        elif choice == 6:
            daily_summary()
        elif choice == 7:
            custom_summary()
        elif choice == 0:
            print("\nGoodbye!")
            break


def main():
    # Load persisted data before starting the menu so previous sessions are restored
    load_habit_from_csv()
    load_habit_logs_from_csv()
    user_menu()

if __name__ == "__main__":
    main()
