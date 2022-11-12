#!/usr/bin/env python3
from unittest import TestCase
from coffee_for_me.employees.employee import Employee
from io import StringIO
from unittest.mock import patch
from unittest import mock


class EmployeeTest(TestCase):

    def __init__(self,*args, **kwargs):
        self.emp = Employee('David', 'Owner')
        super(EmployeeTest, self).__init__(*args, **kwargs)

    def test_emp_employee_greeting(self):
        expected_output = 'Hi \x1b[32mDavid\x1b[0m! You are a owner.Hello!\n'
        with patch('sys.stdout', new=StringIO()) as actual_output:
            self.emp.employee_greeting('Hello!')
        self.assertIn(expected_output, actual_output.getvalue(), '\n\nStrings do not match')

    def test_emp_fullname(self):
        full_name = self.emp.fullname
        self.assertEqual(full_name, 'David Divad', '\n\nStrings do not match')

    @mock.patch('coffee_for_me.employees.employee.input', create=True)  # mocking user input
    def test_emp_user_choice_valid(self, mocked_input):
        mocked_input.side_effect = [1]
        choice = self.emp.user_choice('Input number:', 3)
        self.assertEqual(choice, 1)

    @mock.patch('coffee_for_me.employees.employee.input', create=True)
    def test_emp_user_choice_exceed_delta(self, mocked_input):
        expected_output = 'David, that is not:\n1 or 2\nTry again!\n\nYour choice is 2\n\n'
        with patch('sys.stdout', new=StringIO()) as actual_output:
            mocked_input.side_effect = [11, 2]
            choice = self.emp.user_choice('Input number:', 3)
        self.assertIn(expected_output, actual_output.getvalue(), '\n\nStrings do not match')
        self.assertEqual(choice, 2)

    @mock.patch('coffee_for_me.employees.employee.input', create=True)
    def test_emp_user_choice_invalid_type_passed(self, mocked_input):
        expected_output = 'David, you can input only numbers. Enter:\n1 or 2\n\nYour choice is 1\n\n'
        with patch('sys.stdout', new=StringIO()) as actual_output:
            mocked_input.side_effect = ['test', 1]
            choice = self.emp.user_choice('Input number:', 3)
        self.assertIn(expected_output, actual_output.getvalue(), '\n\nStrings do not match')
        self.assertEqual(choice, 1)

    def test_emp_view_records(self):
        expected_output = 'Hi David Divad! Ask your managers if you need to see sales records\n'
        with patch('sys.stdout', new=StringIO()) as actual_output:
            self.emp.view_records()
        self.assertIn(expected_output, actual_output.getvalue(), '\n\nStrings do not match')
