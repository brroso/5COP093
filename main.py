import sys  # biblioteca responsável pela manipulação de elementos do sistema
import getopt   # biblioteca utilizada na separação dos argumentos

identificadores = []  # inicialização da lista de identificadores
states = [  # : ( * . > < ' , ; ) = * [ ] { } _ - + a...z 0...9
            [5, 8, 10, 6, 3, 13, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15,
            18, 19, 1, 2],  # q0
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
            -1, -1, 1, 1],  # q1
            [-1, -1, -1, 16, -1 ,-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
            -1, -1, -1, 2],  # q2
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 12, -1, -1, -1, -1 ,-1 ,-1,
            -1, -1, -1, -1],  # q3
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ,-1 ,-1,
            -1, -1, -1, -1],  # q4
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4, -1, -1, -1, -1 ,-1 ,-1,
            -1, -1, -1, -1],  #q5
            [-1, -1, -1, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ,-1 ,-1,
            -1, -1, -1, -1],  # q6
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ,-1 ,-1,
            -1, -1, -1, -1],  # q7
            [-1, -1, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ,-1 ,-1,
            -1, -1, -1, -1],  # q8
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ,-1 ,-1,
            -1, -1, -1, -1],  # q9
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, 11, -1, -1, -1, -1, -1 ,-1 ,-1,
            -1, -1, -1, -1],  # q10
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ,-1 ,-1,
            -1, -1, -1, -1],  # q11
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ,-1 ,-1,
            -1, -1, -1, -1],  # q12
            [-1, -1, -1, -1, 14, -1, -1, -1, -1, -1, 14, -1, -1, -1, -1 ,-1 ,-1,
            -1, -1, -1, -1],  # q13
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ,-1 ,-1,
            -1, -1, -1, -1],  # q14
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ,-1 ,-1,
            -1, -1, -1, -1],  # q15
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ,-1 ,-1,
            -1, -1, -1, 17],  # q16
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ,-1 ,-1,
            -1, -1, -1, -1],  # q17
            [-1, -1, -1, 20, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ,-1 ,-1,
            -1, -1, -1, 18],  # q18
            [-1, -1, -1, 22, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ,-1 ,-1,
            -1, -1, -1, 19],  # q19
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ,-1 ,-1,
            -1, -1, -1, 21],  # q20
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ,-1 ,-1,
            -1, -1, -1, -1],  # q21
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ,-1 ,-1,
            -1, -1, -1, 23],  # q22
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ,-1 ,-1,
            -1, -1, -1, -1],  # q23
            ]
palavras_reservadas = [
                        'and', 'array', 'asm', 'begin', 'case', 'const',
                        'constructor', 'destructor', 'div', 'do', 'downto',
                        'else', 'end', 'file', 'for', 'foward', 'function',
                        'goto','if', 'implementation', 'in', 'inline',
                        'interface', 'label', 'mod', 'nil', 'not', 'object',
                        'of', 'or', 'packed', 'procedure', 'program', 'record',
                        'repeat', 'set', 'shl', 'shr', 'string', 'string',
                        'then', 'to', 'type', 'unit', 'until', 'uses', 'var',
                        'while', 'with', 'xor'
                        ]
special_symbols = [
                    '\'', ',', ';', ')', '=', '[', ']', '{', '}'
                ]
special_symbols2 = [
                    ':', '(', '*', '.', '>', '<', '-', '+'
                    ]
not_final_states = [
                    16,20,22
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
numbers = [
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
            ]

def get_column(c):
    if c == ':':
        return 1
    if c == '(':
        return 2
    if c == '*':
        return 3
    if c == '.':
        return 4
    if c == '>':
        return 5
    if c == '<':
        return 6
    if c == '\\':
        return 7
    if c == ',':
        return 8
    if c == ';':
        return 9
    if c == ')':
        return 10
    if c == '=':
        return 11
    if c == '*':
        return 12
    if c == '[':
        return 13
    if c == ']':
        return 14
    if c == '{':
        return 15
    if c == '}':
        return 16
    if c == '_':
        return 17
    if c == '-':
        return 18
    if c == '+':
        return 19
    if c in letters or c in cap_letters:
        return 20
    if c in numbers:
        return 21


def main(argv):
    # declaração do alfabeto
    for x in states:
        print(x)
    input_file = ''
    output_file = ''

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
        c = f.read(1)
        while c:
            c = f.read(1)
            x = get_column(c)
    output.close()


main(sys.argv[1:])
