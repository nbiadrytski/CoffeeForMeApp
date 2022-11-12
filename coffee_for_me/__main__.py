#!/usr/bin/env python3
from coffee_for_me.employees.manager import Manager
from coffee_for_me.employees.salesperson import Salesperson
from coffee_for_me.argparser.argument_parser import ArgumentParser
from coffee_for_me.functions.db_funcs import create_table, is_table_empty
from coffee_for_me.functions.functions import get_employee_position
from coffee_for_me.functions.colors import Colors
import logging
import sys


def main():
    # creating logger
    logger = logging.getLogger('main')
    logger.setLevel(logging.INFO)
    # creating File Handler
    file_handler = logging.FileHandler('coffee_for_me.log')
    file_handler.setLevel(logging.INFO)
    # creating Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    salesperson_choice_msg = '''What would you like to do? Enter 1 or 2:
    1 - Sell a beverage
    2 - I am tired... No more sales...\n'''

    manager_choice_msg = '''What would you like to do? Enter 1 or 2:
        1 - View/export sales records
        2 - No reports today... Maybe later...\n'''

    parser = ArgumentParser.parse_arguments()
    args = parser.parse_args()
    if str(sys.argv[1]) is not '-h':  # don't print Help if user passed -h arg
        print('=' * 76)
        parser.print_help()  # printing Help for user once the app is started
        print('=' * 76 + '\n')
    logger.info('User passed the following command line args: {}'.format(args))

    # detecting if employee is a manager
    if get_employee_position(args) == 'manager':
        try:
            manager = Manager(args.name[0], args.position[0])
            logger.info('Created Manager instance: {}'.format(manager.__str__()))
            manager.employee_greeting('\nYou can view and export sales records\n')
            logger.debug('Greeted {}'.format(manager.__str__()))
            while manager.user_choice(manager_choice_msg, 3) == 1:
                create_table()
                logger.info('DB table created: {}'.format(manager.fullname))
                if not is_table_empty():
                    manager.view_records()
                    logger.info('{} viewed salespeople records'.format(manager.fullname))
                    manager.export_records()
                    logger.info('{} exported salespeople records'.format(manager.fullname))
            else:
                print('Bye-Bye, {}! See you next time'.format(args.name[0]))
                logger.info('Manager {} decided to quit the app'.format(manager.fullname))
        except NameError:
            logger.error('Non-manager object is trying to access manager stuff...')

    # detecting if employee is a salesperson
    elif get_employee_position(args) == 'salesperson':
        try:
            if args.beverage and args.addition:
                salesperson = Salesperson(args.name[0], args.position[0], args.beverage, args.addition)
                logger.info('Created Salesperson instance: {}'.format(salesperson.__str__()))
                salesperson.employee_greeting('\nYou can sell beverages and ingredients\n')
                logger.debug('Greeted {}'.format(salesperson.__str__()))
                while salesperson.user_choice(salesperson_choice_msg, 3) == 1:
                    create_table()
                    logger.info('DB table created: {}'.format(salesperson.fullname))
                    salesperson.make_sale(args.beverage, args.addition)
                    logger.info('{} made a sale'.format(salesperson.fullname))
                    salesperson.view_records()
                    logger.info('Salesperson {} is viewing personal sales records'.format(salesperson.fullname))
                else:
                    print('Bye-Bye, {}! See you next time'.format(args.name[0]))
                    logger.info('Salesperson {} decided to quit the app'.format(salesperson.fullname))
            else:
                print('Provide both', Colors.GREEN + 'beverage(s)' + Colors.RESET, 'and ' + Colors.GREEN
                      + 'ingredient(s)' + Colors.RESET, 'as command line arguments! See Help above.')
        except NameError:
            logger.error('Non-salesperson object is trying to access salesperson stuff...')
    else:
        args_positions = ArgumentParser()
        args_positions.quit_msg(args.name[0], args.position[0])
        logger.error('{} with position {} is not a valid employee...'.format(args.name[0], args.position[0]))


if __name__ == "__main__":
    main()
