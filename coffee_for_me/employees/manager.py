#!/usr/bin/env python3
from coffee_for_me.employees.employee import Employee
from coffee_for_me.functions.db_funcs import *
from coffee_for_me.exporter.exporter import Exporter
from coffee_for_me.functions.functions import show_sales_table, employee_filename
import logging


class Manager(Employee):
    """
    Manager class inherits Employee class.
    Holds logic for viewing salespeople sales records in formatted table
    And exporting sales records to different formats.

    Attributes:
        name (str): Manager first name passed as a command line argument
        position (str): Manager position passed as a command line argument
        logger (Logger): creating Logger for Manager class
    """

    manager_export_msg = '''Would you like to export sales records? Enter 1, 2, 3 or 4:
        1 - Export as JSON
        2 - Export as XML
        3 - Export as CSV
        4 - Do not export\n'''

    def __init__(self, name, position):
        """
        The constructor for Manager class.

        Attributes:
            name (str): Manager first name
            position (str): Manager as position
        """
        super().__init__(name, position)
        self.logger = logging.getLogger('main.argparsing.employees.Manager')
        self.logger.info('Initialising Manager')

    def view_records(self):
        """
        Printing salespeople sales records stored in database in formatted table.
        Overrides Employee.view_records() method.

        Raises:
            RuntimeWarning: If no records found in database.
        """
        try:
            employees = view_db_records()
            self.logger.debug('{} printing salespeople sales records table'.format(self.__str__()))
            show_sales_table(employees)
            self.logger.info('{} viewed the table with sales records'.format(self.__str__()))
        except RuntimeWarning:
            print('\nNo sales records yet. Ask your salespeople to sell something.\n')
            self.logger.info('No sales records yet')

    def export_records(self):
        """
        Exporting sales records to json, xml and csv files based on user's choice.
        Printing file folder to user.

        Returns:
            str: exported file path and name.
        """
        choice = self.user_choice(self.manager_export_msg, 5)
        if choice == 1:
            json_file_path = employee_filename('manager_records', self.fullname, '_records.json')
            self.logger.debug('{} is trying to export json records'.format(self.fullname))
            Exporter.export_as_json(employee_filename('manager_records', self.fullname, '_records.json'))
            self.logger.info('{} exported json records to {}'.format(self.fullname, json_file_path))
            print('{}, your exported json file is in "manager_records" folder\n'.format(self.name))
            return json_file_path
        elif choice == 2:
            xml_file_path = employee_filename('manager_records', self.fullname, '_records.xml')
            self.logger.debug('{} is trying to export xml records'.format(self.fullname))
            Exporter.export_as_xml(employee_filename('manager_records', self.fullname, '_records.xml'))
            self.logger.info('{} exported xml records to {}'.format(self.fullname, xml_file_path))
            print('{}, your exported xml file is in "manager_records" folder\n'.format(self.name))
            return xml_file_path
        elif choice == 3:
            csv_file_path = employee_filename('manager_records', self.fullname, '_records.csv')
            self.logger.debug('{} is trying to export csv records'.format(self.fullname))
            Exporter.export_as_csv(employee_filename('manager_records', self.fullname, '_records.csv'))
            self.logger.info('{} exported csv records to {}'.format(self.fullname, csv_file_path))
            print('{}, your exported csv file is in "manager_records" folder\n'.format(self.name))
            return csv_file_path
        elif choice == 4:
            print('{}, you can always export sales records later.\n'.format(self.name))

    def __str__(self):
        return '{} - {}'.format(self.name, self.position)
