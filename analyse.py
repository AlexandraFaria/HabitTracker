"""This module contains functions to analyze the data in the database."""

from datetime import timedelta, date, datetime
from db import (get_primary_key, get_date_list, list_of_habits_daily, list_of_habits_weekly, search_start_date)


def calculate_longest_streak(db, name):
    """Calculate the longest streak for daily habits.

    dates = a list of check off dates for the habit searched via the habit_id (primary key)

    If there are no dates for the habit, the function returns 0. If there are dates, the function proceeds to the
    calculation.

    The longest streak is calculated by looping through the list of dates and counting the number of consecutive days.
    This value is sent to the current_reviewed_streak variable. Once the streak breaks, the current_reviewed_streak is
    sent to the longest_streak variable. Then the count continues with the current_reviewed_streak reset to 1. This
    cycle continues until the end of the list of dates.

    parameters:
        db: Database connection from get_db() function
        name(str): Name of the habit used to search habit_id

    returns:
        int: The longest streak of the habit."""

    habit_id = get_primary_key(db, name)
    dates = get_date_list(db, habit_id)

    if not dates:
        return 0
    else:
        longest_streak = 1
        current_reviewed_streak = 1

        for i in range(1, len(dates)):
            if dates[i] == dates[i - 1] - timedelta(days=1):
                current_reviewed_streak += 1
            elif dates[i] == dates[i - 1]:
                continue
            else:
                longest_streak = max(longest_streak, current_reviewed_streak)
                current_reviewed_streak = 1

        longest_streak = max(current_reviewed_streak, longest_streak)
        return longest_streak


def calculate_longest_streak_weekly(db, name, start_date):
    """Calculate the longest streak for weekly habits.

    dates = a list of check off dates for the habit searched via the habit_id (primary key)

    If there are no dates for the habit, the function returns 0. If there are dates, the function proceeds to the
    calculation.

    The list of dates is then filtered to only include the dates that match the day of the week the habit was started.
    Again, if this list is empty, the function returns 0. Otherwise, the calculation proceeds to find the longest
    streak by counting the longest streak of consecutive weeks with a check-off on the required day of the week.

    parameters:
        db: Database connection from get_db() function
        name(str): Name of the habit used to search habit_id

    returns:
        int: The longest streak of the habit."""

    habit_id = get_primary_key(db, name)
    dates = get_date_list(db, habit_id)

    if not dates:
        return 0
    else:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        day_of_week = start_date.weekday()

        filtered_list = list(filter(lambda x: (x.weekday() == day_of_week), dates))

        if not filtered_list:
            return 0
        else:
            current_reviewed_streak = 1
            longest_streak = 1

            for i in (range(1, len(filtered_list))):
                if filtered_list[i] == filtered_list[i - 1] - timedelta(weeks=1):
                    current_reviewed_streak += 1
                    longest_streak = max(longest_streak, current_reviewed_streak)
                else:
                    current_reviewed_streak = 1

            longest_streak = max(longest_streak, current_reviewed_streak)
            return longest_streak


def get_longest_streak(db, name):
    """Get the longest streak of given habit regardless of frequency.

    daily_list = a list of daily habits filtered from the database by frequency
    weekly_list = a list of weekly habits filtered from the database by frequency

    Uses the functions calculate_longest_streak (daily) and calculate_longest_streak_weekly (weekly)

    parameters:
        db: Database connection from get_db() function
        name(str): Name of the habit used to search habit_id

    returns:
        str: The longest streak of the habit with designated unit (days or weeks)
    """

    # Check the frequency of the habit
    daily_list = [habit[0] for habit in list_of_habits_daily(db)]
    weekly_list = [habit[0] for habit in list_of_habits_weekly(db)]

    if name in daily_list:
        longest_streak = calculate_longest_streak(db, name)
        return f"{longest_streak} days"

    if name in weekly_list:
        start_date = search_start_date(db, name)
        longest_streak = calculate_longest_streak_weekly(db, name, start_date)
        return f"{longest_streak} weeks"


