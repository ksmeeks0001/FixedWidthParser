import unittest
import csv

from fixed_width_parser import FixedWithFileParser


class FixedWidthTests(unittest.TestCase):

    def setUp(self):
        
        self.parser = FixedWithFileParser("spec.json")
        
        self.fixed_file = "test_output/test_fixed.txt"
        self.csv_file = "test_output/test.csv"
        self.back_fixed_file = "test_output/test_fixed2.txt"
        
        self.parser.rand_fixed(self.fixed_file, lines=100) # fixed width file random column values
        self.parser.to_csv(self.fixed_file, self.csv_file) # convert fixed width to csv
        self.parser.to_fixed(self.csv_file, self.back_fixed_file) # convert the csv back to fixed width
    
    def test_fixed_header(self):
        """
        Check header line of fixed width file is as expected per spec.json
        """
        expected_header = "f1   f2          f3 f4f5           f6     f7        f8           f9                  f10          "
        with open(self.fixed_file, 'r', encoding=self.parser.fixed_encoding) as fixed_file:
            read_header = fixed_file.readline()
        self.assertEqual(expected_header, self.parser.fixed_header, read_header)
        
    def test_line_length(self):
        """
        Each line of the fixed width file should have length equal to sum of column lengths
        """
        lens = []
        with open(self.fixed_file, 'r', encoding=self.parser.fixed_encoding) as fixed_file:
            for line in fixed_file:
                lens.append(len(line))
        expected_length = sum(self.parser.cols.values()) + 1 # for new line char
        
        self.assertEqual(expected_length, min(lens), max(lens))
        
    def test_csv(self):
        """
        Test accuracy of csv output
        """
        with open(self.csv_file, 'r', newline='', encoding=self.parser.delimited_encoding) as csv_file, \
            open(self.fixed_file, 'r', encoding=self.parser.fixed_encoding) as fixed_file:
            
            reader = csv.DictReader(csv_file, delimiter=FixedWithFileParser.DELIMITER, quotechar=FixedWithFileParser.QUOTECHAR, quoting=FixedWithFileParser.QUOTING)
        
            # header of csv should have correct column names
            self.assertEqual(reader.fieldnames, list(self.parser.cols.keys()))
            
            fixed_file.readline() # throw away header
            fixed_line = fixed_file.readline().rstrip("\n")
            csv_line = next(reader)
            
            expected_fixed_line = ""
            for col, value in csv_line.items():
                expected_fixed_line += csv_line[col].ljust(self.parser.cols[col])
                
            self.assertEqual(fixed_line, expected_fixed_line)
            

    def test_fixed_convert(self):
        """
        test the csv file converted to fixed width matches the original fixed width file
        """
        
        with open(self.fixed_file, 'rb') as f1, open(self.back_fixed_file, 'rb') as f2:
            
            while True:
                b1 = f1.read(4096)
                b2 = f2.read(4096)
                
                self.assertEqual(b1, b2)
                
                if not b1:  # End of file
                    return
    
if __name__ == "__main__":

    unittest.main()