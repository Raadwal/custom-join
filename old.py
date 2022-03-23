@staticmethod
    def inner(first_file_path:str, second_file_path:str, column:str):
        join = Join()
        """
        first_key_column = join.check_column_number(first_file_path, column)
        second_key_column = join.check_column_number(second_file_path, column)      
        """
        first_csv_file = open(first_file_path, "r")
        first_reader = csv.DictReader(first_csv_file)
        # Because headears are in first (0) row
        first_chunk_start = 1

        second_csv_file = open(second_file_path, "r")
        second_reader = csv.DictReader(second_csv_file)
        # Because headears are in first (0) row
        second_chunk_start = 1

        current_first_size = 0
        current_second_size = 0

        """
        first_test = []
        for row in first_reader:
            first_test.append(row)

        second_test = []
        for row in second_reader:
            second_test.append(row)

        keys_printed = False
        for f_element in first_test:
            for s_element in second_test:
                if keys_printed == False:
                    print(list((f_element | s_element).keys()))
                    keys_printed = True

                if f_element[column] == s_element[column]:
                    print(list((f_element | s_element).values()))
        """
        keys_printed = False
        count = 0
        for f_row in first_reader:
            second_csv_file.seek(0)
            second_reader = csv.DictReader(second_csv_file)
            for s_row in second_reader:
                if keys_printed == False:
                    print(list((f_row | s_row).keys()))
                    keys_printed = True

                if f_row[column] == s_row[column]:
                    print(list((f_row | s_row).values()))

        print(count)

    @staticmethod
    def left(first_file_path:str, second_file_path:str, column:str):
        join = Join()

        first_csv_file = open(first_file_path, "r")
        first_reader = csv.DictReader(first_csv_file)

        second_csv_file = open(second_file_path, "r")
        second_reader = csv.DictReader(second_csv_file)

        first_test = []
        for row in first_reader:
            first_test.append(row)

        second_test = []
        for row in second_reader:
            second_test.append(row)

        keys_printed = False
        second_file_keys = {}
        for f_element in first_test:
            found = False
            for s_element in second_test:
                if keys_printed == False:
                    print(list((f_element | s_element).keys()))
                    second_file_keys = s_element
                    for key, value in second_file_keys.items():
                        second_file_keys[key] = "NULL"
                    keys_printed = True

                if f_element[column] == s_element[column]:
                    print(list((f_element | s_element).values()))
                    found = True
            
            if not found:
                key_copy = f_element[column]
                tmp_dict = f_element | second_file_keys
                tmp_dict[column] = key_copy
                print(list(tmp_dict.values()))
        
    @staticmethod
    def right(first_file_path:str, second_file_path:str, column:str):
        join = Join()

        first_csv_file = open(first_file_path, "r")
        first_reader = csv.DictReader(first_csv_file)

        second_csv_file = open(second_file_path, "r")
        second_reader = csv.DictReader(second_csv_file)

        first_test = []
        for row in first_reader:
            first_test.append(row)

        second_test = []
        for row in second_reader:
            second_test.append(row)

        keys_printed = False
        first_file_keys = {}
        for s_element in second_test:
            found = False

            for f_element in first_test:
                if keys_printed == False:
                    print(list((f_element | s_element).keys()))
                    first_file_keys = f_element
                    for key, value in first_file_keys.items():
                        first_file_keys[key] = "NULL"
                    keys_printed = True

                if f_element[column] == s_element[column]:
                    print(list((f_element | s_element).values()))
                    found = True

            if not found:
                key_copy = s_element[column]
                tmp_dict = first_file_keys | s_element
                tmp_dict[column] = key_copy
                print(list(tmp_dict.values()))