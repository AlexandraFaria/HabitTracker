"""This module includes the functions associated with checking user input and the main command line interface."""

from datetime import datetime, date
import calendar
import questionary
from habit import Habit
from db import (get_db, list_of_habits, list_of_habits_weekly, list_of_habits_daily, search_start_date, reset_habit,
                search_habit, delete_habit)
from analyse import get_longest_streak, get_current_streak, monthly_habit_completion, max_longest_streak


def check_date(start_date):
    """This function checks if the date entered is actually a date, by specifying the length of the data input (10),
        and checking the format. Then the date is verified to be in the future.
        If the date is not in the future or in poor formatting the user is prompted again to enter a date.

        If the date is in the future, the date is returned to the main function.

        parameters:
            start_date: str entered by the user

        returns:
            start_date: str in the format of YYYY-MM-DD (if the date has met all the requirements tested)
    """
    while True:
        try:
            if len(start_date) == 10:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                if start_date > date.today():
                    return start_date
                if start_date < date.today():
                    print("The date you entered is in the past. Please try again.")
                    raise ValueError("The date you entered is in the past.")
            # Tries to catch any errors of incorrect date format/strings entered.
            if len(start_date) != 10:
                print("The date you entered is not in the correct format. Please try again.")
                raise ValueError("The date you entered is not in the correct format.")
        except ValueError:
            start_date = questionary.text("Please enter a date in the correct format: YYYY-MM-DD:").ask()


def check_name(db, name):
    """This function checks if the name entered is not empty, does not start with a space, is not a digit, and does not
        already exist in the database.

        If the name meets all the requirements, the name is returned to the main function.

        If the name does not meet the requirements, the user is prompted to enter a new name.

        parameters:
            db: database connection from get_db() function
            name: str entered by the user

        returns:
            name: str (if the name has met all the requirements tested)
    """
    while True:
        try:
            name = (name.lower()).capitalize()
            result = search_habit(db, name)
            if not name:
                raise ValueError
            if name == "":
                raise ValueError
            if name.startswith(" "):
                raise ValueError
            if name.isdigit():
                raise ValueError
            if name != result:
                return name
            if result == name:
                raise ValueError
        except ValueError:
            name = questionary.text("Please enter a different name for your habit.  It either already "
                                    "exists or is not in the correct format.").ask()


def check_description(description):
    """This function checks if the description entered is not empty, does not start with a space, and is not a digit.

        If the description meets all the requirements, the description is returned to the main function.

        If the description does not meet the requirements, the user is prompted to enter a new description.

        parameters:
            description: str entered by the user

        returns:
            description: str (if the description has met all the requirements tested)
        """
    while True:
        try:
            if not description:
                raise ValueError
            if description == "":
                raise ValueError
            if description.startswith(" "):
                raise ValueError
            if description.isdigit():
                raise ValueError
            else:
                return description
        except ValueError:
            description = questionary.text("Please enter a different description that is meaningful to your habit."
                                           ).ask()


