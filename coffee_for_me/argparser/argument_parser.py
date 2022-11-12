#!/usr/bin/env python3
import argparse
import logging
from coffee_for_me.functions.colors import Colors

logger = logging.getLogger('main.argparsing.argparser.argument_parser.ArgumentParser')


class ArgumentParser(argparse.ArgumentParser):
    """
    Parses positional and optional command-line arguments passed by user.
    ArgumentParser class inherits built-in argparse.ArgumentParser class.
    Overrides argparse.ArgumentParser error method to customize error for missing args.
    Prints -h for user when the app is started.
    """

    @staticmethod
    def parse_arguments():
        """
        Parses positional and optional command-line arguments passed by user.
        Prints help message for user when the app is started.
        Positional args: employee_name, employee_position.
        Optional args: beverage, addition

        Returns:
            ArgumentParser: arguments parser.
        """
        parser = ArgumentParser(description='Sell drinks and view sales records with "CoffeeForMe!"',
                                epilog='Thank you for using "CoffeeForMe" App!\n')

        parser.add_argument('name', type=str, nargs=1, metavar='employee_name', default=None,
                            help='Employee name')
        parser.add_argument('position', type=str, nargs=1, metavar='employee_position', default=None,
                            help='Employee position (Salesperson or Manager)')
        parser.add_argument('-bev', '--beverage', action='append', default=None,
                            help='List of available beverages a Salesperson can sell: tea, coffee, water, soda, etc.')
        parser.add_argument('-add', '--addition', action='append', default=None,
                            help='List of available ingredients a Salesperson can add: sugar, milk, cinnamon, etc.')

        print('\n')
        logger.info('parse_arguments(): created args parser')

        return parser

    def error(self, message):
        """
        Overrides argparse.ArgumentParser error method to customize error for missing args.
        Prints Error message and exits.

        Parameters:
            message (str): message name.
        """
        logger.error('obligatory args were not supplied bu user: {} - {}'.format(self.prog, message))
        self.exit(0, '{}: {}.\nRun "python coffee_for_me -h" to see help.\n'.
                  format(self.prog, Colors.RED + message + Colors.RESET))

    @staticmethod
    def quit_msg(name, position):
        """
        Prints info message with valid positions to user
        If invalid position was passed via command-line arguments.

        Parameters:
            name (str): Employee name.
            position (str): valid Employee position (Salesperson or Manager).
        """
        print('{} with {} position is not a valid employee.'.
              format(Colors.RED + name + Colors.RESET, Colors.RED + position + Colors.RESET))
        print('Available positions: Salesperson or Manager')
