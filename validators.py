from datetime import datetime

def get_positive_int(prompt):
    """Repeatedly prompts the user until a non-negative integer is entered."""
    while True:
        try:
            num = int(input(prompt))
            if num < 0:
                print("Number cannot be negative.")
            else:
                return num
        except ValueError:
            print("Invalid input. Please enter a non-negative integer.")

def get_positive_float(prompt):
    """Repeatedly prompts the user until a strictly positive float is entered."""
    while True:
        try:
            num = float(input(prompt))
            if num <= 0:
                print("Number needs to be positive.")
            else:
                return num
        except ValueError:
            print("Invalid input. Please enter a positive float.")

def get_non_negative_float(prompt):
    """Repeatedly prompts the user until a non-negative float is entered.

    Accepts zero, since 0 is a valid score (e.g. a student who submits nothing).
    """
    while True:
        try:
            num = float(input(prompt))
            if num < 0:
                print("Number cannot be negative.")
            else:
                return num
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_non_empty_string(prompt):
    """Repeatedly prompts the user until a non-empty string is entered."""
    while True:
        text = input(prompt)
        if text == "":
            print("Invalid input. Text field can not be empty.")
        else:
            return text

def get_date(prompt):
    """Repeatedly prompts the user until a valid YYYY-MM-DD date is entered."""
    while True:
        text = input(prompt)
        try:
            return datetime.strptime(text, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date. Please use YYYY-MM-DD format (e.g. 2026-03-14).")