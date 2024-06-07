import pytest
from habit import Habit
from db import get_primary_key, delete_habit
from analyse import get_longest_streak, get_current_streak, monthly_habit_completion, max_longest_streak
import os


def setup_method():
    pass


def test_save_habit(habit1, habit2, habit3, habit4, habit5, db):
    habit1.save_habit()
    habit2.save_habit()
    habit3.save_habit()
    habit4.save_habit()
    habit5.save_habit()
    db.commit()


def test_data_storage(db, habit1, habit2, habit3, habit4, habit5):
    cur = db.cursor()
    cur.execute("SELECT name FROM habit_metadata")
    result = cur.fetchall()
    assert result == [("Meditation",), ("Python",), ("Morning walk",), ("Swimming",), ("Water plants",)]


def test_add_habit_completion_date(db, habit1dates, habit2dates, habit3dates, habit4dates,
                                   habit5dates, habit1, habit2, habit3, habit4, habit5):
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
    assert get_primary_key(db, "Meditation") == 1


def test_calculate_longest_streak_daily(db, habit2, habit1, habit3):
    """Test the calculation of the longest streak for daily habits."""
    longest_streak_1 = get_longest_streak(db, habit1.name)
    longest_streak_2 = get_longest_streak(db, habit2.name)
    longest_streak_3 = get_longest_streak(db, habit3.name)
    assert longest_streak_1 == "12 days"
    assert longest_streak_2 == "14 days"
    assert longest_streak_3 == "13 days"


def test_calculate_longest_streak_weekly(db, habit4, habit5):
    """Test the calculation of the longest streak for weekly habits."""
    longest_streak_4 = get_longest_streak(db, habit4.name)
    longest_streak_5 = get_longest_streak(db, habit5.name)
    assert longest_streak_4 == "5 weeks"
    assert longest_streak_5 == "4 weeks"


def test_calculate_current_streak_daily(db, habit1, habit2, habit3):
    current_streak_1 = get_current_streak(db, habit1.name)
    current_streak_2 = get_current_streak(db, habit2.name)
    current_streak_3 = get_current_streak(db, habit3.name)
    assert current_streak_1 == "1 days"
    assert current_streak_2 == "1 days"
    assert current_streak_3 == "0 days"

# Need to determine a way to test the current streak for weekly habits,
# where a day can be added within the last week of testing on the day of the week that counts towards the streak.


def test_max_longest_streak(db, capsys):
    max_longest_streak(db)
    captured = capsys.readouterr()
    assert "Python with 14 days", "Swimming with 5 weeks" in captured.out


def test_monthly_habit_completion(db, capsys):
    """Test monthly habit check-offs by counting the number of dates in the database for each habit.
    The number of dates should be equal to the number of completions for each habit.

    The captured output is reviewed to see if certain portions of the string output are present using
    capsys.readouterr().

    parameters:
        db: database connection
        caps: CaptureFixture object
    """
    monthly_habit_completion(db, 5)
    captured = capsys.readouterr()
    assert "Meditation: 22" in captured.out
    assert "Swimming: 6" in captured.out
    assert "Morning walk: 25" in captured.out
    assert "Water plants: 6" in captured.out
    assert "Python: 24" in captured.out


# def test_habit_deletion(db, habit1, habit2, habit3, habit4, habit5):
#     list_of_habits = [habit1, habit2, habit3, habit4, habit5]
#     for habit in list_of_habits:
#         delete_habit(db, habit.name)
#     cur = db.cursor()
#     cur.execute("SELECT name FROM habit_metadata")
#     result = cur.fetchall()
#     assert result == []
#
#
# def teardown_method():
#     os.remove("test.db")

# teardown_method is not working properly, the test.db is still in the directory after the test is run,
# however it is empty and able to run tests again successfully.
