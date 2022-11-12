#!/usr/bin/env python3
import logging
from coffee_for_me.functions.colors import Colors


class Employee:
    """
    Employee class holds generic logic for any CoffeeForMe position.
    Can be subclassed by different Employee types: Salesperson, Manager, etc.

    Attributes:
        name (str): Employee first name passed as a command line argument
        position (str): Employee position (e.g. Salesperson, Manager) passed as a command line argument
        logger (Logger): creating Logger for Employee class
    """

    def __init__(self, first_name, position):
        """
        The constructor for Employee class.

        Attributes:
            first_name (str): Employee first name
            position (str): Employee position (e.g. Salesperson, Manager)
        """
        self.name = first_name
        self.position = position
        self.logger = logging.getLogger('main.argparsing.employees.Employee')
        self.logger.debug('Initialising Employee')

    @property
    def fullname(self):
        """str: Get Employee fullname: first name + first name with capital letter in reverse order"""
        return "{} {}".format(self.name, self.name[::-1].capitalize())

    def employee_greeting(self, message):
        """
        Prints greeting message (name, position, possible actions) when employee starts the app

        Parameters:
            message (str): Employee possible actions based on the position.
        """
        print('Hi {}! You are a {}.{}'.format(Colors.GREEN + self.name + Colors.RESET, self.position.lower(), message))

    def user_choice(self, choice_msg, delta):
        """
        Getting user input, validating it.
        Returns user's choice as a dictionary value.

        Parameters:
            choice_msg (str): Start message to get user input.
            delta (int): range of valid numbers for user's choice

        Returns:
            int: user's choice as a dictionary value.

        Raises:
            ValueError: If user input non-int value
        """
        while True:
            try:
                choice_dict = dict()
                choice = int(input(choice_msg))
                value = choice
                self.logger.debug('Employee {} made a choice: {}'.format(self.__str__(), str(choice)))
            except ValueError:
                print('{}, you can input only numbers. Enter:'.format(self.name))
                print(' or '.join(str(x) for x in range(1, delta)) + '\n')
                continue
            if 0 < choice < delta:
                self.logger.debug('Employee {} choice "{}" is valid according to choice delta "{}"'.
                                  format(self.__str__(), str(choice), str(delta)))
                break
            else:
                print('{}, that is not:'.format(self.name))
                print(' or '.join(str(x) for x in range(1, delta)))
                print('Try again!\n')
        print('Your choice is {}\n'.format(choice))
        choice_dict[choice] = value
        return choice_dict[value]

    def view_records(self):
        """Printing info message for owner position."""
        print('Hi {}! Ask your managers if you need to see sales records'.format(self.fullname))

    def __str__(self):
        return '{} - {}'.format(self.name, self.position)
