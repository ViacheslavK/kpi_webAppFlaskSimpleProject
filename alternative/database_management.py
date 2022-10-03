import sqlite3
from sqlite3 import Error
from app.tables_management import sql_create_results_table, sql_create_updates_table, sql_create_components_table


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


if __name__ == '__main__':
    conn = create_connection(r"../db/dashboardsSummary.db")

    # create tables
    if conn is not None:
        # create components table
        create_table(conn, sql_create_components_table)
        # create component report updates table
        create_table(conn, sql_create_updates_table)
        # create test run results table
        create_table(conn, sql_create_results_table)
    else:
        print("Error! cannot create the database connection.")

    if conn:
        conn.close()
