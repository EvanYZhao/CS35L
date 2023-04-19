#!/usr/bin/python3

import random, argparse, string, sys

class shuf:
    # Initialize with infile, echo, and input_range
    # Constructor should create a string with words to be shuffled
    def __init__(self, infile, echo, input_range):
        self.lines=[]
        if infile and infile != "-":
            for line in infile:
                self.lines.append(line.strip())
        if echo:
            for n in echo:
                self.lines.append(str(n))
        if input_range: # Process the range by splitting with '-' delimiter
            start, end = input_range.split('-', 1)[0], input_range.split('-', 1)[1]
            try:
                start = int(start)
            except ValueError:
                print('Not a valid input', start)
                exit()
            try:
                end = int(end)
            except ValueError:
                print('Not a valid input', end)
                exit()
            newRange = range(start, end + 1)
            for n in newRange:
                self.lines.append(str(n))
        if (not infile or infile == "-") and not echo and not input_range:
            self.lines=[]
    
    # Shuffle function should with repeat and head_count parameters
    # Should perform the shuffling for head_count amount of lines based on repeat value
    def shuffle(self, repeat, head_count):
        try:
            numLines = int(head_count)
        except:
            numLines = len(self.lines)
        if numLines < 0:
            print("negative count:", numLines)
            exit()
        if repeat and not head_count:
            while True:
                line = random.choice(self.lines)
                print(line)
        elif repeat:
            for i in range(numLines):
                line = random.choice(self.lines)
                print(line)
        else:
            lines = random.sample(self.lines, numLines)
            for line in lines:
                print(line)
        
def main():
    # Creating the parser for shuf
    parser = argparse.ArgumentParser(description="generates random permutation of lines")
    
    # Adding arguments to the parser
    parser.add_argument("infile", help="enter a file to read from", default=None, nargs="?")
    
    # Group creation to prevent i and e from being called together
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--echo", "-e", help="treat each ARG as an input line", nargs="*")
    group.add_argument("--input-range","-i", help="treat each number LO through HI as an input line")
    
    # Adding more arguments to parser
    parser.add_argument("--head-count", "-n", help="output at most COUNT lines", type=int)
    parser.add_argument("--repeat", "-r", help="output lines can be repeated", action="store_true")
    
    # Parsing the args Namespace(infile, echo, input_range, head_count, repeat)
    args = parser.parse_args()
    
    # Creating the shuf object with the args
    obj = shuf(args.infile, args.echo, args.input_range)
    
    # Printing occurs within this member function
    obj.shuffle(args.repeat, args.head_count)
    
if __name__ == "__main__":
    main()
    
