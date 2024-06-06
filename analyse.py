# sort out repeated code for finding the filtered data for the weekly current and longest streak
# work on getting down the duplicate code--- make into another function!


from db import (get_primary_key, get_date_list, get_db, list_of_habits_daily, list_of_habits_weekly, search_habit,
                search_start_date)
from datetime import timedelta, date, datetime


def calculate_longest_streak(db, name, habit_id=None):
    """Calculate the longest streak by comparing current streak to the longest streak."""

    habit_id = get_primary_key(db, name)

    if habit_id is None:
        print(f"Habit {name} has not yet added any completion dates.")
    else:
        dates = get_date_list(db, habit_id)

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


def calculate_longest_streak_weekly(db, name, start_date, habit_id=None):
    """Calculate the longest streak by comparing current streak to the longest streak."""

    habit_id = get_primary_key(db, name)

    if habit_id is None:
        print(f"Habit {name} has not yet added any completion dates.")

    else:
        dates = get_date_list(db, habit_id)

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


def calculate_current_streak(db, name, habit_id=None):
    """Calculate the current streak of the habit, if there is a completion date with today's date."""

    habit_id = get_primary_key(db, name)

    today = date.today()

    if habit_id is None:
        print(f"Habit {name} has not yet added any completion dates.")
    else:
        dates = get_date_list(db, habit_id)

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

def calculate_current_streak_weekly(db, name, start_date, habit_id=None):
    """Calculate the longest streak by comparing current streak to the longest streak."""

    habit_id = get_primary_key(db, name)

    today = date.today()

    if habit_id is None:
        print(f"Habit {name} has not yet added any completion dates.")

    else:
        dates = get_date_list(db, habit_id)

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




#
# def calculate_longest_streak(db, name, habit_id=None):
#     """Calculate the longest streak by comparing current streak to the longest streak."""
#
#     habit_id = get_primary_key(db, name)
#
#     if habit_id is None:
#         print(f"Habit {name} has not yet added any completion dates.")
#     else:
#         dates = get_date_list(db, habit_id)
#
#         longest_streak = 1
#         current_reviewed_streak = 1
#
#         for i in range(1, len(dates)):
#             if dates[i] == dates[i - 1] - timedelta(days=1):
#                 current_reviewed_streak += 1
#             elif dates[i] == dates[i - 1]:
#                 continue
#             else:
#                 longest_streak = max(longest_streak, current_reviewed_streak)
#                 current_reviewed_streak = 1
#
#         longest_streak = max(current_reviewed_streak, longest_streak)
#         return longest_streak
#
#
# def calculate_current_streak(db, name, habit_id=None):
#     """Calculate the current streak of the habit, if there is a completion date with today's date."""
#
#     habit_id = get_primary_key(db, name)
#
#     today = date.today()
#
#     if habit_id is None:
#         print(f"Habit {name} has not yet added any completion dates.")
#     else:
#         dates = get_date_list(db, habit_id)
#
#         current_streak = 0
#
#         if dates[0] == today:
#             current_streak += 1
#             for i in range(1, len(dates)):
#                 if dates[i] == dates[i - 1] - timedelta(days=1):
#                     current_streak += 1
#                 elif dates[i] == dates[i - 1]:
#                     continue
#                 else:
#                     break
#         else:
#             current_streak = 0
#
#         return current_streak
#
#
# def calculate_longest_streak_weekly(db, name, start_date, habit_id=None):
#     """Calculate the longest streak by comparing current streak to the longest streak."""
#
#     habit_id = get_primary_key(db, name)
#
#     if habit_id is None:
#         print(f"Habit {name} has not yet added any completion dates.")
#
#     else:
#         dates = get_date_list(db, habit_id)
#
#         start_date = datetime.strptime(start_date, "%Y-%m-%d")
#         day_of_week = start_date.weekday()
#
#         filtered_list = list(filter(lambda x: (x.weekday() == day_of_week), dates))
#
#         current_reviewed_streak = 1
#         longest_streak = 1
#
#         for i in (range(1, len(filtered_list))):
#             if filtered_list[i] == filtered_list[i - 1] - timedelta(weeks=1):
#                 current_reviewed_streak += 1
#                 longest_streak = max(longest_streak, current_reviewed_streak)
#             else:
#                 current_reviewed_streak = 1
#
#         longest_streak = max(longest_streak, current_reviewed_streak)
#         return longest_streak
#
#
# def calculate_current_streak_weekly(db, name, start_date, habit_id=None):
#     """Calculate the longest streak by comparing current streak to the longest streak."""
#
#     habit_id = get_primary_key(db, name)
#
#     today = date.today()
#
#     if habit_id is None:
#         print(f"Habit {name} has not yet added any completion dates.")
#
#     else:
#         dates = get_date_list(db, habit_id)
#
#         start_date = datetime.strptime(start_date, "%Y-%m-%d")
#         day_of_week = start_date.weekday()
#
#         filtered_list = list(filter(lambda x: (x.weekday() == day_of_week), dates))
#
#         current_streak = 1
#
#         if filtered_list[0] >= today - timedelta(weeks=1):
#             for i in (range(1, len(filtered_list))):
#                 if filtered_list[i] == filtered_list[i - 1] - timedelta(weeks=1):
#                     current_streak += 1
#                 else:
#                     break
#         else:
#             current_streak = 0
#
#         return current_streak

