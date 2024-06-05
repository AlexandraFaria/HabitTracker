"""This module contains the Habit class and associated methods."""


from datetime import datetime, timedelta, date
from db import (get_db, add_habit, get_primary_key, add_habit_completion, search_habit, get_date_list,
                reset_habit, delete_habit)
from analyse import (calculate_longest_streak, calculate_current_streak, calculate_longest_streak_weekly,
                     calculate_current_streak_weekly)
from operator import attrgetter


class Habit:
    """This is the Habit Class and associated methods."""

    Database = "test.db"
    habits = []

    @classmethod
    def max_longest_streak(cls):
        """Get the habit with the longest streak for daily and weekly habits."""

        for habit in cls.habits:
            habit.get_longest_streak()

        daily_habits = [habit for habit in cls.habits if habit.frequency == "Daily"]
        maximum_daily_streak = max(daily_habits, key=attrgetter('longest_streak'))

        weekly_habits = [habit for habit in cls.habits if habit.frequency == "Weekly"]
        maximum_weekly_streak = max(weekly_habits, key=attrgetter('longest_streak'))

        return (f"\nDaily Habit with longest streak: "
                f"{maximum_daily_streak.name} with {maximum_daily_streak.longest_streak} days.\n"
                f"\nWeekly Habit with longest streak: {maximum_weekly_streak.name} "
                f"with {maximum_weekly_streak.longest_streak} weeks.")

    @classmethod
    def monthly_habit_completion(cls, month: int):
        """Get the number of completions for each habit in the last month, in ascending order.


        parameters:
           month(int): Numerical value of month for date retrieval.
        returns:
           list: Number of completion events for each habit in the last month separated by frequency.
        """
        # Not sure how to reduce code redundancy.

        month = int(month)
        if 1 <= month <= 12:

            # First create a list of completion events for daily habits.
            print("\nDaily Habits: Number of completion events in a month.")
            daily_habits = [habit for habit in cls.habits if habit.frequency == "Daily"]
            daily_habit_total = {}

            for habit in daily_habits:
                habit_id = get_primary_key(habit.db, habit.name)
                dates = get_date_list(habit.db, habit_id)
                month_check_offs = [check_off for check_off in dates if check_off.month == month]
                daily_habit_total[habit.name] = len(month_check_offs)
            sort_daily_habit_total = dict(sorted(daily_habit_total.items(), key=lambda x: x[1]))
            for key, value in sort_daily_habit_total.items():
                print(f"{key}: {value}")

            # Second create a list of completion events for weekly habits.
            print("\nWeekly Habits: Number of completion events in a month.")
            weekly_habits = [habit for habit in cls.habits if habit.frequency == "Weekly"]
            weekly_habit_total = {}

            for habit in weekly_habits:
                habit_id = get_primary_key(habit.db, habit.name)
                dates = get_date_list(habit.db, habit_id)
                month_check_offs = [check_off for check_off in dates if check_off.month == month]
                weekly_habit_total[habit.name] = len(month_check_offs)
            sort_weekly_habit_total = dict(sorted(weekly_habit_total.items(), key=lambda x: x[1]))
            for key, value in sort_weekly_habit_total.items():
                print(f"{key}: {value}")

        else:
            raise (ValueError("Please enter a valid month between 1 and 12."))

    def __init__(self, name: str = None, description: str = None, frequency: str = None, start_date: date = None):
        """
        Initialize Habit Instance.


        parameters:
           name (str): Name of the habit.
           description(str): Description of the habit.
           frequency(str): Periodicity habit should be done.
           start_date(date): Date the habit was started.
           database(str): Name of the database to connect to. Default is main.db.
           self.habit_id(int): Primary key of the habit.
           self.current_streak(int): Current streak of the habit, including today's date.
           self.longest_streak(int): Longest streak of the habit.
        """
        self.name = (name.lower()).capitalize()
        self.description = description
        self.frequency = frequency
        self.start_date = start_date
        self.habit_id = None
        self.current_streak = 0
        self.longest_streak = 0
        self.db = get_db(self.Database)
        self.habits.append(self) if self not in self.habits else None

    def __str__(self):
        """
        Description of attributes and values of the habit.


        Returns:
           str: Description of the habit.
        """
        return (f"""Habit: {self.name} \nDescription: {self.description} \nFrequency: {self.frequency}"""
                f"""\nStart Date: {self.start_date}""")

    def save_habit(self):
        """
       Save the habit to the database.


       Method first searches database to see if the habit already exists.
       If habit exists, it will print a message saying the habit already exists.
       If habit does not exist, it will be added to the database.


        """
        result = search_habit(self.db, self.name)
        if result == self.name:
            print(f"{self.name} already exists.")

        else:
            add_habit(self.db, self.name, self.description, self.frequency, self.start_date)
            self.habit_id = get_primary_key(self.db, self.name)
            return self.habit_id

    @staticmethod
    def check_date_input_past(completion_date):
        """
       Check if the date is in the correct format and not in the future.


       argument:
           completion_date(str): Date the habit was completed.


       returns:
           str: Date in the correct format or statement showing the date is in the future.
        """
        try:
            completion_date = datetime.strptime(completion_date, "%Y-%m-%d %H:%M")
            current_datetime = datetime.now()
            if completion_date > current_datetime:
                print("The date you entered is in the future.")
            else:
                completion_date = datetime.strftime(completion_date, "%Y-%m-%d %H:%M")
                return completion_date
        except ValueError or TypeError:
            print("The date you entered is not in the correct format.")
            print("Please enter a date in the format: YYYY-MM-DD HH:MM")
            return

    @staticmethod
    def check_month(month):
        """Check the input of a month to make sure it is an integer and between 1-12"""
        month = int(month)
        if 1 <= month <= 12:
            return month
        else:
            raise ValueError("Please enter a valid month between 1 and 12.")

    def add_habit_completion_date(self, completion_date=None):
        """
        Add a completion date to the habit.


        If no completion date is added, the default is the current date and time.
        If a date is added by the user, the date is checked by the check_date_input_past method to make sure
        the date is in the correct format and not in the future.


        argument:
           completion_date(str): Date the habit was completed. Default is today, if not provided.
        """
        if completion_date is None:
            self.habit_id = get_primary_key(self.db, self.name)
            add_habit_completion(self.db, self.habit_id, completion_date)
        else:
            completion_date = self.check_date_input_past(completion_date)
            self.habit_id = get_primary_key(self.db, self.name)
            add_habit_completion(self.db, self.habit_id, completion_date)

    def get_longest_streak(self):
        """Get the longest streak of the habit."""
        if self.frequency == "Daily":
            self.longest_streak = calculate_longest_streak(self.db, self.name)
            return self.longest_streak
        if self.frequency == "Weekly":
            self.longest_streak = calculate_longest_streak_weekly(self.db, self.name, self.start_date)
            return self.longest_streak

    def get_current_streak(self):
        """Get the current streak of the habit."""
        if self.frequency == "Daily":
            self.current_streak = calculate_current_streak(self.db, self.name, self.habit_id)
            return self.current_streak
        if self.frequency == "Weekly":
            self.current_streak = calculate_current_streak_weekly(self.db, self.name, self.start_date)
            return self.current_streak

    def reset_habit(self, start_date=None):
        """Reset the habit by deleting all completion dates and add a new start date."""
        reset_habit(self.db, self.habit_id, start_date)
        self.start_date = start_date
        return self.start_date

    def delete_habit(self):
        """Delete the habit from the database completely and remove from the habits list."""
        self.habit_id = get_primary_key(self.db, self.name)
        delete_habit(self.db, self.habit_id)
        self.habits.remove(self)
        return self.habits