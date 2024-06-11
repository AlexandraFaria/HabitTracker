# sort out repeated code for finding the filtered data for the weekly current and longest streak
# work on getting down the duplicate code--- make into another function!


from db import (get_primary_key, get_date_list, get_db, list_of_habits_daily, list_of_habits_weekly, search_habit,
                search_start_date)
from datetime import timedelta, date, datetime


def calculate_longest_streak(db, name):
    """Calculate the longest streak by comparing current streak to the longest streak."""

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
    """Calculate the longest streak by comparing current streak to the longest streak."""

    habit_id = get_primary_key(db, name)
    dates = get_date_list(db, habit_id)

    if not dates:
        return 0
    else:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        day_of_week = start_date.weekday()

        filtered_list = list(filter(lambda x: (x.weekday() == day_of_week), dates))

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
    """Get the longest streak of the habit."""
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
    """Calculate the current streak of the habit, if there is a completion date with today's date."""

    habit_id = get_primary_key(db, name)

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
    """Calculate the longest streak by comparing current streak to the longest streak."""

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
    """Get the current streak of the habit."""
    daily_list = [habit[0] for habit in list_of_habits_daily(db)]
    weekly_list = [habit[0] for habit in list_of_habits_weekly(db)]

    if name in daily_list:
        current_streak = calculate_current_streak(db, name)
        return f"{current_streak} days"

    if name in weekly_list:
        start_date = search_start_date(db, name)
        current_streak = calculate_current_streak_weekly(db, name, start_date)
        return f"{current_streak} weeks"


# Need to improve data redundancy in the following functions. Also-- Need to add feature that only includes dates from
# less than 1 year ago. (So then days from May 2024 are not counted with May 2025.)
def monthly_habit_completion(db, month):
    """Get the number of completions for each habit in the last month, in ascending order.

    parameters:
        db: Database connection.
       month(int): Numerical value of month for date retrieval.
    returns:
       list: Number of check-off events for each habit in the last month separated by frequency.
    """
    print("Daily Habits:\n")
    daily_list = [habit[0] for habit in list_of_habits_daily(db)]

    if not daily_list:
        print("\nYou have no habits logged to analyze.\n")
    else:
        daily_habit_total = {}

        for habit in daily_list:
            habit_id = get_primary_key(db, habit)
            dates = get_date_list(db, habit_id)
            month_check_offs = [check_off for check_off in dates if check_off.month == month]
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

        for habit in weekly_list:
            habit_id = get_primary_key(db, habit)
            dates = get_date_list(db, habit_id)
            month_check_offs = [check_off for check_off in dates if check_off.month == month]
            weekly_habit_total[habit] = len(month_check_offs)
        sort_weekly_habit_total = dict(sorted(weekly_habit_total.items(), key=lambda x: x[1]))
        for key, value in sort_weekly_habit_total.items():
            print(f"{key}: {value}")


def max_longest_streak(db):
    """Get the habit with the longest streak for daily and weekly habits."""

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

