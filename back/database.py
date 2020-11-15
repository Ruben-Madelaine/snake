# save scores
# game name, save layer, nodes, weights

import sqlite3

from prettytable import from_db_cursor


def get_connection(db_name):
    con = sqlite3.connect(db_name)
    con.row_factory = sqlite3.Row
    return con


# ----------------------- Score ---------------------------


def create_table(con):
    sql_create_primes_table = """
        CREATE TABLE IF NOT EXISTS score 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
        size integer, age integer, score integer, 
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);
    """
    with con:
        con.execute(sql_create_primes_table)


def insert_rows(con, rows):
    sql_insert_primes = """
        INSERT INTO score 
            (size, age, score) 
        VALUES
            (?, ?, ?);
    """
    with con:
        try:
            con.executemany(sql_insert_primes, rows)
        except sqlite3.IntegrityError:
            return "Line already exists."

    rows = get_all(con)


def get_all(con):
    sql_select_all = """
        SELECT * FROM score
        ORDER by size desc, age desc, score desc
        limit 50;
    """
    return con.execute(sql_select_all)


def print_table(rows):
    table = from_db_cursor(rows)
    print(table)


# ----------------------- Test ---------------------------


def test_db_creation():
    con = get_connection(":memory:")
    create_table(con)

    rows = [
        (2, 2, "3.5"),
        (3, 13, "10.3"),
        (5, 3, "22"),
    ]
    insert_rows(con, rows)
    rows = get_all(con)
    print_table(rows)

    con.close()


if __name__ == "__main__":
    test_db_creation()
