import argparse
from typing import Optional
from typing import Sequence

from validator import *

def main():
    parser = argparse.ArgumentParser(description="""
        The program is designed to read two csv files and join them using a specified column.
        Files can be bigger than memory available on the machine. The result is written to the standard output.
        """)
    parser.add_argument('first_file_path', help='path to first csv file')
    parser.add_argument('second_file_path',  help='path to second csv file')
    parser.add_argument('column_name', help='column used to join two files')
    parser.add_argument('join_type', help='inner|left|right - if none is specified inner join will be used', nargs='?', default='inner')

    args = parser.parse_args()

    validator = Validator(args.first_file_path, args.second_file_path, args.column_name, args.join_type)
    validator.info()

    return 0


if(__name__ == "__main__"):
    main()