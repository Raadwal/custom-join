import argparse

from validator import Validator, JoinType
from join import Join

def main():
    # Command line help
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

    
    if validator.join_type is JoinType.INNER:
        Join.inner(validator.first_file_path, validator.second_file_path, validator.colun_name)
    
    if validator.join_type is JoinType.LEFT:
        Join.left(validator.first_file_path, validator.second_file_path, validator.colun_name)
    
    if validator.join_type is JoinType.RIGHT:
        Join.right(validator.first_file_path, validator.second_file_path, validator.colun_name)

if(__name__ == "__main__"):
    main()