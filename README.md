## CoffeeForMe
Sell beverages and view/export sales records with CoffeeForMe command-line application.

Supports _Python 3.6+_. Only builtin modules are used.

#### Description
There are 2 roles in the app: **Salesperson** and **Manager**.

Salesperson can sell _beverages_ (e.g. Tea, Coffee, Water, Soda, etc.) and _ingredients_ (e.g. Sugar, Milk, Cinnamon, etc.). Once the sale is done, salesperson's sales details will be printed and stored at project root inside **salesperson_records** folder with file name **FirstName LastName_records.txt**.

Manager can view salespeople's sales records (printed as a table) and export records as json, xml and csv files. Sales records are stored at project root inside **manager_records** folder with file names **FirstName LastName_records.json**, **FirstName LastName_records.xml**, **FirstName LastName_records.csv**.

Once the app is started, HELP will be printed:
```
usage: coffee_for_me [-h] [-bev BEVERAGE] [-add ADDITION]
                     employee_name employee_position

Sell drinks and view sales records with "CoffeeForMe!"

positional arguments:
  employee_name         Employee name
  employee_position     Employee position (Salesperson or Manager)

optional arguments:
  -h, --help            show this help message and exit
  -bev BEVERAGE, --beverage BEVERAGE
                        List of available beverages a Salesperson can sell:
                        tea, coffee, water, soda, etc.
  -add ADDITION, --addition ADDITION
                        List of available ingredients a Salesperson can add:
                        sugar, milk, cinnamon, etc.

Thank you for using "CoffeeForMe" App!
```

#### Installation
1. Clone the repository.
2. Run ```pip3 install -e .``` from project root folder to install the app in development mode (if on Windows OS you will probably have to run ```python pip install -e .``` .
```
Machine_Name:CoffeeForMeApp user_name$ pip3 install -e .
Obtaining file:///Users/user_name/path/to/app/CoffeeForMeApp
Installing collected packages: coffee-for-me
  Found existing installation: coffee-for-me 1.0.0
    Uninstalling coffee-for-me-1.0.0:
      Successfully uninstalled coffee-for-me-1.0.0
  Running setup.py develop for coffee-for-me
Successfully installed coffee-for-me
```

#### Usage
1. As a Salesperson run ```python3 coffee_for_me Tony Salesperson -bev=Tea -bev=Coffee -bev=Water -add=Sugar -add=Milk -add=Cinnamon``` to make a sale. Where ```Tony``` is a salesperson's name, ```Salesperson ``` is an employee position, ```-bev=``` is a beverage and ```-add=``` is an ingredient.  You can provide any number of beverages and ingredients arguments.
2. As a Manager run ```python3 coffee_for_me Anna Manager``` to view and export sales records. Where ```Anna``` is a manager's name and ```Manager``` is an employee position.
3. Run ```python3 coffee_for_me -h```  to see Help.

#### Run unit tests
_Note_: Python builtin module ```unittest``` was used for test creation and running.
1. From project root folder navigate to ```cd /coffee_for_me/tests```
2. Run ```python3 -m unittest -b```.
```
Machine_Name:tests user_name$ python3 -m unittest -b
..........................................................
----------------------------------------------------------------------
Ran 58 tests in 0.158s

OK
```
If there are any failures, they will printed to console, e.g.:
```
Machine_Name:tests user_name$ python3 -m unittest -b
......F
Stdout:


...................................................
======================================================================
FAIL: test_argsparser_one_of_pos_args_missing (test_argparser.ArgparserTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/local/Cellar/python3/3.6.4_2/Frameworks/Python.framework/Versions/3.6/lib/python3.6/unittest/mock.py", line 1179, in patched
    return func(*args, **keywargs)
  File "/Users/mikalai_biadrytski/Documents/autotests/CoffeeForMeApp/coffee_for_me/tests/test_argparser.py", line 59, in test_argsparser_one_of_pos_args_missing
    self.assertIn('And the following arguments are required: employee_position', mock_stderr.getvalue())
AssertionError: 'And the following arguments are required: employee_position' not found in 'obligatory args were not supplied bu user: python3 -m unittest - the following arguments are required: employee_position\npython3 -m unittest Error: the following arguments are required: employee_position.\nRun "coffee_for_me -h" to see help.\n'

Stdout:



----------------------------------------------------------------------
Ran 58 tests in 0.160s

FAILED (failures=1)
```

#### Salesperson usage example
```
Hi Liza! You are a salesperson.
You can sell beverages and ingredients

What would you like to do? Enter 1 or 2:
    1 - Sell a beverage
    2 - I am tired... No more sales...
1
Your choice is 1

Would you like to add an ingredient to your beverage?
    1 - Add ingredient
    2 - Don not add ingredient
2
Your choice is 2

You can sell the following beverages:
Water
Soda
Tea
Enter beverage name: 
Soda
Enter beverage price: 
3
You sold 1 beverages and 0 additions
Your sales total amount: 3.0$
Beverage: soda. Price: 3.0$

What would you like to do? Enter 1 or 2:
    1 - Sell a beverage
    2 - I am tired... No more sales...
2
Your choice is 2

Bye-Bye, Liza! See you next time
```

#### Manager usage example
```
Hi James! You are a manager.
You can view and export sales records

What would you like to do? Enter 1 or 2:
        1 - View/export sales records
        2 - No reports today... Maybe later...
1
Your choice is 1

Seller Name                     | Number Of Sales | Total Value ($)
Liza Azil                       | 1               | 3
Total:                          | 1               | 3 

Would you like to export sales records? Enter 1, 2, 3 or 4:
        1 - Export as JSON
        2 - Export as XML
        3 - Export as CSV
        4 - Do not export
1
Your choice is 1

James, your exported json file is in "manager_records" folder

What would you like to do? Enter 1 or 2:
        1 - View/export sales records
        2 - No reports today... Maybe later...
2
Your choice is 2

Bye-Bye, James! See you next time
```