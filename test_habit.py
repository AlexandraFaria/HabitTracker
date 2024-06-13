"""This module contains tests for the functions associated with the Habit Class, db, and analyse module."""

import pytest
import os
from habit import Habit
from db import get_primary_key, delete_habit
from analyse import get_longest_streak, get_current_streak, monthly_habit_completion, max_longest_streak


def test_save_habit(habit1, habit2, habit3, habit4, habit5, db):
    """Saves all 5 predefined habits to the database.

      parameters:
        fixtures that are defined in the conftest.py file
    """
    habit1.save_habit()
    habit2.save_habit()
    habit3.save_habit()
    habit4.save_habit()
    habit5.save_habit()
    db.commit()


def test_data_storage(db, habit1, habit2, habit3, habit4, habit5):
    """Test the data storage of the habits in the database.
    Test asserts that the list of names in the database is equal to the list of names of the habits entered.

    parameters:
        fixtures that are defined in the conftest.py file
    """
    cur = db.cursor()
    cur.execute("SELECT name FROM habit_metadata")
    result = cur.fetchall()
    assert result == [("Meditation",), ("Python",), ("Morning walk",), ("Swimming",), ("Water plants",)]


def test_add_habit_completion_date(db, habit1dates, habit2dates, habit3dates, habit4dates,
                                   habit5dates, habit1, habit2, habit3, habit4, habit5):
    """Test function used to save all the dates for each habit in the database.
     Data used in following test functions to calculate the longest streaks, max streak,
     current streaks, and monthly habit completions.

    parameters:
        fixtures that are defined in the conftest.py file

    """
    for check_off in habit1dates:
        habit1.add_habit_completion_date(check_off)
    for check_off in habit2dates:
        habit2.add_habit_completion_date(check_off)
    for check_off in habit3dates:
        habit3.add_habit_completion_date(check_off)
    for check_off in habit4dates:
        habit4.add_habit_completion_date(check_off)
    for check_off in habit5dates:
        habit5.add_habit_completion_date(check_off)
    habit1.add_habit_completion_date()
    habit2.add_habit_completion_date()


def test_get_primary_key(db, habit1):
    """Test the get_primary_key function.
    The function should return the primary key of the habit in the database.

    parameters:
        fixtures that are defined in the conftest.py file
    """
    assert get_primary_key(db, "Meditation") == 1


def test_calculate_longest_streak_daily(db, habit2, habit1, habit3):
    """Test the calculation of the longest streak for each daily habit.
    The longest streak is calculated by the longest streak of consecutive days.

    parameters:
        fixtures that are defined in the conftest.py file

    """
    longest_streak_1 = get_longest_streak(db, habit1.name)
    longest_streak_2 = get_longest_streak(db, habit2.name)
    longest_streak_3 = get_longest_streak(db, habit3.name)
    assert longest_streak_1 == "12 days"
    assert longest_streak_2 == "14 days"
    assert longest_streak_3 == "13 days"


def test_calculate_longest_streak_weekly(db, habit4, habit5):
    """Test the calculation of the longest streak for each weekly habit.
    The longest streak is calculated by the longest streak of consecutive weeks, where the habit was completed on the
    same weekday as the start_date.

    (e.g. if the start_date is a Monday, the habit must be completed on a Monday to
    count toward the longest streak)

    parameters:
        fixtures that are defined in the conftest.py file
    """
    longest_streak_4 = get_longest_streak(db, habit4.name)
    longest_streak_5 = get_longest_streak(db, habit5.name)
    assert longest_streak_4 == "5 weeks"
    assert longest_streak_5 == "4 weeks"


def test_calculate_current_streak_daily(db, habit1, habit2, habit3):
    """
    Test the calculation of the current streak for each daily habit.
    Note: In the function test_add_habit_completion_date, a completion date is added with "Today's date" for habit1
    and habit2 for testing purposes.

    The current streak is only calculated if the most recent date in the database is equal to today's date.

    Test asserts that there is only a current streak for habit1 and habit2, as habit3 does not have a current streak.

    parameters:
        fixtures that are defined in the conftest.py file
    """
    current_streak_1 = get_current_streak(db, habit1.name)
    current_streak_2 = get_current_streak(db, habit2.name)
    current_streak_3 = get_current_streak(db, habit3.name)
    assert current_streak_1 == "1 days"
    assert current_streak_2 == "1 days"
    assert current_streak_3 == "0 days"


# Need to determine a way to test the current streak for weekly habits,
# where a day can be added within the last week of testing on the day of the week that counts towards the streak.


def test_max_longest_streak(db, capsys):
    """Test the max_longest_streak function.

    The function should return a string including the two habits with the longest streak for each periodicity
    (daily and weekly) with their associated streak length.

    parameters:
        db: database connection fixture in conftest.py
        capsys: CaptureFixture which captures the text output of the function max_longest_streak

    """

    max_longest_streak(db)
    captured = capsys.readouterr()
    assert "Python with 14 days", "Swimming with 5 weeks" in captured.out


def test_monthly_habit_completion(db, capsys):
    """Test monthly habit check-offs by counting the number of dates in the database for each habit in a given
    month. (Function is set to count the number of dates in May 2024)

    The number of dates should be equal to the number of completions for each habit in May 2024.

    The captured output is reviewed to see if certain portions of the string output are present using
    capsys.readouterr().

    parameters:
        db: database connection
        capsys: CaptureFixture which captures the text output of the function monthly_habit_completion(db, 5)
    """
    monthly_habit_completion(db, 5)
    captured = capsys.readouterr()
    assert "Meditation: 22" in captured.out
    assert "Swimming: 6" in captured.out
    assert "Morning walk: 25" in captured.out
    assert "Water plants: 6" in captured.out
    assert "Python: 24" in captured.out


@pytest.mark.skip(reason="Comment out if you would like to run Pytest more than once to delete ALL data after running.")
# This test is skipped so the user can use the test.db file to run the main.py CLI program to see full functionality.
def test_habit_deletion(db, habit1, habit2, habit3, habit4, habit5):
    """Test the deletion of habits from the database.

    parameters:
        fixtures that are defined in the conftest.py file
    """
    list_of_habits = [habit1, habit2, habit3, habit4, habit5]
    for habit in list_of_habits:
        delete_habit(db, habit.name)
    cur = db.cursor()
    cur.execute("SELECT name FROM habit_metadata")
    result = cur.fetchall()
    assert result == []


@pytest.mark.skip(reason="Comment out if you would like to run Pytest more than once to delete ALL data after running.")
# This test is skipped so the user can use the test.db file to run the main.py CLI program to see full functionality.
def teardown_method():
    """Delete the test.db file after the tests are run."""
    os.remove("test.db")

# teardown_method is not working properly, the test.db is still in the directory after the test is run,
# however it is empty and able to run tests again successfully.
