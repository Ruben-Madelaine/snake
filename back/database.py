# save scoress
# game name, save layer, nodes, weights

import sqlite3

from prettytable import from_db_cursor


def get_connection(db_name):
    con = sqlite3.connect(db_name)
    con.row_factory = sqlite3.Row
    return con


# ----------------------- Scores ---------------------------


def create_table(con):
    sql_create_scores_table = """
        CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        size integer, age integer, scores real, details Text,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);
    """
    with con:
        con.execute(sql_create_scores_table)


def insert_rows(con, rows):
    sql_insert_primes = """
        INSERT INTO scores 
            (size, age, scores, details) 
        VALUES
            (?, ?, ?, ?);
    """
    with con:
        try:
            con.executemany(sql_insert_primes, rows)
        except sqlite3.IntegrityError:
            return "Line already exists."

    rows = get_all(con)


def get_all(con):
    sql_select_all = """
        SELECT * FROM scores
        ORDER by size desc, age desc, scores desc
        limit 10;
    """
    return con.execute(sql_select_all)


# ----------------------- Networks ---------------------------


def create_networks_table(con):
    # sql_create_networks_table = """
    #     ALTER TABLE networks
    #     ADD COLUMN generation_id integer;
    # """
    # with con:
    #     con.execute(sql_create_networks_table)
    sql_create_networks_table = """
        CREATE TABLE IF NOT EXISTS networks (
            id INTEGER PRIMARY KEY AUTOINCREMENT, score real,
            generation_id integer, duration TEXT,
            input_nodes integer, hidden_nodes integer, 
            output_nodes integer, hidden_layers integer, 
            wheights_info Text, Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);
    """
    with con:
        con.execute(sql_create_networks_table)


def insert_networks_rows(con, rows):
    sql_insert_networks = """
        INSERT INTO networks 
            (score, generation_id, duration, input_nodes, hidden_nodes, output_nodes, hidden_layers, wheights_info) 
        VALUES
            (?, ?, ?, ?, ?, ?, ?, ?);
    """
    with con:
        try:
            con.executemany(sql_insert_networks, rows)
        except sqlite3.IntegrityError:
            return "Line already exists."

    rows = get_all_networks(con)


def get_all_networks(con):
    sql_select_all = """
        SELECT id, score,
        generation_id, duration,
        input_nodes, hidden_nodes, 
        output_nodes, hidden_layers, 
        Timestamp
        FROM networks
        ORDER by score desc
        LIMIT 10;
    """
    return con.execute(sql_select_all)


def get_best_network(con):
    sql_select_all = """
        SELECT id, score, 
        input_nodes, hidden_nodes, 
        output_nodes, hidden_layers, 
        wheights_info, Timestamp
        FROM networks
        ORDER by score desc
        LIMIT 1;
    """
    return con.execute(sql_select_all)

def get_latest_network(con):
    sql_select_all = """
        SELECT id, score, 
        input_nodes, hidden_nodes, 
        output_nodes, hidden_layers, 
        wheights_info, Timestamp
        FROM networks
        ORDER by Timestamp desc
        LIMIT 1;
    """
    return con.execute(sql_select_all)


# ----------------------- Test ---------------------------


def print_table(rows):
    table = from_db_cursor(rows)
    print(table)


def test_db_creation():
    con = get_connection(":memory:")
    create_table(con)

    rows = [
        (2, 2, "3.5", "Test 1"),
        (3, 13, "10.3", "Test 2"),
        (5, 3, "22", "Test 2"),
    ]
    insert_rows(con, rows)
    rows = get_all(con)
    print_table(rows)

    con.close()


def test_networks_creation():
    con = get_connection(":memory:")
    create_networks_table(con)

    networks = [
        (4, 2, 3, 2, "2, 2 : 0.7103738721235457, 0.8850661600022534, -0.17338400521862019, -0.732893433305073"),
        (4, 2, 3, 2, "2, 2 : 0.7103738721235457, 0.8850661600022534, -0.17338400521862019, -0.732893433305073"),
    ]
    insert_networks_rows(con, networks)
    networks = get_all_networks(con)
    print_table(networks)

    con.close()


if __name__ == "__main__":
    # test_db_creation()
    test_networks_creation()
