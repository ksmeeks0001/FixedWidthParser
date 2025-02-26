import argparse

from fixed_width_parser import FixedWithFileParser


def parse_args():

    parser = argparse.ArgumentParser(description="Convert to and from csv and fixed width file per spec file")
    parser.add_argument('conversion', choices=['csv', 'fixed'], help='Set the file conversion type')
    parser.add_argument('infile', type=str, help='File to convert')
    parser.add_argument('--spec', '-s', type=str, help='json file with fixed width spec', default='spec.json')
    parser.add_argument('--outfile', '-o', type=str, help='File to write conversion to')

    args = parser.parse_args()

    return args.conversion, args.infile, args.spec, args.outfile


def main():
    """
    Convert a file to/from csv and fixed width per specification file
    """
    conversion, infile, spec, outfile = parse_args()

    parser = FixedWithFileParser(spec)
    
    if conversion == 'csv':
        parser.to_csv(infile, outfile)
    elif conversion == 'fixed':
        parser.to_fixed(infile, outfile)
            
            
if __name__ == '__main__':

    main()
    

    