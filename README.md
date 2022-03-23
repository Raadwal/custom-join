# Custom join

## Package manager used
```Bash
Anaconda
```
## Python version
```Bash
Python 3.10.0
```
## Brief Description
### 1. What the program does?
The program is designed to read two csv files and join them using a specified column. Files can be bigger than memory available on the machine. The result is written to the standard output.
### 2. How to run the program?
#### a) You can simply download source files and run command:
```Bash
python main.py file_path file_path column_name join_type
```

### Mandatory arguments:
- ```Bash
  file_path
  ```
    As file_path the program is accepting only path to csv files conform to the rfc4180. Otherwise, some unexpected behavior may be encountered.
- ```Bash
  column_name
  ```
    This argument specified which column will be used for joining two files together


### Nonmandatory argumet:
 ```Bash
join_type
```
Which type of join will be used. If none is specified the inner join will be used. It's the simples and most common form of join is inner join, also SQL uses inner join as default join type. 

How to specified join type?
```Bash
inner|left|right
```

### Example usage:
```Bash
python main.py important_data.csv other_data.csv ID left
```

### How the program works on inner join example:
We have two files: first_data.csv second_data.csv
- Firstly we are dividing second file into many small ones, each one has certain numbers of lines (CHUNK SIZE variable).
- Secondly we are creating dictionary where keys are indexes of column given by user and values are lists of files which contains given indexes.
- Thirdly we are reading first file one row at the time, we are checking value of key column and checking in dictionary in which files we can find matching rows.
- At the end we are using multithreading for searching rows in each files and we are printing it

### Python libraries that are perfect for joining two large CSV files:
```Bash
  Dask, Pandas, NumPy
```