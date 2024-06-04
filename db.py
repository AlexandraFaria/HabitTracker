import sqlite3
from datetime import date, datetime, timedelta


def get_db(name="main.db"):
    """Create a connection to the database and return it.
       While creating the connection, also create database tables.


    parameters:
       name(str): Name of the database to connect to. Default is main.db."""

    db = sqlite3.connect(name)
    create_tables(db)
    return db


def create_tables(db):
    """Create the tables in the database if they do not exist.


    parameters:
       db: Database connection.
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
       description(str): Description of the habit.
       frequency(str): Periodicity habit should be done.
       start_date(date): Date the habit was started.
    """

    cur = db.cursor()
    cur.execute("INSERT INTO habit_metadata VALUES (null,?,?,?,?)", (name, description, frequency, start_date))
    db.commit()


def get_primary_key(db, name):
    """Get the primary key of the habit from the parent table habit_metadata


    parameters:
       db: Database connection.
       name(str): Name of the habit.
    """

    cur = db.cursor()
    result = cur.execute("""SELECT habit_id FROM habit_metadata WHERE name = ?""", (name,))
    return result.fetchone()[0]


def add_habit_completion(db, habit_id, completion_date=None):
    """Add a completion date to the habit_completion_dates table with the associated habit_id.


    parameters:
       db: Database connection.
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
       db: Database connection.
       name(str): Name of the habit to search for.
    """

    cur = db.cursor()
    try:
        result = cur.execute("""SELECT * FROM habit_metadata WHERE name = ?""", (name,))
        return result.fetchone()[1]
    except TypeError:
        return None


# def list_of_habits(db):
#     """Search for a habit in the habit_metadata table.
#         This function provides the ability to search for a habit by name, to ensure the habit is not
#         duplicated in the database.
#
#     parameters:
#         db: Database connection.
#         name(str): Name of the habit to search for.
#     """
#
#     cur = db.cursor()
#     try:
#         result = cur.execute("""SELECT name FROM habit_metadata""")
#         return result.fetchall()
#     except TypeError:
#         return None


def get_date_list(db, habit_id):
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


def delete_habit(db, habit_id=None, name=None):
    habit_id = get_primary_key(db, name)
    cur = db.cursor()
    cur.execute("DELETE FROM habit_completion_dates WHERE habit_id = ?", (habit_id,))
    cur.execute("DELETE FROM habit_metadata WHERE habit_id = ?", (habit_id,))
    db.commit()


def reset_habit(db, habit_id=None, start_date=None):
    cur = db.cursor()
    cur.execute("DELETE FROM habit_completion_dates WHERE habit_id = ?", (habit_id,))
    cur.execute("UPDATE habit_metadata SET start_date = ? WHERE habit_id = ?", (start_date, habit_id))
    db.commit()