def calculate_current_streak(db, name):
    """Calculate the current streak of daily habits.

    dates = a list of check off dates for the habit searched via the habit_id (primary key)

    If there are no dates for the habit, the function returns 0. If there are dates, the function proceeds to the
    calculation.

    The current streak is only calculated if the date at index [0] is today's date. Then, it is calculated by looping
    through the list of dates and counting the number of consecutive days until the streak breaks.

    parameters:
        db: Database connection from get_db() function
        name(str): Name of the habit used to search habit_id

    returns:
        int: The current streak of the habit.
    """

    today = date.today()

    habit_id = get_primary_key(db, name)
    dates = get_date_list(db, habit_id)

    if not dates:
        print(f"Habit {name} has not yet added any completion dates.")
        return 0
    else:
        current_streak = 0

        if dates[0] == today:
            current_streak += 1
            for i in range(1, len(dates)):
                if dates[i] == dates[i - 1] - timedelta(days=1):
                    current_streak += 1
                elif dates[i] == dates[i - 1]:
                    continue
                else:
                    break
        else:
            current_streak = 0

        return current_streak


def calculate_current_streak_weekly(db, name, start_date):
    """Calculate the current streak of weekly habits.

    dates = a list of check off dates for the habit searched via the habit_id (primary key)

    If there are no dates for the habit, the function returns 0. If there are dates, the function proceeds to the
    calculation.

    filtered_list = a list of dates that match the day of the week the habit was started

    If the filtered_list is empty, the function returns 0. Otherwise, the calculation proceeds.

    The current streak is only calculated if the date at index [0] is within the last week. Then, it is calculated by
    counting the number of consecutive weeks when the habit was completed on the required day of the week.

    parameters:
        db: Database connection from get_db() function
        name(str): Name of the habit used to search habit_id

    returns:
        int: The current streak of the habit.
    """

    habit_id = get_primary_key(db, name)
    today = date.today()
    dates = get_date_list(db, habit_id)

    if not dates:
        print(f"Habit {name} has not yet added any completion dates.")
        return 0
    else:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        day_of_week = start_date.weekday()
        filtered_list = list(filter(lambda x: (x.weekday() == day_of_week), dates))

        if not filtered_list:
            return 0
        else:
            current_streak = 1

            if filtered_list[0] >= today - timedelta(weeks=1):
                for i in (range(1, len(filtered_list))):
                    if filtered_list[i] == filtered_list[i - 1] - timedelta(weeks=1):
                        current_streak += 1
                    else:
                        break
            else:
                current_streak = 0

            return current_streak


def get_current_streak(db, name):
    """Get the current streak of given habit regardless of frequency.

    daily_list = a list of daily habits filtered from the database by frequency
    weekly_list = a list of weekly habits filtered from the database by frequency

    Uses the functions calculate_current_streak (daily) and calculate_current_streak_weekly (weekly)

    parameters:
        db: Database connection from get_db() function
        name(str): Name of the habit used to search habit_id

    returns:
        str: The current streak of the habit with designated unit (days or weeks)
    """

    daily_list = [habit[0] for habit in list_of_habits_daily(db)]
    weekly_list = [habit[0] for habit in list_of_habits_weekly(db)]

    if name in daily_list:
        current_streak = calculate_current_streak(db, name)
        return f"{current_streak} days"

    if name in weekly_list:
        start_date = search_start_date(db, name)
        current_streak = calculate_current_streak_weekly(db, name, start_date)
        return f"{current_streak} weeks"


