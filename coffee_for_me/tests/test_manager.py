#!/usr/bin/env python3
from unittest import TestCase
from coffee_for_me.employees.manager import Manager
from coffee_for_me.functions.db_funcs import *
from io import StringIO
from unittest.mock import patch
from unittest import mock
import shutil
import os


class ManagerTest(TestCase):

    def __init__(self,*args, **kwargs):
        self.mng = Manager('Tony', 'Manager')
        super(ManagerTest, self).__init__(*args, **kwargs)

    def setUp(self):
        create_table()
        if not is_employee_in_db('Johnny Smith') or not is_employee_in_db('Mary Brown'):
            insert_db_record('Johnny Smith', 5, 67.8)
            insert_db_record('Mary Brown', 2, 9)

    def tearDown(self):
        # delete temp folder and files created by tests
        try:
            exts = ('.db', '.json', '.xml', '.csv')
            mng_tmp_folder = os.path.join(os.path.dirname(__file__), 'manager_records')
            shutil.rmtree(mng_tmp_folder)
            for f in os.listdir(os.curdir):
                if f.endswith(exts):
                    os.remove(f)
        except FileNotFoundError as e:
            print(e)

    def test_mng_employee_greeting(self):
        expected_output = 'Hi \x1b[32mTony\x1b[0m! You are a manager.Hello!\n'
        with patch('sys.stdout', new=StringIO()) as actual_output:
            self.mng.employee_greeting('Hello!')
            self.assertIn(expected_output, actual_output.getvalue(), '\n\nStrings do not match')

    def test_mng_fullname(self):
        full_name = self.mng.fullname
        self.assertEqual(full_name, 'Tony Ynot', '\n\nStrings do not match')

    @mock.patch('coffee_for_me.employees.employee.input', create=True)  # mocking user input
    def test_mng_user_choice_valid(self, mocked_input):
        mocked_input.side_effect = [1]
        choice = self.mng.user_choice('Input number:', 3)
        self.assertEqual(choice, 1)

    @mock.patch('coffee_for_me.employees.employee.input', create=True)
    def test_mng_user_choice_exceed_delta(self, mocked_input):
        expected_output = 'Tony, that is not:\n1 or 2\nTry again!\n\nYour choice is 2\n\n'
        with patch('sys.stdout', new=StringIO()) as actual_output:
            mocked_input.side_effect = [11, 2]
            choice = self.mng.user_choice('Input number:', 3)
        self.assertIn(expected_output, actual_output.getvalue(), '\n\nStrings do not match')
        self.assertEqual(choice, 2)

    @mock.patch('coffee_for_me.employees.employee.input', create=True)
    def test_mng_user_choice_invalid_type_passed(self, mocked_input):
        expected_output = 'Tony, you can input only numbers. Enter:\n1 or 2\n\nYour choice is 1\n\n'
        with patch('sys.stdout', new=StringIO()) as actual_output:
            mocked_input.side_effect = ['test', 1]
            choice = self.mng.user_choice('Input number:', 3)
        self.assertIn(expected_output, actual_output.getvalue(), '\n\nStrings do not match')
        self.assertEqual(choice, 1)

    def test_mng_view_records(self):
        expected_output = '\x1b[32mSeller Name\x1b[0m                   \t|\t\x1b[32mNumber Of Sales\x1b[0m\t|\t\x1b' \
                          '[32mTotal Value ($)\x1b[0m\nJohnny Smith                  \t|\t5              \t|\t' \
                          '67.8\nMary Brown                    \t|\t2              \t|\t9\nTotal:' \
                          '                        \t|\t7              \t|\t76.8\t\n\n'
        with patch('sys.stdout', new=StringIO()) as actual_output:
            self.mng.view_records()
        self.assertIn(expected_output, actual_output.getvalue(), '\n\nStrings do not match')

    @mock.patch('builtins.input', create=True)
    def test_mng_export_records_json(self, mocked_input):
        expected_output = os.path.join('Your choice is 1\n\n'
                                       'Tony, your exported json file is in "manager_records" folder\n\n')
        with patch('sys.stdout', new=StringIO()) as actual_output:
            mocked_input.side_effect = [1]
            json_file_path = self.mng.export_records()
        self.assertIn(expected_output, actual_output.getvalue(), '\n\nStrings do not match')
        self.assertEqual(os.path.join('manager_records', 'Tony Ynot_records.json'), json_file_path)

    @mock.patch('builtins.input', create=True)
    def test_mng_export_records_xml(self, mocked_input):
        expected_output = os.path.join('Your choice is 2\n\n'
                                       'Tony, your exported xml file is in "manager_records" folder\n\n')
        with patch('sys.stdout', new=StringIO()) as actual_output:
            mocked_input.side_effect = [2]
            xml_file_path = self.mng.export_records()
        self.assertIn(expected_output, actual_output.getvalue(), '\n\nStrings do not match')
        self.assertEqual(os.path.join('manager_records', 'Tony Ynot_records.xml'), xml_file_path)

    @mock.patch('builtins.input', create=True)
    def test_mng_export_records_csv(self, mocked_input):
        expected_output = os.path.join('Your choice is 3\n\n'
                                       'Tony, your exported csv file is in "manager_records" folder\n\n')
        with patch('sys.stdout', new=StringIO()) as actual_output:
            mocked_input.side_effect = [3]
            csv_file_path = self.mng.export_records()
        self.assertIn(expected_output, actual_output.getvalue(), '\n\nStrings do not match')
        self.assertEqual(os.path.join('manager_records', 'Tony Ynot_records.csv'), csv_file_path)

    @mock.patch('builtins.input', create=True)
    def test_mng_export_records_no_export(self, mocked_input):
        expected_output = 'Your choice is 4\n\nTony, you can always export sales records later.\n\n'
        with patch('sys.stdout', new=StringIO()) as actual_output:
            mocked_input.side_effect = [4]
            self.mng.export_records()
        self.assertIn(expected_output, actual_output.getvalue(), '\n\nStrings do not match')
