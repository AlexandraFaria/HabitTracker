from habit import Habit
import questionary
from datetime import datetime, date
from db import (get_db, list_of_habits, list_of_habits_weekly, list_of_habits_daily, search_start_date, reset_habit,
                search_habit)
from analyse import get_longest_streak
from operator import attrgetter


def check_date(start_date):
    while True:
        try:
            if len(start_date) == 10:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                if start_date > date.today():
                    break
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
            description = questionary.text("Please enter a different description that is meaningful to your habit.").ask()


def cli():
    while True:
        db = get_db("test.db")

        choice = questionary.select("What would you like to do?",
                                    choices=["Create Habit", "Check Off Habit", "Show List of Habits", "Analyze Habit",
                                             "Delete Habit", "Reset Habit", "Exit"]).ask()

        if choice == "Create Habit":
            name = questionary.text("What is the name of your habit?").ask()
            name = check_name(db, name)

            description = questionary.text("What are you hoping your habit will improve?").ask()
            description = check_description(description)

            frequency = str(questionary.select("Choose the frequency of the habit",
                                               ["Daily", "Weekly"]).ask())
            start_date = questionary.select("When would you like your habit to start?",
                                            choices=["Today", "A day in the Future"]).ask()
            if start_date == "Today":
                start_date = date.today()
                # The date will be today's date

            elif start_date == "A day in the Future":
                start_date = questionary.text("Enter the date you would like to start your "
                                              "habit in the format YYYY-MM-DD:").ask()
                check_date(start_date)  # Check if the date is in the future
            habit = Habit(name, description, frequency, start_date)
            habit.save_habit()
            print(f"\nPlease review the information you entered for your habit:\n\n{habit}\n")

        elif choice == "Check Off Habit":
            habits = [habit[0] for habit in list_of_habits(db)]
            if not habits:
                print("\nYou have no habits to check off.\n")
                continue
            habit_name = questionary.select("Which habit would you like to check off?", habits).ask()
            habit = Habit(habit_name)
            start_date = search_start_date(db, habit_name)
            # The start_date needs to be retrieved from the database.

            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            today_date = datetime.now().date()
            # Put both dates in the same format to compare.

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
                                             "the daily or weekly habits?", choices=["All", "Daily", "Weekly"]).ask()
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

        elif choice == "Delete Habit":
            habits = [habit[0] for habit in list_of_habits(db)]
            if not habits:
                print("\nYou have no habits logged to delete.\n")
                continue
            habit = questionary.select("Which habit would you like to delete?:", habits).ask()
            habit = Habit(habit)
            habit.delete_habit()
            print(f"\n{habit.name} has been deleted.\n")

        elif choice == "Reset Habit":
            habits = [habit[0] for habit in list_of_habits(db)]
            if not habits:
                print("\nYou have no habits logged to reset.\n")
                continue
            habit_name = questionary.select("Which habit would you like to reset?:", habits).ask()
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
                check_date(start_date)  # Check if the date is in the future
                reset_habit(db, habit_name, start_date)

            print(f"\n{habit.name} has been reset.\n")

        elif choice == "Analyze Habit":
            analysis_choice = questionary.select("What would you like to analyze?",
                                                 choices=["Longest Streak of All Habits",
                                                          "Last Months Habit Check-offs",
                                                          "Current Streak for a Habit",
                                                          "Longest Streak for a Habit"]).ask()

            if analysis_choice == "Longest Streak of All Habits":
                pass
            if analysis_choice == "Last Months Habit Check-offs":
                pass
            if analysis_choice == "Current Streak for a Habit":
                pass
            if analysis_choice == "Longest Streak for a Habit":
                habits = [habit[0] for habit in list_of_habits(db)]
                if not habits:
                    print("\nYou have no habits to analyze.\n")
                    continue
                habit_name = questionary.select("For which habit would you like to know your longest streak?",
                                                habits).ask()
                longest_streak = get_longest_streak(db, habit_name)
                print(f"\n{habit_name} has a longest streak of {longest_streak}.\n")

        elif choice == "Exit":
            break


if __name__ == "__main__":
    cli()



    #
    # elif choice == "Get Longest Streak":
    #     name = text("Enter the name of the habit:").ask()
    #     habit = Habit(name)
    #     habit.get_longest_streak()
    #     print(f"{habit.name} has a longest streak of {habit.longest_streak}.")
    #
    # elif choice == "Get Current Streak":
    #     name = text("Enter the name of the habit:").ask()
    #     habit = Habit(name)
    #     habit.get_current_streak()
    #     print(f"{habit.name} has a current streak of {habit.current_streak}.")
    #

    #
    # elif choice == "Exit":
    #     break


# if __name__ == "__main__":
#     main()