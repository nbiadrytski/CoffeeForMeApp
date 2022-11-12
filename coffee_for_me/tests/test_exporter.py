#!/usr/bin/env python3
from unittest import TestCase
from coffee_for_me.exporter.exporter import Exporter
from coffee_for_me.functions.db_funcs import *
import os


class ExporterTest(TestCase):

    def setUp(self):
        create_table()
        insert_db_record('Mike', 7, 9)
        insert_db_record('John', 2, 32)
        self.exporter = Exporter()
        self.file_name = 'Dan Smith_records.'

    def tearDown(self):
        try:
            extensions = ('.db', '.json', '.xml', '.csv')
            for f in os.listdir(os.curdir):
                if f.endswith(extensions):
                    os.remove(f)
        except FileNotFoundError as e:
            print(e)

    def test_export_as_json(self):
        expected_json = '{"employees": [{"id": 1, "name": "Mike", "sales": 7, "amount": 9}, ' \
                        '{"id": 2, "name": "John", "sales": 2, "amount": 32}]}'
        res = self.exporter.export_as_json(self.file_name + 'json')
        self.assertEqual(expected_json, res)

    def test_export_as_xml(self):
        expected_xml = '''<?xml version="1.0" ?>
<employees>
  <row>
    <id>1</id>
    <name>Mike</name>
    <sales>7</sales>
    <amount>9</amount>
  </row>
  <row>
    <id>2</id>
    <name>John</name>
    <sales>2</sales>
    <amount>32</amount>
  </row>
</employees>\n'''
        res = self.exporter.export_as_xml(self.file_name + 'xml')
        self.assertEqual(expected_xml, res)

    def test_export_as_csv(self):
        res = self.exporter.export_as_csv(self.file_name + 'xml')
        self.assertIn('ID,Name,Number of Sales,Total Amount ($)', res)
        self.assertIn('1,Mike,7,9', res)
        self.assertIn('2,John,2,32', res)

