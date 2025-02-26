import json
import sys
import csv

from faker import Faker


class FixedWithFileParser:
    """

    """
    DELIMITER = ","
    QUOTECHAR = '"'
    QUOTING = csv.QUOTE_MINIMAL

    def __init__(self, spec_file):

        self.load_spec(spec_file)


    def load_spec(self, spec_file):

        with open(spec_file, 'r') as f:
            spec = json.load(f)
            self.cols = {}
            for i in range(len(spec['ColumnNames'])):
                self.cols[spec['ColumnNames'][i]] = int(spec['Offsets'][i])
            
            self.fixed_encoding = spec['FixedWidthEncoding']
            self.include_header = spec['IncludeHeader'].lower() == 'true'
            self.delimited_encoding = spec['DelimitedEncoding']
            
         

    def to_fixed(self, infile, outfile=None):

        with open(infile, 'r', encoding=self.delimited_encoding) as csv_file, \
            open(outfile, 'w', encoding=self.fixed_encoding) if outfile is not None else sys.stdout as fixed_file:

            reader = csv.DictReader(csv_file, fieldnames=self.cols.keys(), delimiter=self.DELIMITER, quotechar=self.QUOTECHAR, quoting=self.QUOTING)

            if self.include_header:
                fixed_file.write(self.fixed_header + "\n")
                next(reader) # ignore csv header
                      
            for row in reader:
                data = ""
                for col, width in self.cols.items():
                    data += row[col][:width].ljust(width)
                fixed_file.write(data + "\n")

            
    def to_csv(self, infile, outfile=None):
        
        with open(infile, 'r', encoding=self.fixed_encoding) as fixed_file, \
            open(outfile, 'w', newline='', encoding=self.delimited_encoding) if outfile is not None else sys.stdout as csv_file:
            
            writer = csv.DictWriter(csv_file, fieldnames=self.cols.keys(), delimiter=self.DELIMITER, quotechar=self.QUOTECHAR, quoting=self.QUOTING)
            
            if self.include_header:
                writer.writeheader()
                fixed_file.readline() # ignore header of fixed
            
            for line in fixed_file:
                row = {}
                start_index = 0
                for col, width in self.cols.items():
                    row[col] = line[start_index:start_index+width].rstrip()
                    start_index += width
                writer.writerow(row)
            
            
    def rand_fixed(self, outfile=None, lines=100):
        """
        Generate a fixed width file with random column values
        """
        
        with open(outfile, 'w', encoding=self.fixed_encoding) if outfile is not None else sys.stdout as fixed_file:
            
            fake = Faker()
            
            if self.include_header:
                fixed_file.write(self.fixed_header + "\n")
            
            for _ in range(lines):
                data = ""
                for width in self.cols.values():
                    data += fake.word()[:width].ljust(width)
                fixed_file.write(data + "\n")
    
    
    @property
    def fixed_header(self):
        header = ""
        for col, width in self.cols.items():
            header += col[:width].ljust(width)
        return header

