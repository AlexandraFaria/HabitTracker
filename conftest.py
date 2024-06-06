# could I add fixtures here to make the tests more efficient?
# could I add the dates here as well?
from habit import Habit
import pytest
from db import get_db


@pytest.fixture
def db():
    db = get_db("test.db")
    return db


@pytest.fixture
def habit1():
    habit1 = Habit(name="Meditation", description="Improve mindfulness and presence.",
                   frequency="Daily", start_date="2024-04-30")
    return habit1


@pytest.fixture
def habit2():
    habit2 = Habit(name="Python", description="Improve job performance.",
                   frequency="Daily", start_date="2024-04-30")
    return habit2


@pytest.fixture
def habit3():
    habit3 = Habit(name="Morning walk", description="Increase wakefulness and improve quality of sleep.",
                   frequency="Daily", start_date="2024-04-30")
    return habit3


@pytest.fixture
def habit4():
    habit4 = Habit(name="Swimming", description="Improve cardio fitness.",
                   frequency="Weekly", start_date="2024-05-01")
    return habit4


@pytest.fixture
def habit5():
    habit5 = Habit(name="Water plants", description="Keep plants healthy.",
                   frequency="Weekly", start_date="2024-05-01")
    return habit5


@pytest.fixture
def habit1dates():
    habit1dates = [
            "2024-05-01 08:00", "2024-05-02 09:15", "2024-05-03 10:30", "2024-05-04 11:45", "2024-05-05 12:00",
            "2024-05-06 13:15", "2024-05-07 14:30", "2024-05-08 15:45", "2024-05-09 16:00", "2024-05-10 17:15",
            "2024-05-12 19:45", "2024-05-13 20:00", "2024-05-14 21:15", "2024-05-15 06:30", "2024-05-16 07:45",
            "2024-05-17 08:00", "2024-05-18 09:15", "2024-05-19 10:30", "2024-05-20 11:45", "2024-05-21 12:00",
            "2024-05-22 13:15", "2024-05-23 14:30"
        ]
    return habit1dates


@pytest.fixture
def habit2dates():
    habit2dates = [
            "2024-05-01 07:00", "2024-05-02 08:30", "2024-05-03 09:45", "2024-05-04 11:00", "2024-05-05 12:15",
            "2024-05-06 13:30", "2024-05-07 14:45", "2024-05-08 16:00", "2024-05-09 17:15", "2024-05-10 18:30",
            "2024-05-12 21:00", "2024-05-13 06:15", "2024-05-14 07:30", "2024-05-15 08:45", "2024-05-16 10:00",
            "2024-05-17 11:15", "2024-05-18 12:30", "2024-05-19 13:45", "2024-05-20 15:00", "2024-05-21 16:15",
            "2024-05-22 17:30", "2024-05-23 18:45", "2024-05-24 20:00", "2024-05-25 21:15"
        ]
    return habit2dates


@pytest.fixture
def habit3dates():
    habit3dates = [
            "2024-05-01 06:00", "2024-05-02 07:15", "2024-05-03 08:30", "2024-05-04 09:45", "2024-05-05 06:00",
            "2024-05-06 07:15", "2024-05-07 08:30", "2024-05-08 09:45", "2024-05-09 06:00", "2024-05-10 07:15",
            "2024-05-11 08:30", "2024-05-12 09:45", "2024-05-13 06:00", "2024-05-15 08:30", "2024-05-16 09:45",
            "2024-05-17 06:00", "2024-05-18 07:15", "2024-05-19 08:30", "2024-05-20 09:45", "2024-05-21 06:00",
            "2024-05-22 07:15", "2024-05-23 08:30", "2024-05-24 09:45", "2024-05-25 06:00", "2024-05-26 07:15",
        ]
    return habit3dates

# add in weekly dates for habit 4 and habit 5.

@pytest.fixture
def habit4dates():
    habit4dates = [
            "2024-05-01 06:00", "2024-05-08 07:15", "2024-05-15 08:30", "2024-05-22 09:45", "2024-05-21 06:00",
            "2024-05-29 07:15"
        ]
    return habit4dates

@pytest.fixture
def habit5dates():
    habit5dates = [
            "2024-05-01 06:00", "2024-05-08 07:15", "2024-05-15 08:30", "2024-05-22 09:45", "2024-05-21 06:00",
            "2024-05-30 07:15", "2024-06-05 08:30"
        ]
    return habit5dates