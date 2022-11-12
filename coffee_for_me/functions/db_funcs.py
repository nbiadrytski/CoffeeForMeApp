#!/usr/bin/env python3
import sqlite3
import logging

db_name = 'employees.db'
table_name = 'employees'

logger = logging.getLogger('main.argparsing.functions.db_funcs')


def create_connection():
    """
    Creates connection to sqlite3 database.

    Returns:
        sqlite3.Connection: connection to database.

    Raises:
        sqlite3.Error: If error when trying to create connection.
    """
    try:
        conn = sqlite3.connect(db_name)
        logger.debug('created connection to {}'.format(db_name))
        return conn
    except sqlite3.Error as e:
        logger.error('could not create connection... {}'.format(e))
    return None


def create_table():
    """
    Creates sqlite3 database table if it doesn't exist already.

    Raises:
        sqlite3.Error: If error when trying to create db table.
    """
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            'CREATE TABLE IF NOT EXISTS ' + table_name +
            ' (id INTEGER PRIMARY KEY, name text, sales integer, amount integer)')
        conn.commit()
        logger.debug('created {} if not exists already'.format(table_name))
    except sqlite3.Error as e:
        logger.error('could not create table {}... {}'.format(table_name, e))
    finally:
        conn.close()


def is_employee_in_db(name):
    """
    Checks if salesperson is in database by name.
    Pass salesperson's fullname as a parameter when calling the function.

    Parameters:
        name (str): Salesperson's full name.

    Returns:
        bool: True if salesperson is in database, False if not.

    Raises:
        sqlite3.Error: If error when trying to fetch salesperson from table.
    """
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM ' + table_name + ' WHERE name=?', (name,))
        row = cur.fetchall()
        if name in [i[1] for i in row]:
            logger.debug('{} is found in {} table'.format(name, table_name))
            return True
        else:
            logger.debug('{} is not found in {} table'.format(name, table_name))
            return False
    except sqlite3.Error as e:
        logger.error('error when fetching employee from table... {}'.format(e))
    finally:
        conn.close()


def insert_db_record(name, sales, amount):
    """
    Inserts salesperson record into database by name, number of sales and sales amount.
    When calling the function use Salesperson fullname, count_sales(), total_sales_amount() methods correspondingly.

    Parameters:
        name (str): Salesperson's full name.
        sales (int): Salesperson's number of sales. Call Salesperson.count_sales()
        amount (float): Salesperson's sales total amount. Call Salesperson.total_sales_amount()()

    Raises:
        sqlite3.Error: If error when trying to insert salesperson record into table.
    """
    conn = create_connection()
    try:
        cur = conn.cursor()
        # NULL will be replaced by id
        cur.execute('INSERT INTO ' + table_name + ' VALUES (NULL,?,?,?)', (name, sales, amount))
        conn.commit()
        logger.debug('{} was added to {} table'.format(name, table_name))
    except sqlite3.Error as e:
        logger.error('error when inserting employee {} into {} table... {}'.format(name, table_name, e))
    finally:
        conn.close()


def update_db_record(name, sales, amount):
    """
    Updates salesperson record in database by name, number of sales and sales amount.
    When calling the function use Salesperson fullname, count_sales(), total_sales_amount() methods correspondingly.

    Parameters:
        name (str): Salesperson's full name.
        sales (int): Salesperson's number of sales. Call Salesperson.count_sales()
        amount (float): Salesperson's sales total amount. Call Salesperson.total_sales_amount()()

    Raises:
        sqlite3.Error: If error when trying to update salesperson record in table.
    """
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('UPDATE ' + table_name + ' SET amount=?, sales=? WHERE name=?', (amount, sales, name))
        conn.commit()
        logger.debug('{} record was updated in {} table with {} sales and {} amount'.
                     format(name, table_name, sales, amount))
    except sqlite3.Error as e:
        logger.error('error updating {} record in {} table with {} sales and {} amount... {}'.
                     format(name, table_name, sales, amount, e))
    finally:
        conn.close()


def view_db_records():
    """
    Selects all salespeople records from table.

    Returns:
        list: List of all salespeople records from table.

    Raises:
        sqlite3.Error: If error when trying to select salespeople from table.
    """
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM ' + table_name)
        rows = cur.fetchall()
        logger.debug('selected all salespeople records from {} table'.format(table_name))
        return rows
    except sqlite3.Error as e:
        logger.error('Error when viewing employee records in {} table... {}'.format(table_name, e))
    finally:
        conn.close()


def is_table_empty():
    """
    Checks if there are any salespeople records in database.
    Pass salesperson's fullname as a parameter when calling the function.

    Returns:
        bool: True if there are any salespeople records in database, False if not.

    Raises:
        sqlite3.Error: sqlite3.Error: If error when trying to select salespeople from table.
    """
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM ' + table_name)
        rows = cur.fetchall()
        logger.debug('selected all salespeople records from {} table'.format(table_name))
        if not rows:
            print('There are no sales records. Ask your salespeople to sell something...\n')
            logger.info('there are no sales records in {} table yet'.format(table_name))
            return True
    except sqlite3.Error as e:
        logger.error('unable to select from {}...'.format(table_name, e))
    finally:
        conn.close()
    return False