# import sqlite3
# from datetime import date, datetime, timedelta
#
#
# def get_db(name="main.db"):
#     """Create a connection to the database and return it.
#         While creating the connection, also create database tables.
#
#     parameters:
#         name(str): Name of the database to connect to. Default is main.db."""
#
#     db = sqlite3.connect(name)
#     create_tables(db)
#     return db
#
#
# def create_tables(db):
#     """Create the tables in the database if they do not exist.
#
#     parameters:
#         db: Database connection.
#     """
#
#     cur = db.cursor()
#
#     cur.execute("""CREATE TABLE IF NOT EXISTS habit_metadata (
#         habit_id INTEGER PRIMARY KEY,
#         name TEXT,
#         description TEXT,
#         frequency TEXT,
#         start_date TEXT
#         )""")
#
#     cur.execute("""CREATE TABLE IF NOT EXISTS habit_completion_dates (
#         tracker_id INTEGER PRIMARY KEY,
#         completion_date TEXT,
#         habit_id INT,
#         FOREIGN KEY (habit_id) REFERENCES habit_metadata(habit_id)
#     )""")
#
#     db.commit()
#
#
# def add_habit(db, name, description, frequency, start_date):
#     """Add a habit to the database.
#
#     parameters:
#         db: Database connection.
#         name(str): Name of the habit.
#         description(str): Description of the habit.
#         frequency(str): Periodicity habit should be done.
#         start_date(date): Date the habit was started.
#     """
#
#     cur = db.cursor()
#     cur.execute("INSERT INTO habit_metadata VALUES (null,?,?,?,?)", (name, description, frequency, start_date))
#     db.commit()
#
#
# def get_primary_key(db, name):
#     """Get the primary key of the habit from the parent table habit_metadata
#
#     parameters:
#         db: Database connection.
#         name(str): Name of the habit.
#     """
#
#     cur = db.cursor()
#     result = cur.execute("""SELECT habit_id FROM habit_metadata WHERE name = ?""", (name,))
#     return result.fetchone()[0]
#
#
# def add_habit_completion(db, habit_id, completion_date):
#     """Add a completion date to the habit_completion_dates table with the associated habit_id.
#
#     parameters:
#         db: Database connection.
#         habit_id(int): Primary key of the habit to be used as the foreign key.
#         completion_date(str): Date the habit was completed. Default is the current date.
#     """
#
#     cur = db.cursor()
#     # if completion_date is None:
#     #     from datetime import datetime
#     #     completion_date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M")
#     cur.execute("INSERT INTO habit_completion_dates VALUES (null,?,?)", (completion_date, habit_id))
#     db.commit()
#
#
# def search_habit(db, name):
#     """Search for a habit in the habit_metadata table.
#         This function provides the ability to search for a habit by name, to ensure the habit is not
#         duplicated in the database.
#
#     parameters:
#         db: Database connection.
#         name(str): Name of the habit to search for.
#     """
#
#     cur = db.cursor()
#     try:
#         result = cur.execute("""SELECT * FROM habit_metadata WHERE name = ?""", (name,))
#         return result.fetchone()[1]
#     except TypeError:
#         return None
#
#
# def get_date_list(db, habit_id):
#     cur = db.cursor()
#     result = cur.execute("""SELECT habit_id, completion_date FROM habit_completion_dates WHERE habit_id = ?""",
#                          (habit_id,))
#     date_list = result.fetchall()
#
#     dates = []
#     for day in date_list:
#         day = datetime.strptime(day[1], "%Y-%m-%d %H:%M").date()
#         dates.append(day)
#     dates.sort(reverse=True)
#     return dates
#
#
# def delete_habit(db, habit_id=None, name=None):
#     habit_id = get_primary_key(db, name)
#     cur = db.cursor()
#     cur.execute("DELETE FROM habit_completion_dates WHERE habit_id = ?", (habit_id,))
#     cur.execute("DELETE FROM habit_metadata WHERE habit_id = ?", (habit_id,))
#     db.commit()
#
#
# def reset_habit(db, habit_id=None, start_date=None):
#     cur = db.cursor()
#     cur.execute("DELETE FROM habit_completion_dates WHERE habit_id = ?", (habit_id,))
#     cur.execute("UPDATE habit_metadata SET start_date = ? WHERE habit_id = ?", (start_date, habit_id))
#     db.commit()
#
# # def drop_database(db):
# #     cur = db.cursor()
# #     cur.execute("DROP TABLE habit_metadata")
# #     cur.execute("DROP TABLE habit_completion_dates")
# #     db.commit()
# #     db.close()
# #     return db
#
# # def list_of_habits(db):
# #     """Search for a habit in the habit_metadata table.
# #         This function provides the ability to search for a habit by name, to ensure the habit is not
# #         duplicated in the database.
# #
# #     parameters:
# #         db: Database connection.
# #         name(str): Name of the habit to search for.
# #     """
# #
# #     cur = db.cursor()
# #     try:
# #         result = cur.execute("""SELECT name FROM habit_metadata""")
# #         return result.fetchall()
# #     except TypeError:
# #         return None
