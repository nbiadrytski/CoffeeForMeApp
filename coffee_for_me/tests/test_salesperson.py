#!/usr/bin/env python3
from unittest import TestCase
from coffee_for_me.employees.salesperson import Salesperson
from coffee_for_me.functions.db_funcs import *
from coffee_for_me.functions.functions import *
from io import StringIO
from unittest.mock import patch
from unittest import mock
import random
import string
import shutil
import os


class SalespersonTest(TestCase):

    def __init__(self, *args, **kwargs):
        self.sp = Salesperson('John', 'Salesperson', ['Tea'], ['Sugar'])
        self.dynamic_sp = Salesperson(SalespersonTest.generate_random_name(), 'Salesperson', ['Tea'], ['Sugar'])
        super(SalespersonTest, self).__init__(*args, **kwargs)

    def setUp(self):
        create_table()
        with open(employee_filename('salesperson_records', 'John Nhoj', '_records.txt'), 'w') as f:
            f.write('Beverage: tea. Price: 4.0$\n')
            f.write('Beverage: water. Price: 4.3$\n')
            f.write('Addition: sugar. Price: 1.5$\n')

    def tearDown(self):
        # delete temp folder and files created by tests
        try:
            exts = ('.db', '.json', '.xml', '.csv')
            sp_tmp_folder = os.path.join(os.path.dirname(__file__), 'salesperson_records')
            shutil.rmtree(sp_tmp_folder)
            for f in os.listdir(os.curdir):
                if f.endswith(exts):
                    os.remove(f)
        except FileNotFoundError as e:
            print(e)

    @staticmethod
    def generate_random_name():
        name = ''.join(random.choices(string.ascii_letters, k=10))  # random 10-character string
        return name

    def test_sp_employee_greeting(self):
        expected_output = 'Hi \x1b[32mJohn\x1b[0m! You are a salesperson.Hello!\n'
        with patch('sys.stdout', new=StringIO()) as actual_output:
            self.sp.employee_greeting('Hello!')
        self.assertIn(expected_output, actual_output.getvalue(), '\n\nStrings do not match')

    def test_sp_fullname(self):
        full_name = self.sp.fullname
        self.assertEqual(full_name, 'John Nhoj', '\n\nStrings do not match')

    @mock.patch('coffee_for_me.employees.employee.input', create=True)  # mocking user input
    def test_sp_user_choice_valid(self, mocked_input):
        mocked_input.side_effect = [1]
        choice = self.sp.user_choice('Input number:', 3)
        self.assertEqual(choice, 1)

    @mock.patch('coffee_for_me.employees.employee.input', create=True)
    def test_sp_user_choice_exceed_delta(self, mocked_input):
        expected_output = 'John, that is not:\n1 or 2\nTry again!\n\nYour choice is 2\n\n'
        with patch('sys.stdout', new=StringIO()) as actual_output:
            mocked_input.side_effect = [11, 2]
            choice = self.sp.user_choice('Input number:', 3)
        self.assertIn(expected_output, actual_output.getvalue(), '\n\nStrings do not match')
        self.assertEqual(choice, 2)

    @mock.patch('coffee_for_me.employees.employee.input', create=True)
    def test_sp_user_choice_invalid_type_passed(self, mocked_input):
        expected_output = 'John, you can input only numbers. Enter:\n1 or 2\n\nYour choice is 1\n\n'
        with patch('sys.stdout', new=StringIO()) as actual_output:
            mocked_input.side_effect = ['test', 1]
            choice = self.sp.user_choice('Input number:', 3)
        self.assertIn(expected_output, actual_output.getvalue(), '\n\nStrings do not match')
        self.assertEqual(choice, 1)

    @mock.patch('builtins.input', create=True)
    def test_sp_make_sale_beverage_only(self, mocked_input):
        expected_output = 'Beverage: tea. Price: 4.0$\n'
        mocked_input.side_effect = [2, 'tea', 4]
        self.dynamic_sp.make_sale(['Tea'], ['Sugar'])
        with open(employee_filename('salesperson_records', self.dynamic_sp.fullname, '_records.txt'), 'r') as f:
            actual_output = f.read()
        self.assertTrue(is_employee_in_db(self.dynamic_sp.fullname), '\nSalesperson is not found in db')
        self.assertEqual(expected_output, actual_output)

    @mock.patch('builtins.input', create=True)
    def test_sp_make_sale_beverage_and_addition(self, mocked_input):
        expected_output = 'Beverage: tea. Price: 4.0$\nAddition: sugar. Price: 2.0$\n'
        mocked_input.side_effect = [1, 'tea', 4, 'sugar', 2]
        self.dynamic_sp.make_sale(['Tea'], ['Sugar'])
        with open(employee_filename('salesperson_records', self.dynamic_sp.fullname, '_records.txt'), 'r') as f:
            actual_output = f.read()
        self.assertTrue(is_employee_in_db(self.dynamic_sp.fullname), '\nSalesperson is not found in db')
        self.assertEqual(expected_output, actual_output)

    @mock.patch('builtins.input', create=True)
    def test_sp_add_beverage(self, mocked_input):
        mocked_input.side_effect = ['cOfFeE', 2]
        record = self.sp.add_beverage(['Milk', 'Coffee'])
        self.assertEqual('Beverage: coffee. Price: 2.0$', record)

    @mock.patch('builtins.input', create=True)
    def test_sp_add_ingredient(self, mocked_input):
        mocked_input.side_effect = ['mIlK', 3]
        record = self.sp.add_ingredient(['Sugar', 'Milk'])
        self.assertEqual('Addition: milk. Price: 3.0$', record)

    def test_sp_total_sales_amount(self):
        total_amount = self.sp.total_sales_amount()
        self.assertEqual(9.8, total_amount)

    def test_sp_count_sales(self):
        sales_number = self.sp.count_sales()
        self.assertEqual(3, sales_number)

    def test_sp_view_records(self):
        expected_output = 'Beverage: tea. Price: 4.0$\n\nBeverage: water. Price: 4.3$\n\n' \
                          'Addition: sugar. Price: 1.5$\n\n'
        with patch('sys.stdout', new=StringIO()) as actual_output:
            self.sp.view_records()
        self.assertIn(expected_output, actual_output.getvalue(), '\n\nStrings do not match')
