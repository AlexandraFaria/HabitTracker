from habit import Habit
from operator import attrgetter
from analyse import calculate_longest_streak, calculate_current_streak
from db import get_db, create_tables, add_habit, get_primary_key, search_habit, add_habit_completion, get_date_list


if __name__ == "__main__":

    meditation = Habit("Meditation", "Meditate for 10 minutes", "Daily", "2024-05-01")
    meditation.save_habit()
    print(meditation.habit_id)
    meditation.add_habit_completion_date()
    meditation.add_habit_completion_date("2024-05-01 06:00")
    meditation.add_habit_completion_date("2024-05-02 07:15")
    meditation.add_habit_completion_date("2024-05-06 07:15")
    meditation.add_habit_completion_date("2024-05-07 08:30")
    meditation.add_habit_completion_date("2024-05-08 09:45")
    meditation.add_habit_completion_date("2024-05-09 06:00")
    meditation.add_habit_completion_date("2024-05-10 07:15")
    meditation.get_longest_streak()
    swimming = Habit("Swimming", "Swim for 30 minutes", "Daily", "2024-05-01")
    swimming.save_habit()
    print(swimming.habit_id)
    swimming.add_habit_completion_date()
    swimming.add_habit_completion_date("2024-05-31 06:00")
    swimming.add_habit_completion_date("2024-05-30 06:00")
    swimming.add_habit_completion_date("2024-05-29 06:00")
    swimming.add_habit_completion_date("2024-05-01 06:00")
    swimming.add_habit_completion_date("2024-05-01 12:00")
    swimming.add_habit_completion_date("2024-05-02 07:15")
    swimming.add_habit_completion_date("2024-05-06 07:15")
    swimming.add_habit_completion_date("2024-05-07 08:30")
    swimming.add_habit_completion_date("2024-05-08 09:45")
    swimming.get_longest_streak()
    swimming.get_current_streak()
    meditation.get_current_streak()
    plants = Habit("Water plants", "Water plants", "Weekly", "2024-05-01")
    plants.save_habit()
    print(plants.habit_id)
    plants.add_habit_completion_date()
    plants.add_habit_completion_date("2024-05-08 06:00")
    plants.add_habit_completion_date("2024-05-15 06:00")
    plants.add_habit_completion_date("2024-05-22 06:00")
    plants.add_habit_completion_date("2024-05-23 06:00")
    plants.add_habit_completion_date("2024-05-28 06:00")
    plants.add_habit_completion_date("2024-05-29 06:00")
    plants.get_longest_streak()
    plants.get_current_streak()
    soccer = Habit("Soccer", "Play soccer", "Weekly", "2024-05-01")
    soccer.save_habit()
    print(soccer.habit_id)
    soccer.add_habit_completion_date()
    soccer.add_habit_completion_date("2024-05-08 06:00")
    soccer.add_habit_completion_date("2024-05-15 06:00")
    soccer.add_habit_completion_date("2024-05-22 06:00")
    print(Habit.habits)
    soccer.delete_habit()
    print(Habit.habits)

    # print(f"Plants current streak should be 4:{plants.current_streak}")
    # print(f"{plants.longest_streak} longest streak should be 4")
    # print(f"{meditation.current_streak} should be 1")
    # print(f"{swimming.current_streak} should be 1")
    # print(Habit.max_longest_streak())
    # Habit.monthly_habit_completion(5)