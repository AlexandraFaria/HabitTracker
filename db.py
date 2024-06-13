"""This module contains functions to analyze the data in the database."""

from datetime import datetime
import sqlite3


def get_db(name="main.db"):
    """Create a connection to the database and return it.
       While creating the connection, also create database tables.


    parameter:
       name(str): Name of the database to connect to. Default argument is main.db."""

    db = sqlite3.connect(name)
    create_tables(db)
    return db


def create_tables(db):
    """Create the tables in the database if they do not exist.

    :parameter:
       db: Database connection from the get_db function.
    """

    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS habit_metadata (
        habit_id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        frequency TEXT,
        start_date TEXT
        )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS habit_completion_dates (
        tracker_id INTEGER PRIMARY KEY,
        completion_date TEXT,
        habit_id INT,
        FOREIGN KEY (habit_id) REFERENCES habit_metadata(habit_id)
    )""")

    db.commit()


def add_habit(db, name, description, frequency, start_date):
    """Add a habit to the database.

    parameters:
       db: Database connection.
       name(str): Name of the habit.
       description(str): Description of the habit/ purpose for habit creation.
       frequency(str): Periodicity habit should be done (Daily or Weekly).
       start_date(date): Date the habit was started.
    """

    cur = db.cursor()
    cur.execute("INSERT INTO habit_metadata VALUES (null,?,?,?,?)", (name, description, frequency, start_date))
    db.commit()


def get_primary_key(db, name):
    """Get the primary key of the habit from the parent table habit_metadata searching by name.

    parameters:
       db: Database connection from the get_db function.
       name(str): Name of the habit.
    """

    cur = db.cursor()
    result = cur.execute("""SELECT habit_id FROM habit_metadata WHERE name = ?""", (name,))
    return result.fetchone()[0]


def add_habit_completion(db, habit_id, completion_date=None):
    """Add a completion date to the habit_completion_dates table with the associated habit_id.

    parameters:
       db: Database connection from the get_db function.
       habit_id(int): Primary key of the habit to be used as the foreign key.
       completion_date(str): Date the habit was completed. Default is the current date.
    """

    cur = db.cursor()
    if completion_date is None:
        from datetime import datetime
        completion_date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M")
    cur.execute("INSERT INTO habit_completion_dates VALUES (null,?,?)", (completion_date, habit_id))
    db.commit()


def search_habit(db, name):
    """Search for a habit in the habit_metadata table.
       This function provides the ability to search for a habit by name, to ensure the habit is not
       duplicated in the database.

    parameters:
       db: Database connection from the get_db function.
       name(str): Name of the habit to search for.
    """

    cur = db.cursor()
    try:
        result = cur.execute("""SELECT * FROM habit_metadata WHERE name = ?""", (name,))
        return result.fetchone()[1]
    except TypeError:
        return None


def search_start_date(db, name):
    """Search for a habit in the habit_metadata table by name and return the start date.

    parameters:
       db: Database connection from the get_db function.
       name(str): Name of the habit to search for.

    return:
        start_date(str): Start date of the habit.
    """

    cur = db.cursor()
    try:
        result = cur.execute("""SELECT * FROM habit_metadata WHERE name = ?""", (name,))
        return result.fetchone()[4]
    except TypeError:
        return None


def list_of_habits(db):
    """Creates a list of names of all habits in the database.

    parameters:
        db: Database connection from the get_db function.

    returns:
        result.fetchall(): List of habits in the habit_metadata table.

    """

    cur = db.cursor()
    try:
        result = cur.execute("""SELECT name FROM habit_metadata""")
        return result.fetchall()
    except TypeError:
        return None


def list_of_habits_daily(db):
    """Provides a list of habits with the frequency daily.

    parameters:
        db: Database connection from the get_db function.
    """

    cur = db.cursor()
    try:
        result = cur.execute("""SELECT name FROM habit_metadata WHERE frequency = "Daily" """)
        return result.fetchall()
    except TypeError:
        return None


def list_of_habits_weekly(db):
    """Provides a list of habits with the frequency weekly.

    parameters:
        db: Database connection from the get_db function.
    """

    cur = db.cursor()
    try:
        result = cur.execute("""SELECT name FROM habit_metadata WHERE frequency = "Weekly" """)
        return result.fetchall()
    except TypeError:
        return None


def get_date_list(db, habit_id):
    """Get a list of completion dates for a habit based on habit_id.

    parameters:
        db: Database connection from the get_db function.
        habit_id(int): Primary key of the habit.
    """
    cur = db.cursor()
    result = cur.execute("""SELECT habit_id, completion_date FROM habit_completion_dates WHERE habit_id = ?""",
                         (habit_id,))
    date_list = result.fetchall()

    dates = []
    for day in date_list:
        day = datetime.strptime(day[1], "%Y-%m-%d %H:%M").date()
        dates.append(day)
    dates.sort(reverse=True)
    return dates


def delete_habit(db, name):
    """Deletes habit from the habit_metadata table and all dates from the
    habit_completion_dates table by first searching for the habit_id through the get_primary_key
    function, and using this argument for cascade deletion.

    parameters:
        db: Database connection from the get_db function.
        name(str): Name of the habit used to search for habit_id to be deleted.
    """
    cur = db.cursor()
    habit_id = get_primary_key(db, name)
    cur.execute("DELETE FROM habit_completion_dates WHERE habit_id = ?", (habit_id,))
    cur.execute("DELETE FROM habit_metadata WHERE habit_id = ?", (habit_id,))
    db.commit()


def reset_habit(db, name, start_date=None):
    """This function searches for the habit_id using the name as an argument in the get_primary_key function.
    The corresponding dates associated with this habit_id are deleted from the habit_completion_dates table.
    The associated start_date is changed to the date provided in the start_date parameter.

    parameters:
        db: Database connection from the get_db function.
        name(str): Name of the habit used to search for habit_id
        start_date(str): Date the habit is reset to.
   """
    cur = db.cursor()
    habit_id = get_primary_key(db, name)
    cur.execute("DELETE FROM habit_completion_dates WHERE habit_id = ?", (habit_id,))
    cur.execute("UPDATE habit_metadata SET start_date = ? WHERE habit_id = ?", (start_date, habit_id))
    db.commit()
