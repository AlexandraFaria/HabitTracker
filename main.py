from habit import Habit
import questionary
from datetime import datetime, date
from db import get_db, list_of_habits, list_of_habits_weekly, list_of_habits_daily, search_start_date
from operator import attrgetter


def cli():
    while True:
        db = get_db("main.db")

        choice = questionary.select("What would you like to do?",
                                    choices=["Create Habit", "Check Off Habit", "Show List of Habits", "Analyze Habit",
                                             "Delete Habit", "Reset Habit", "Exit"]).ask()

        if choice == "Create Habit":
            name = questionary.text("What is the name of your habit?").ask()
            description = questionary.text("What are you hoping your habit will improve?").ask()
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
                try:
                    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                    if start_date < date.today():
                        print("The date you entered is in the past. Please try again.")
                        raise ValueError("The date you entered is in the past.")
                except ValueError:
                    start_date = questionary.text("Enter the date you would like to start your "
                                                  "habit in the format YYYY-MM-DD:").ask()
                    # Check if the date is in the future
            habit = Habit(name, description, frequency, start_date)
            habit.save_habit()
            print(f"{habit}")

        elif choice == "Check Off Habit":
            habits = [habit[0] for habit in list_of_habits(db)]
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
                    print(f"{habit.name} has been checked off.")
                else:
                    raise ValueError(f"{habit.name} has not started yet.")
            except ValueError:
                print(f"{habit.name} has not started yet.")

        elif choice == "Show List of Habits":
            next_choice = questionary.select("Would you like to see all habits or just "
                                             "the daily or weekly habits?", choices=["All", "Daily", "Weekly"]).ask()
            if next_choice == "All":
                print("Here is a list of all your current habits:")
                habits = list_of_habits(db)
                for habit in habits:
                    print(habit[0])
            elif next_choice == "Daily":
                print("Here is a list of all your current daily habits:")
                habits = list_of_habits_daily(db)
                for habit in habits:
                    print(habit[0])
            elif next_choice == "Weekly":
                print("Here is a list of all your current weekly habits:")
                habits = list_of_habits_weekly(db)
                for habit in habits:
                    print(habit[0])

        elif choice == "Delete Habit":
            habits = [habit[0] for habit in list_of_habits(db)]
            habit = questionary.select("Which habit would you like to delete?:", habits).ask()
            habit = Habit(habit)
            habit.delete_habit()
            print(f"{habit.name} has been deleted.")

        elif choice == "Reset Habit":
            habits = [habit[0] for habit in list_of_habits(db)]
            habit = questionary.select("Which habit would you like to reset?:", habits).ask()
            habit = Habit(habit)
            start_date = questionary.select(f"Would you like to change your start date? "
                                            f"Current start date is: {habit.start_date}",
                                            choices=["Change to today.", "Stay the same.",
                                                     "Choose a day in the future."]).ask()
            if start_date == "Change to today.":
                start_date = date.today()
                start_date = datetime.strftime(start_date, "%Y-%m-%d")
                print("The start date has been changed to today.")

            elif start_date == "Stay the same.":
                start_date = habit.start_date
                print(f"Your start date is still: {habit.start_date}")

            elif start_date == "Choose a day in the future.":
                start_date = questionary.text("Enter the date you would like to start your habit in the "
                                              "format YYYY-MM-DD:").ask()
                try:
                    start_date = datetime.strptime(start_date, "%Y-%m-%d")
                    if start_date < datetime.today():
                        print("The date you entered is in the past. Please try again.")
                        raise ValueError("The date you entered is in the past.")
                except ValueError:
                    start_date = questionary.text("Enter the date you would like to start your "
                                                  "habit in the format YYYY-MM-DD:").ask()

            habit.reset_habit(date)
            print(f"{habit.name} has been reset.")

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