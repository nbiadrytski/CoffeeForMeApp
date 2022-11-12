#!/usr/bin/env python3
from unittest import TestCase
from coffee_for_me.functions.functions import *
from coffee_for_me.argparser.argument_parser import ArgumentParser
from unittest.mock import patch
from unittest import mock
from io import StringIO
import shutil


class FunctionsTest(TestCase):

    def setUp(self):
        self.parser = ArgumentParser.parse_arguments()

    def tearDown(self):
        # delete temp folder created by tests
        try:
            tmp_folder = os.path.join(os.path.dirname(__file__), 'manager_records')
            shutil.rmtree(tmp_folder)
        except FileNotFoundError as e:
            print(e)

    def test_get_employee_position_salesperson(self):
        args = self.parser.parse_args(['John', 'SaLeSpErSoN'])
        pos = get_employee_position(args)
        self.assertEqual('salesperson', pos)

    def test_get_employee_position_manager(self):
        args = self.parser.parse_args(['John', 'mAnaGeR'])
        pos = get_employee_position(args)
        self.assertEqual('manager', pos)

    def test_get_employee_position_invalid_pos(self):
        args = self.parser.parse_args(['John', 'Seller'])
        pos = get_employee_position(args)
        self.assertEqual(None, pos)

    def test_employee_filename(self):
        file_path = employee_filename('manager_records', 'Mike Jones', '_file.txt')
        self.assertEqual(os.path.join('manager_records', 'Mike Jones_file.txt'), file_path)

    @mock.patch('builtins.input', create=True)
    def test_item_to_sell(self, mocked_input):
        expected_output = 'You can sell the following beverages:\n\x1b[32mWater\x1b[0m\n\x1b[32mTea\x1b[0m\n'
        with patch('sys.stdout', new=StringIO()) as actual_output:
            mocked_input.side_effect = ['beverage']
            item = get_item_to_sell('beverage', ['Water', 'Tea'])
        self.assertIn(expected_output, actual_output.getvalue(), '\n\nStrings do not match')
        self.assertEqual('beverage', item)

    @mock.patch('builtins.input', create=True)
    def test_enter_price_int(self, mocked_input):
        mocked_input.side_effect = [4]
        price = enter_price('ingredient')
        self.assertEqual('4.0', price)

    @mock.patch('builtins.input', create=True)
    def test_enter_price_float(self, mocked_input):
        mocked_input.side_effect = [4.87]
        price = enter_price('ingredient')
        self.assertEqual('4.87', price)

    @mock.patch('builtins.input', create=True)
    def test_enter_price_str(self, mocked_input):
        expected_output = '"four" is not a number. You can enter only positive integers or floats\nTry again!\n'
        with patch('sys.stdout', new=StringIO()) as actual_output:
            mocked_input.side_effect = ['four', 5]
            price = enter_price('ingredient')
        self.assertEqual('5.0', price)
        self.assertIn(expected_output, actual_output.getvalue(), '\n\nStrings do not match!')

    @mock.patch('builtins.input', create=True)
    def test_enter_price_negative_number(self, mocked_input):
        expected_output = 'You can enter only positive integers or floats.\nTry Again!\n'
        with patch('sys.stdout', new=StringIO()) as actual_output:
            mocked_input.side_effect = [-3, 5]
            price = enter_price('beverage')
        self.assertEqual('5.0', price)
        self.assertIn(expected_output, actual_output.getvalue(), '\n\nStrings do not match!')

    def test_beverage_to_file(self):
        bev1 = beverage_to_file('test_records.txt', '1st beverage')
        bev2 = beverage_to_file('test_records.txt', '2nd beverage')
        os.remove('test_records.txt')
        self.assertEqual('1st beverage\n', bev1)
        self.assertEqual('1st beverage\n2nd beverage\n', bev2)

    def test_beverage_addition_to_file(self):
        rec1 = beverage_addition_to_file('test_records.txt', '1st beverage', '1st addition')
        rec2 = beverage_addition_to_file('test_records.txt', '2nd beverage', '2nd addition')
        os.remove('test_records.txt')
        self.assertEqual('1st beverage\n1st addition\n', rec1)
        self.assertEqual('1st beverage\n1st addition\n2nd beverage\n2nd addition\n', rec2)

    def test_show_sales_table(self):
        expected_output = '\x1b[32mSeller Name\x1b[0m                   \t|\t\x1b' \
                          '[32mNumber Of Sales\x1b[0m\t|\t\x1b[32mTotal Value ($)\x1b' \
                          '[0m\nTony Ynot                     \t|\t3              \t|\t6.8\n' \
                          'Jack Smith                    \t|\t6              \t|\t9.67\n' \
                          'Total:                        \t|\t9              \t|\t16.47\t\n\n'
        with patch('sys.stdout', new=StringIO()) as actual_output:
            show_sales_table([(1, 'Tony Ynot', 3, 6.8), (2, 'Jack Smith', 6, 9.67)])
        self.assertIn(expected_output, actual_output.getvalue(), '\n\nStrings do not match')

    def test_match_price(self):
        price_list = [2.0]
        final_price_list = match_price(price_list, r'[-+]?\d*\.\d+|\d+', 'Addition: milk. Price: 1.58$')
        self.assertEqual([2.0, 1.58], final_price_list)
