# Fixed Width Parser

Convert files from csv to a fixed width specification and back.   

#### setup
Faker is the only external dependency for generating random data
```
pip install faker
```

To run tests and regenerate example files with random data simply execute tests.py   


example usage    

```
python3 convert.py csv test_output/test_fixed.txt
python3 convert.py fixed test_output/test.csv
```