#!/usr/bin/env python3
from coffee_for_me.argparser.argument_parser import ArgumentParser
from unittest import TestCase
from io import StringIO
from unittest.mock import patch


class ArgparserTest(TestCase):

    def setUp(self):
        self.parser = ArgumentParser.parse_arguments()

    def test_argsparser_all_args(self):
        args = self.parser.parse_args(['John', 'Salesperson', '-bev=Tea', '-add=Sugar'])
        self.assertEqual(args.name, ['John'])
        self.assertEqual(args.position, ['Salesperson'])
        self.assertEqual(args.beverage, ['Tea'])
        self.assertEqual(args.addition, ['Sugar'])

    def test_argsparser_multi_bevs_and_adds(self):
        args = self.parser.parse_args(['John', 'Salesperson', '-bev=Tea', '-bev=Coffee', '-add=Sugar', '-add=Salt'])
        self.assertEqual(args.name, ['John'])
        self.assertEqual(args.position, ['Salesperson'])
        self.assertEqual(args.beverage, ['Tea', 'Coffee'])
        self.assertEqual(args.addition, ['Sugar', 'Salt'])

    def test_argsparser_no_opt_args(self):
        args = self.parser.parse_args(['John', 'Salesperson'])
        self.assertEqual(args.name, ['John'])
        self.assertEqual(args.position, ['Salesperson'])
        self.assertEqual(args.beverage, None)
        self.assertEqual(args.addition, None)

    def test_argsparser_no_bev_arg(self):
        args = self.parser.parse_args(['John', 'Salesperson', '-add=Sugar'])
        self.assertEqual(args.name, ['John'])
        self.assertEqual(args.position, ['Salesperson'])
        self.assertEqual(args.beverage, None)
        self.assertEqual(args.addition, ['Sugar'])

    def test_argsparser_no_add_arg(self):
        args = self.parser.parse_args(['John', 'Salesperson', '-bev=Tea'])
        self.assertEqual(args.name, ['John'])
        self.assertEqual(args.position, ['Salesperson'])
        self.assertEqual(args.beverage, ['Tea'])
        self.assertEqual(args.addition, None)

    @patch('sys.stderr', new_callable=StringIO)
    def test_argsparser_no_pos_args(self, mock_stderr):
        with self.assertRaises(SystemExit):  # catching SystemExit
            self.parser.parse_args(['-bev=Tea', '-add=Sugar'])
        self.assertIn('the following arguments are required: employee_name, employee_position',
                      mock_stderr.getvalue())

    @patch('sys.stderr', new_callable=StringIO)
    def test_argsparser_one_of_pos_args_missing(self, mock_stderr):
        with self.assertRaises(SystemExit):
            self.parser.parse_args(['John', '-bev=Tea', '-add=Sugar'])
        self.assertIn('the following arguments are required: employee_position', mock_stderr.getvalue())