# Need to improve data redundancy in the following two functions monthly_habit_completion and max_longest_streak
def monthly_habit_completion(db, month):
    """Get the number of completions for each habit for the provided month, in ascending order.

    daily_list = a list of daily habits filtered from the database by frequency
    weekly_list = a list of weekly habits filtered from the database by frequency

    The function loops through the list of daily habits and weekly habits and filters the dates to only include the
    dates that match the designated month and are within the most recent year.

    The function then counts the number of check-off events for each habit and stores the count in a dictionary with the
    habit name as the key and the count as the value. The dictionary is then sorted in ascending order by the number of
    check off events.

    parameters:
        db: Database connection.
       month(int): Numerical value of month for date retrieval.

    returns:
       list of key:value pairs: Name of habit with number of check-off events in the designated month separated by
                                periodicity.
    """
    print("Daily Habits:\n")
    daily_list = [habit[0] for habit in list_of_habits_daily(db)]

    if not daily_list:
        print("\nYou have no habits logged to analyze.\n")
    else:
        daily_habit_total = {}
        cutoff_date = date.today() - timedelta(days=365)

        for habit in daily_list:
            habit_id = get_primary_key(db, habit)
            dates = get_date_list(db, habit_id)
            month_check_offs = [check_off for check_off in dates if check_off.month == month and
                                check_off > cutoff_date]
            daily_habit_total[habit] = len(month_check_offs)
        sort_daily_habit_total = dict(sorted(daily_habit_total.items(), key=lambda x: x[1]))
        for key, value in sort_daily_habit_total.items():
            print(f"{key}: {value}")

    print("\nWeekly Habits:\n")
    weekly_list = [habit[0] for habit in list_of_habits_weekly(db)]

    if not weekly_list:
        print("\nYou have no habits logged to analyze.\n")
    else:
        weekly_habit_total = {}
        cutoff_date = date.today() - timedelta(days=365)

        for habit in weekly_list:
            habit_id = get_primary_key(db, habit)
            dates = get_date_list(db, habit_id)
            month_check_offs = [check_off for check_off in dates if check_off.month == month and
                                check_off > cutoff_date]
            weekly_habit_total[habit] = len(month_check_offs)
        sort_weekly_habit_total = dict(sorted(weekly_habit_total.items(), key=lambda x: x[1]))
        for key, value in sort_weekly_habit_total.items():
            print(f"{key}: {value}")


def max_longest_streak(db):
    """Analyzes the longest streak of all habits in the database and returns the daily and weekly habit with the longest
    streak.

    daily_list = a list of daily habits filtered from the database by frequency
    weekly_list = a list of weekly habits filtered from the database by frequency

    The function loops through the list of daily habits and weekly habits and calculates the longest streak for each
    storing these values in a dictionary with the habit name as the key and the longest streak as the value.

    The function then finds the maximum value of the dictionary and prints the habit with the longest streak with its
    corresponding unit (days or weeks).

    parameters:
        db: Database connection.

    returns:
        str: Daily and weekly habit with the longest streak and the number of days or weeks.

    """

    print("\nDaily Habits:\n")
    daily_list = [habit[0] for habit in list_of_habits_daily(db)]
    if not daily_list:
        print("\nYou have no habits logged to analyze.\n")
    else:
        daily_habit_longest_streak = {}

        for habit in daily_list:
            longest_streak = calculate_longest_streak(db, habit)
            daily_habit_longest_streak[habit] = longest_streak
        maximum_daily_streak = max(daily_habit_longest_streak, key=daily_habit_longest_streak.get)
        print(f"Daily Habit with Longest Streak: {maximum_daily_streak} with "
              f"{daily_habit_longest_streak[maximum_daily_streak]} days.\n")

    print("Weekly Habits:\n")
    weekly_list = [habit[0] for habit in list_of_habits_weekly(db)]
    if not weekly_list:
        print("\nYou have no habits logged to analyze.\n")
    else:
        weekly_habit_longest_streak = {}

        for habit in weekly_list:
            start_date = search_start_date(db, habit)
            longest_streak = calculate_longest_streak_weekly(db, habit, start_date)
            weekly_habit_longest_streak[habit] = longest_streak
        maximum_weekly_streak = max(weekly_habit_longest_streak, key=weekly_habit_longest_streak.get)
        print(f"Weekly Habit with Longest Streak: {maximum_weekly_streak} with "
              f"{weekly_habit_longest_streak[maximum_weekly_streak]} weeks.\n")
