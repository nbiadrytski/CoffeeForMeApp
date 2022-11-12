#!/usr/bin/env python3
from coffee_for_me.functions.db_funcs import *
import json
import csv

logger = logging.getLogger('main.argparsing.exporter.exporter.Exporter')


class Exporter:
    """
    Exporter class holds methods to export data to different formats.
    """

    @staticmethod
    def export_as_json(file_name):
        """
        Gets salespeople records from database and
        Exports them to json file using json module.

        Parameters:
            file_name (str): name of the file. Pass employee_filename function.

        Returns:
            str: json file content.

        Raises:
            IOError: If file not found or path is incorrect.
            TypeError: If trying to pass NoneType instead of file.
        """
        try:
            with open(file_name, "w") as f:
                conn = create_connection()
                cur = conn.cursor()
                result = cur.execute('SELECT * FROM ' + table_name)
                items = [dict(zip([key[0] for key in cur.description], row)) for row in result]
                json_records = (json.dumps({table_name: items}))
                logger.debug('json records to export: {}'.format(json_records))
                f.write(json_records)
                conn.close()
                return json_records
        except IOError as e:
            logger.error('File {} not found or path is incorrect... {}'.format(file_name, e))
        except TypeError as e:
            logger.error('Trying to pass NoneType {} instead of file... {}'.format(file_name, e))

    @staticmethod
    def export_as_xml(file_name):
        """
        Gets salespeople records from database and writes them to xml file.

        Parameters:
            file_name (str): name of the file. Pass employee_filename function.

        Returns:
            str: xml file content.

        Raises:
            IOError: If file not found or path is incorrect.
            TypeError: If trying to pass NoneType instead of file.
        """
        try:
            with open(file_name, 'w') as f:
                f.write('<?xml version="1.0" ?>\n')
                f.write('<employees>\n')
                for row in view_db_records():
                    f.write('  <row>\n')
                    f.write('    <id>{}</id>\n'.format(row[0]))
                    f.write('    <name>{}</name>\n'.format(row[1]))
                    f.write('    <sales>{}</sales>\n'.format(row[2]))
                    f.write('    <amount>{}</amount>\n'.format(row[3]))
                    f.write('  </row>\n')
                f.write('</employees>\n')
                logger.debug('stored sales records to xml {} file'.format(file_name))
            with open(file_name, 'r') as file:
                content = file.read()
            return content
        except IOError as e:
            logger.error('File {} not found or path is incorrect... {}'.format(file_name, e))
        except TypeError as e:
            logger.error('Trying to pass NoneType {} instead of file... {}'.format(file_name, e))

    @staticmethod
    def export_as_csv(file_name):
        """
        Gets salespeople records from database and writes them to csv file.

        Parameters:
            file_name (str): name of the file.  Pass employee_filename function.

        Returns:
            _io.TextIOWrapper: file object.

        Raises:
            IOError: If file not found or path is incorrect.
            TypeError: If trying to pass NoneType instead of file.
        """
        conn = create_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM ' + table_name)
        try:
            with open(file_name, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Name", 'Number of Sales', 'Total Amount ($)'])
                for row in cur:
                    writer.writerow(row)
                logger.debug('stored sales records to csv {} file'.format(file_name))
            with open(file_name, 'r') as file:
                content = file.read()
            conn.close()
            return content
        except IOError as e:
            logger.error('File {} not found or path is incorrect... {}'.format(file_name, e))
        except TypeError as e:
            logger.error('Trying to pass NoneType {} instead of file... {}'.format(file_name, e))
