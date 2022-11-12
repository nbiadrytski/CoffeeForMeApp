from setuptools import setup
"""
the runnable will be called coffee_for_me,
and when executed it will run the main function in the __main__
which is part of the coffee_for_me package.
"""


setup(
    name='coffee_for_me',
    version='1.0.0',
    packages=['coffee_for_me'],
    entry_points={'console_scripts': ['coffee_for_me = coffee_for_me.__main__:main']}
)