import sys  # biblioteca responsável pela manipulação de elementos do sistema
import getopt   # biblioteca utilizada na separação dos argumentos


def main(argv):

    input_file = ''
    output_file = ''
    special_symbols = [
                        '\'', ',', ';', ')', '=', '*', '[', ']', '{', '}', ':',
                        '(', '*', '.', '>', '<', '+', '-'
                        ]
    letters = [
                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm'
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
                ]
    cap_letters = [
                    'A', 'B', 'C', 'D', 'E',  'F', 'G', 'H', 'I', 'J', 'K', 'L'
                    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                    'Y', 'Z'
                    ]
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('main.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
    print('Input file is "', input_file, '"')
    print('Output file is "', output_file, '"')
    with open(input_file) as f:
        while True:
            c = f.read(1)
            if not c:
                print('End of file')
                break
            if c in special_symbols:
                print(c, 'is a special symbol')
            elif c in letters:
                print(c, 'is a letter')
            elif c in cap_letters:
                print(c, 'is a capital letter')
            elif c in numbers:
                print(c, 'is a number')
            elif c == ' ':
                print(c, 'is a blank space')
            elif c == '\n':
                print('this position is a end line')
            else:
                print(c, 'is not a valid symbol')


main(sys.argv[1:])