def cli():
    """This function is the main command line interface for the user to interact with the Habit Tracker."""
    while True:
        db = get_db(Habit.Database)
        choice = questionary.select("What would you like to do?",
                                    choices=["Create Habit", "Check Off Habit", "Show List of Habits", "Analyze Habit",
                                             "Delete Habit", "Reset Habit", "Exit"]).ask()

        if choice == "Create Habit":
            name = questionary.text("What is the name of your habit?").ask()
            name = check_name(db, name)

            description = questionary.text("What are you hoping your habit will improve?").ask()
            description = check_description(description)

            frequency = str(questionary.select("Choose the frequency of the habit",
                                               ["Daily", "Weekly", "Exit"]).ask())
            if frequency == "Exit":
                print(f"Your habit {name} was not created.")
                continue

            start_date = questionary.select("When would you like your habit to start?",
                                            choices=["Today", "A day in the Future", "Exit"]).ask()
            if start_date == "Today":
                start_date = date.today()
                # The date will be today's date

            elif start_date == "A day in the Future":
                start_date = questionary.text("Enter the date you would like to start your "
                                              "habit in the format YYYY-MM-DD:").ask()
                start_date = check_date(start_date)  # Check if the date is in the future and in the correct format

            elif start_date == "Exit":
                print(f"Your habit {name} was not created.")
                continue

            habit = Habit(name, description, frequency, start_date)
            habit.save_habit()
            print(f"\nPlease review the information you entered for your habit:\n\n{habit}\n")

        elif choice == "Check Off Habit":
            habits = [habit[0] for habit in list_of_habits(db)]

            if not habits:
                print("\nYou have no habits to check off.\n")
                continue
            else:
                habits.append("Exit")
                habit_name = questionary.select("Which habit would you like to check off?", habits).ask()
                if habit_name == "Exit":
                    continue
                else:
                    habit = Habit(habit_name)
                    start_date = search_start_date(db, habit_name)
                    # The start_date needs to be retrieved from the database.

                    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                    today_date = datetime.now().date()
                    # Put both dates in the same format to compare.

                    weekly_list = [habit[0] for habit in list_of_habits_weekly(db)]

                # Inform user of what day of the week their weekly habit should be checked off.
                if habit_name in weekly_list:
                    start_date_day_of_week = calendar.day_name[start_date.weekday()]
                    print(f"\nJust so you know, {habit_name} is a weekly habit.\n\nTrying to do this activity the same "
                          f"day each week\nwill help you to maintain your habit.\n\n"
                          f"In order for check-off events to count toward\nyour current streak and longest streak,\n"
                          f"you need to complete your habit on {start_date_day_of_week}s.\n")

                # Check if the habit has started yet.
                try:
                    if today_date >= start_date:
                        today_date = datetime.strftime(today_date, "%Y-%m-%d %H:%M")
                        # Put date into string format before saving.
                        habit.add_habit_completion_date(today_date)
                        print(f"\n{habit.name} has been checked off.\n")
                    else:
                        raise ValueError(f"{habit.name} has not started yet. Please wait until {start_date}.")
                except ValueError:
                    print(f"\n{habit.name} has not started yet. Please wait until {start_date}.\n")

        elif choice == "Show List of Habits":
            next_choice = questionary.select("Would you like to see all habits or just "
                                             "the daily or weekly habits?", choices=["All", "Daily", "Weekly", "Exit"]
                                             ).ask()
            if next_choice == "All":
                print("\nHere is a list of all your current habits:\n")
                habits = list_of_habits(db)
                if not habits:
                    print("\nYou have no habits logged.\n")
                    continue
                for habit in habits:
                    print(habit[0])

            elif next_choice == "Daily":
                print("\nHere is a list of all your current daily habits:\n")
                habits = list_of_habits_daily(db)
                if not habits:
                    print("\nYou have no daily habits logged.\n")
                    continue
                for habit in habits:
                    print(habit[0])

            elif next_choice == "Weekly":
                print("\nHere is a list of all your current weekly habits:\n")
                habits = list_of_habits_weekly(db)
                if not habits:
                    print("\nYou have no weekly habits logged.\n")
                    continue
                for habit in habits:
                    print(habit[0])

            elif next_choice == "Exit":
                continue

        elif choice == "Delete Habit":
            habits = [habit[0] for habit in list_of_habits(db)]

            if not habits:
                print("\nYou have no habits logged to delete.\n")
                continue
            else:
                habits.append("Exit")
                habit = questionary.select("Which habit would you like to delete?:", habits).ask()
                if habit == "Exit":
                    continue
                else:
                    delete_habit(db, habit)
                    print(f"\n{habit} has been deleted.\n")

        elif choice == "Reset Habit":
            habits = [habit[0] for habit in list_of_habits(db)]

            if not habits:
                print("\nYou have no habits logged to reset.\n")
                continue
            else:
                habits.append("Exit")
                # Inform user of what resetting a habit will do.
                print("\nPlease note that resetting a habit will delete all check-off events already logged "
                      "and provide a new start date for your habit.\n")
                habit_name = questionary.select("Which habit would you like to reset?:", habits).ask()
                if habit_name == "Exit":
                    continue
                else:
                    habit = Habit(habit_name)
                    start_date = search_start_date(db, habit_name)
                    change_start_date = questionary.select(f"Would you like to change your start date? " 
                                                           f"Current start date is: {start_date}",
                                                           choices=["Change to today.", "Stay the same.",
                                                                    "Choose a day in the future."]).ask()

                    if change_start_date == "Change to today.":
                        start_date = date.today()
                        start_date = datetime.strftime(start_date, "%Y-%m-%d")
                        reset_habit(db, habit_name, start_date)
                        print("\nThe start date has been changed to today.\n")

                    elif change_start_date == "Stay the same.":
                        print(f"\nYour start date is still: {start_date}\n")
                        # No change is needed.

                    elif change_start_date == "Choose a day in the future.":
                        start_date = questionary.text("Enter the date you would like to restart your habit in the "
                                                      "format YYYY-MM-DD:").ask()
                        check_date(start_date)  # Check if the date is in the future and in the correct format
                        reset_habit(db, habit_name, start_date)

                    print(f"\n{habit.name} has been reset.\n")

        elif choice == "Analyze Habit":
            analysis_choice = questionary.select("What would you like to analyze?",
                                                 choices=["Longest Streak of All Habits",
                                                          "Check-off Events for a Specific Month",
                                                          "Current Streak for a Habit",
                                                          "Longest Streak for a Habit",
                                                          "Exit"]).ask()

            if analysis_choice == "Longest Streak of All Habits":
                max_longest_streak(db)

            if analysis_choice == "Check-off Events for a Specific Month":
                month = questionary.text("Enter the month you would like to analyze in the format of 1-12:").ask()
                while True:
                    try:
                        month = int(month)
                        if 1 <= month <= 12:
                            break
                        if month < 1 or month > 12:
                            print("The month number you entered is not in the correct format. Please try again.")
                            raise ValueError
                    except ValueError:
                        month = questionary.text("Please enter a month in the correct format: 1-12:").ask()

                month_name = calendar.month_name[month]
                print(f"\nHere is a list of all the habits you completed in {month_name}:\n")
                monthly_habit_completion(db, month)

            if analysis_choice == "Current Streak for a Habit":
                habits = [habit[0] for habit in list_of_habits(db)]
                if not habits:
                    print("\nYou have no habits to analyze.\n")
                    continue
                else:
                    habits.append("Exit")
                    habit_name = questionary.select("For which habit would you like to know your "
                                                    "current streak?", habits).ask()
                    current_streak = get_current_streak(db, habit_name)
                    print(f"\n{habit_name} has a current streak of {current_streak}.\n")

            if analysis_choice == "Longest Streak for a Habit":
                habits = [habit[0] for habit in list_of_habits(db)]
                if not habits:
                    print("\nYou have no habits to analyze.\n")
                    continue
                else:
                    habits.append("Exit")
                    habit_name = questionary.select("For which habit would you like to know your longest streak?",
                                                    habits).ask()
                    longest_streak = get_longest_streak(db, habit_name)
                    print(f"\n{habit_name} has a longest streak of {longest_streak}.\n")

            if analysis_choice == "Exit":
                continue

        elif choice == "Exit":
            break


if __name__ == "__main__":
    cli()
