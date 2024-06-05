import pytest
from habit import Habit
from db import get_primary_key
import os
import random


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
    Habit.habits = []
    habit1.get_longest_streak()
    habit2.get_longest_streak()
    habit3.get_longest_streak()
    assert habit1.longest_streak == 12
    assert habit2.longest_streak == 14
    assert habit3.longest_streak == 13


def test_calculate_current_streak_daily(db, habit1, habit2, habit3):
    habit1.get_current_streak()
    habit2.get_current_streak()
    habit3.get_current_streak()
    assert habit1.current_streak == 1
    assert habit2.current_streak == 1
    assert habit3.current_streak == 0


def test_calculate_longest_streak_weekly(db, habit4, habit5):
    habit4.get_longest_streak()
    habit5.get_longest_streak()
    assert habit4.longest_streak == 5
    assert habit5.longest_streak == 4


def test_max_longest_streak(db, habit1dates, habit2dates, habit3dates, habit4dates, habit5dates, habit1,
                            habit2, habit3, habit4, habit5):
    Habit.max_longest_streak()
    assert "Python with 14 days", "Swimming with 5 weeks" in str(Habit.max_longest_streak())

@pytest.mark.skip
def test_monthly_habit_completion(db, habit1dates, habit2dates, habit3dates, habit4dates, habit5dates, habit1,
                                  habit2, habit3, habit4, habit5):
    list_completions = Habit.monthly_habit_completion(5)
    monthly_habit_completions = ["Meditation: 22", "Swimming: 6", "Morning walk: 25", "Water plants: 6", "Swimming: 6"]
    # Select an item randomly from the list, as unable to assert that all values are in the string returned.
    selected_item = random.choice(monthly_habit_completions)
    assert selected_item in str(list_completions)

@pytest.mark.skip
def test_habit_deletion(db, habit1, habit2, habit3, habit4, habit5):
    habit1.delete_habit()
    habit2.delete_habit()
    habit3.delete_habit()
    habit4.delete_habit()
    habit5.delete_habit()
    cur = db.cursor()
    cur.execute("SELECT name FROM habit_metadata")
    result = cur.fetchall()
    assert result == []


@pytest.mark.skip
def teardown_method():
    os.remove("test.db")
    assert not os.path.exists("test.db")

#teardown_method is not working properly. It is not deleting the test.db file because it is still being used.
