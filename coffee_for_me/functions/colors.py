#!/usr/bin/env python3
class Colors:
    """
    Colors class stores colors variables using ANSI escape codes to make console output colorful.
    Usage, e.g.: Colors.GREEN + 'your_string' + Colors.RESET
    """

    BLACK = '\u001b[30m'
    RED = '\u001b[31m'
    GREEN = '\u001b[32m'
    YELLOW = '\u001b[33m'
    BLUE = '\u001b[34m'
    MAGENTA = '\u001b[35m'
    CYAN = '\u001b[36m'
    WHITE = '\u001b[37m'
    RESET = '\u001b[0m'
