import sys  # biblioteca responsável pela manipulação de elementos do sistema
import getopt   # biblioteca utilizada na separação dos argumentos


def main(argv):
    # declaração do alfabeto
    input_file = ''
    output_file = ''
    special_symbols = [
                        '\'', ',', ';', ')', '=', '[', ']', '{', '}'
                        ]
    special_symbols2 = [
                       ':', '(', '*', '.', '>', '<', '-', '+'
                        ]
    letters = [
                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                'm',
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
                ]
    cap_letters = [
                    'A', 'B', 'C', 'D', 'E',  'F', 'G', 'H', 'I', 'J', 'K', 'L'
                    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                    'Y', 'Z'
                    ]
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    try:  # leitura dos argumentos
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
    output = open(output_file, "w")
    with open(input_file, "r") as f:  # roda todo o arquivo char por char
        while True:
            c = f.read(1)
            if not c or c == '\0':
                print('End of file', file=output)
                break
            elif c in special_symbols:
                print(c, 'is a special symbol', file=output)
            elif c in special_symbols2:
                if c == ':':
                    aux = f.read(1)  # coloca no auxiliar a proxima letra
                    if aux == '=':
                        print(c, aux, 'is a double special symbol',
                              file=output)
                    else:
                        print(c, 'is a special symbol', file=output)
                        f.seek(f.tell()-1)  # devolve o ponteiro
                if c == '(':
                    aux = f.read(1)
                    if aux == '*':
                        print(c, aux, 'is a double special symbol',
                              file=output)
                    else:
                        print(c, 'is a special symbol', file=output)
                        f.seek(f.tell()-1)
                if c == '*':
                    aux = f.read(1)
                    if aux == ')':
                        print(c, aux, 'is a double special symbol',
                              file=output)
                    else:
                        print(c, 'is a special symbol', file=output)
                        f.seek(f.tell()-1)
                if c == '.':
                    aux = f.read(1)
                    if aux == '.':
                        print(c, aux, 'is a double special symbol',
                              file=output)
                    else:
                        print(c, 'is a special symbol', file=output)
                        f.seek(f.tell()-1)
                if c == '>':
                    aux = f.read(1)
                    if aux == '=':
                        print(c, aux, 'is a double special symbol',
                              file=output)
                    else:
                        print(c, 'is a special symbol', file=output)
                        f.seek(f.tell()-1)
                if c == '<':
                    aux = f.read(1)
                    if aux == '=' or aux == '>':
                        print(c, aux, 'is a double special symbol',
                              file=output)
                    else:
                        print(c, 'is a special symbol', file=output)
                        f.seek(f.tell()-1)
            elif c in letters:
                print(c, 'is a letter', file=output)
            elif c in cap_letters:
                print(c, 'is a capital letter', file=output)
            elif c in numbers:
                print(c, 'is a number', file=output)
            elif c == ' ':
                print(c, 'is a blank space', file=output)
            elif c == '\n':
                print('this is a \\n', file=output)
            else:
                print(c, 'is not a valid symbol', file=output)
    output.close()


main(sys.argv[1:])
