#!/usr/bin/env python3
from unittest import TestCase
from coffee_for_me.functions.db_funcs import *
import os


class DbFuncsTest(TestCase):

    def setUp(self):
        self.conn = create_connection()
        create_table()
        self.cur = self.conn.cursor()

    def tearDown(self):
        self.conn.close()
        try:
            extensions = ('.db', '.json', '.xml', '.csv')
            for f in os.listdir(os.curdir):
                if f.endswith(extensions):
                    os.remove(f)
        except FileNotFoundError as e:
            print(e)

    def test_create_table(self):
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='employees'")
        self.assertEqual([('employees',)], self.cur.fetchall(), '\n\nTables does not exist')

    def test_is_employee_in_db(self):
        insert_db_record('Jake', 7, 9)
        self.conn.commit()
        self.assertEqual(True, is_employee_in_db('Jake'))

    def test_insert_db_record(self):
        insert_db_record('Mike', 7, 9)
        self.cur.execute('SELECT * FROM employees WHERE name="Mike"')
        self.assertEqual([(1, 'Mike', 7, 9)], self.cur.fetchall())

    def test_update_db_record(self):
        insert_db_record('Mike', 7, 9)
        update_db_record('Mike', 10, 10)
        self.cur.execute('SELECT * FROM employees WHERE name="Mike"')
        self.assertEqual([(1, 'Mike', 10, 10)], self.cur.fetchall())

    def test_view_db_records(self):
        insert_db_record('Mike', 70, 90)
        insert_db_record('Nina', 20, 30)
        self.assertEqual([(1, 'Mike', 70, 90), (2, 'Nina', 20, 30)], view_db_records())

    def test_is_table_empty_false(self):
        insert_db_record('Mike', 70, 90)
        self.assertEqual(False, is_table_empty())

    def test_is_table_empty_true(self):
        self.assertEqual(True, is_table_empty())


