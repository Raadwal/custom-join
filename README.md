# Custom join

## Package manager used
```Bash
Anaconda
```
## Python version
```Bash
Python 3.9.7
```
## Additional packages
```Bash
  absl-py
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
    As file_path the program is accepting only path to csv files conform to the rfc4180. Otherwise some unexpected behaviour may be encountered.
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