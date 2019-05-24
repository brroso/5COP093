import sys
import getopt
import re

# reserved_word = 0
# special_symbol = 1
# double_special_symbol = 2
# integer_number = 3
# float_number = 4
# positive_float_number = 5
# negative_float_number = 6
# identifier = 7

keywords = [
    'AND', 'ARRAY', 'ASM', 'BEGIN', 'CASE',
    'CONST', 'CONSTRUCTOR', 'CONTINUE', 'DESTRUCTOR',
    'DIV', 'DO', 'DOWNTO', 'ELSE', 'END', 'FILE',
    'FOR', 'FUNCTION', 'GOTO', 'IF', 'IMPLEMENTATION',
    'IN', 'INLINE', 'INTERFACE', 'LABEL', 'MOD', 'NIL',
    'NOT', 'OBJECT', 'OF', 'OR', 'INHERITED',
    'PACKED', 'PROCEDURE', 'PROGRAM', 'RECORD', 'REPEAT',
    'SET', 'SHL', 'SHR', 'STRING', 'THEN', 'TO', 'TRUE',
    'TYPE', 'UNIT', 'UNTIL', 'USES', 'VAR', 'WHILE',
    'WITH', 'XOR',
]


class Token(object):
    def __init__(self, name, category):
        self.name = name
        self.category = category

    def getName(self):
        return self.name

    def getCat(self):
        return self.category


class Parser:
    def __init__(self, token_list):
        self.token_list = token_list
        self.index = 0
        self.atual = token_list[self.index].getName().upper()

    def next_token(self):
        self.index += 1
        self.atual = self.token_list[self.index].upper()

    def start_parse(self):
        if self.atual == 'PROGRAM':
            self.next_token()
        else:
            return 'erro'


def main(argv):
    # Leitura dos argumentos
    token_list = []
    try:    # Lê os argumentos
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
    # output = open(output_file, "w")
    with open(input_file, "r") as f:   # Roda todo o arquivo char por char
        lines = f.readlines()
        for line in lines:  # Coloca os tokens e suas categorias em token_list
            line = line.rstrip()
            if 'categoria' in line:
                category = line.split("da categoria ", 1)[1]
                name = line.split("da categoria ", 1)[0]
                name = name.rstrip()
                newtoken = Token(name, category)
                token_list.append(newtoken)
    parser = Parser(token_list)
    parser.start_parse()
    if parser == 'erro':
        print('Erro sintático')
        return None


main(sys.argv[1:])
