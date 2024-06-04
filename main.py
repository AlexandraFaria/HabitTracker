from habit import Habit
import questionary
from datetime import datetime, date
from db import get_db, list_of_habits, list_of_habits_weekly, list_of_habits_daily


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
                start_date = None
                # The date will be today's date

            elif start_date == "A day in the Future":
                start_date = questionary.text("Enter the date you would like to start your "
                                              "habit in the format YYYY-MM-DD:").ask()
                try:
                    start_date = datetime.strptime(start_date, "%Y-%m-%d")
                    if start_date < datetime.today():
                        print("The date you entered is in the past. Please try again.")
                        raise ValueError("The date you entered is in the past.")
                except ValueError:
                    start_date = questionary.text("Enter the date you would like to start your "
                                                  "habit in the format YYYY-MM-DD:").ask()
                    # Check if the date is in the future
            habit = Habit(name, description, frequency, start_date)
            habit.save_habit()
            print(f"{habit.name} habit has been created.")

        elif choice == "Check Off Habit":
            habits = [habit[0] for habit in list_of_habits(db)]
            habit = questionary.select("Which habit would you like to check off?", habits).ask()
            habit = Habit(habit)
            habit.add_habit_completion_date()
            print(f"{habit.name} habit has been checked off.")

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
    # elif choice == "Delete Habit":
    #     name = text("Enter the name of the habit:").ask()
    #     habit = Habit(name)
    #     habit.delete_habit()
    #     print(f"{habit.name} has been deleted.")
    #
    # elif choice == "Exit":
    #     break


# if __name__ == "__main__":
#     main()