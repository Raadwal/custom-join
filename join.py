import csv
import os
from threading import Thread
from collections import defaultdict

class Join:
    # Path to tmp folder where divided file will be stored
    PATH_TO_TMP = "tmp"
    # Number of lines in each temporary file
    CHUNK_SIZE = 10000

    @staticmethod
    def inner(first_file_path:str, second_file_path:str, column:str):
        join = Join()

        join.create_tmp_folder()
        # Dividing second file into smaller ones
        join.divide_csv_file(second_file_path)

        # Hashing
        # Key: column ID, value files in which given key exists
        hash_table = defaultdict(list)
        for chunk_path in join.chunk_paths:
            with open(chunk_path, "r") as csv_chunk:
                csv_reader = csv.DictReader(csv_chunk)
                for row in csv_reader:
                    hash_table[row[column]].append(chunk_path)

        
        with open(first_file_path, "r") as csv_first:
            csv_first_reader = csv.DictReader(csv_first)
            first_row = True
            first_headers = []

            # Reading first file row by row
            for row in csv_first_reader:
                if first_row:
                    first_headers = list(row.keys())
                    first_row = False
                    # Printing headers - removing duplicated column
                    print(*(first_headers+[i for i in join.second_headers if i not in first_headers]), sep=',')

                # Checking hash_table for files with given key
                files_list = hash_table[row[column]]
                # Removing duplicates from the list
                files_list = list(defaultdict.fromkeys(files_list))

                # Searching for rows in files (each file = one thread)
                if not files_list == []:
                    threads = [None] * len(files_list)
                    results = [None] * len(files_list)
                    for index in range(len(files_list)):
                        threads[index] = Thread(target=join.find_rows_inner_left, args=[files_list[index], row, column, results, index])
                        threads[index].start()

                    for index in range(len(files_list)):
                        results.append(threads[index].join())
                        
                    for result in results:
                        if not result == None:
                            for r in result:
                                print(*r, sep=',')

        join.delete_tmp_folder()

    @staticmethod
    def left(first_file_path:str, second_file_path:str, column:str):
        join = Join()

        join.create_tmp_folder()
        # Dividing second file into smaller ones
        join.divide_csv_file(second_file_path)
        # Creating dictionary with empty values
        null_dict = {}
        for header in join.second_headers:
            null_dict[header] = 'NULL'

        # Hashing
        # Key: column ID, value files in which given key exists
        hash_table = defaultdict(list)
        for chunk_path in join.chunk_paths:
            with open(chunk_path, "r") as csv_chunk:
                csv_reader = csv.DictReader(csv_chunk)
                for row in csv_reader:
                    hash_table[row[column]].append(chunk_path)

        
        with open(first_file_path, "r") as csv_first:
            csv_first_reader = csv.DictReader(csv_first)
            first_row = True
            first_headers = []

            # Reading first file row by row
            for row in csv_first_reader:
                if first_row:
                    first_headers = list(row.keys())
                    first_row = False
                    # Printing headers - removing duplicated column
                    print(*(first_headers+[i for i in join.second_headers if i not in first_headers]), sep=',')

                # Checking hash_table for files with given key
                files_list = hash_table[row[column]]
                # Removing duplicates from the list
                files_list = list(defaultdict.fromkeys(files_list))

                # Searching for rows in files (each file = one thread)
                if not files_list == []:
                    threads = [None] * len(files_list)
                    results = [None] * len(files_list)
                    for index in range(len(files_list)):
                        threads[index] = Thread(target=join.find_rows_inner_left, args=[files_list[index], row, column, results, index])
                        threads[index].start()

                    for index in range(len(files_list)):
                        results.append(threads[index].join())
                        
                    for result in results:
                        if not result == None:
                            for r in result:
                                print(*r, sep=',')
                else:
                    # Headers from second file without key column
                    key_copy = row[column]
                    tmp_dict = row | null_dict
                    tmp_dict[column] = key_copy
                    print(*(tmp_dict.values()), sep=',')


        join.delete_tmp_folder()

    @staticmethod
    def right(second_file_path:str, first_file_path:str, column:str):
        join = Join()

        join.create_tmp_folder()
        # Dividing second file into smaller ones
        join.divide_csv_file(second_file_path)
        # Creating dictionary with empty values
        null_dict = {}
        for header in join.second_headers:
            null_dict[header] = 'NULL'
        
        null_dict.pop(column)

        # Hashing
        # Key: column ID, value files in which given key exists
        hash_table = defaultdict(list)
        for chunk_path in join.chunk_paths:
            with open(chunk_path, "r") as csv_chunk:
                csv_reader = csv.DictReader(csv_chunk)
                for row in csv_reader:
                    hash_table[row[column]].append(chunk_path)

        
        with open(first_file_path, "r") as csv_first:
            csv_first_reader = csv.DictReader(csv_first)
            first_row = True
            first_headers = []

            # Reading first file row by row
            for row in csv_first_reader:
                if first_row:
                    first_headers = list(row.keys())
                    first_row = False
                    # Printing headers
                    tmp_list = (join.second_headers + first_headers)
                    tmp_list.reverse()
                    tmp_list = list(dict.fromkeys(tmp_list))
                    tmp_list.reverse()
                    print(*tmp_list, sep=',')

                # Checking hash_table for files with given key
                files_list = hash_table[row[column]]
                # Removing duplicates from the list
                files_list = list(defaultdict.fromkeys(files_list))

                # Searching for rows in files (each file = one thread)
                if not files_list == []:
                    threads = [None] * len(files_list)
                    results = [None] * len(files_list)
                    for index in range(len(files_list)):
                        threads[index] = Thread(target=join.find_rows_right, args=[files_list[index], row, column, results, index])
                        threads[index].start()

                    for index in range(len(files_list)):
                        results.append(threads[index].join())
                        
                    for result in results:
                        if not result == None:
                            for r in result:
                                print(*r, sep=',')
                else:
                    # Headers from second file without key column
                    print(*(list(null_dict.values()) + list(row.values())), sep=',')


        join.delete_tmp_folder()

    def create_tmp_folder(self):
        if not os.path.exists(self.PATH_TO_TMP):
            os.mkdir(self.PATH_TO_TMP)


    def delete_tmp_folder(self):
        for root, dirs, files in os.walk(self.PATH_TO_TMP, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        
        os.rmdir(self.PATH_TO_TMP)

    def divide_csv_file(self, path):
        self.chunk_paths = []
        rows_counter = 0
        chunk_number = 0

        first_row = True

        with open(path) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            rows = []

            for row in csv_reader:      
                if first_row:
                    self.second_headers = list(row.keys())
                    first_row = False

                if rows_counter >= self.CHUNK_SIZE:
                    self.write_chunk_file(rows, chunk_number)

                    rows_counter = 0
                    chunk_number += 1
                    rows = []

                rows.append(row)
                rows_counter += 1

            if not rows == []:
                self.write_chunk_file(rows, chunk_number)

                
    def write_chunk_file(self, lines:list, chunk_number:int):
        chunk_path = self.PATH_TO_TMP + f"/chunk_{chunk_number}.csv"
        self.chunk_paths.append(chunk_path)
        with open(chunk_path, "w", newline="") as chunk_file:
            csv_writer = csv.DictWriter(chunk_file, fieldnames=self.second_headers)
            csv_writer.writeheader()

            for line in lines:
                csv_writer.writerow(line)

    def find_rows_inner_left(self, chunk, row, column, result, index):
        tmp_result = []
        with open(chunk, "r") as csv_chunk:
            chunk_reader = csv.DictReader(csv_chunk)

            for chunk_row in chunk_reader:
                if row[column] == chunk_row[column]:
                    tmp_result.append(list((row | chunk_row).values()))

        result[index] = tmp_result

    def find_rows_right(self, chunk, row, column, result, index):
        tmp_result = []
        with open(chunk, "r") as csv_chunk:
            chunk_reader = csv.DictReader(csv_chunk)

            for chunk_row in chunk_reader:
                if row[column] == chunk_row[column]:
                    chunk_row.pop(column)
                    tmp_result.append(list((chunk_row | row).values()))

        result[index] = tmp_result