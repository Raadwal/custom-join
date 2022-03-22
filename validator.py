import sys
import csv
from enum import Enum

"""
Enum type representing join type
"""
class JoinType(Enum):
    INNER = 0
    LEFT = 1
    RIGHT = 2


"""
Class responsible for validating given starting arguments.
If everything is correct we can use member variables:
first_file_path - string
second_file_path - string
column_name - string
join_type - int
"""
class Validator:

    def __init__(self, first_file_path:str, second_file_path:str, column_name:str, join_type:str):
        """
        Firstly we are checking if both csv files are valid and conform to rfc 4810.         
        If they are incorrect there is no point to checking if they contains given column.
        """
        if(self.is_csv_valid(first_file_path)):
            self.first_file_path = first_file_path
        
        if(self.is_csv_valid(second_file_path)):
            self.second_file_path = second_file_path

        """
        Checking if given column exists.
        """
        if(self.is_column_valid(column_name)):
            self.colun_name = column_name

        """
        Checking if correct join type was entered and converting it to Enum type.
        0 - inner join
        1 - left join
        2 - right join
        """
        self.join_type = self.get_join_type(join_type)
    
    """
    Checking if join type matches one of the above: inner, left, right.
    If join type is correct function returning Enum value, if not program ends.

    join_type - string represtenting join type
    """
    def get_join_type(self, join_type: str):
        match(join_type.lower()):
            case "inner":
                return JoinType.INNER
            case "left":
                return JoinType.LEFT
            case "right":
                return JoinType.RIGHT
            case _:
                print("Wrong join type! Allowed: inner, left, right")
                sys.exit(1)

    """
    Checking if given file is valid:
        - checking extension of the file
        - checking path to the file
        - checking if file matches standard rfc4180
    """
    def is_csv_valid(self, path:str):
        if not path.endswith('.csv'):
            print("Program is accepting only csv files!")
            exit(1)
        
        try:
            open(path)
        except FileNotFoundError:
            print("Given file doesn't exist: " + path)
            exit(1)

        return True

    """
    Checking if column given as argument exists in both files
    """
    def is_column_valid(self, column:str):
        first_file_columns = []
        second_file_columns = []

        with open(self.first_file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter = ',')

            for row in csv_reader:
                first_file_columns = row
                break

        with open(self.second_file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter = ',')

            for row in csv_reader:
                second_file_columns = row
                break

        if not column in first_file_columns:
            print("First file doesn't contain given column")
            exit(1)

        if not column in second_file_columns:
            print("Second file doesn't contain given column")
            exit(1)

        return True

    def info(self):
        print("========================================")
        print(f"First file name: {self.first_file_path}")
        print(f"Second file name: {self.second_file_path}")
        print(f"Column name: {self.colun_name}")
        print(f"Join type: {self.join_type}")
        print("========================================")
        
