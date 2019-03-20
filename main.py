import sys  # biblioteca responsável pela manipulação de elementos do sistema
import getopt   # biblioteca utilizada na separação dos argumentos

identificadores = []  # inicialização da lista de identificadores
states = [  # : ( * . > < ' , ; ) = * [ ] { } _ - + a...z 0...9
            [5, 8, 10, 6, 3, 13, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15,
             18, 19, 1, 2],  # q0
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             1, -1, -1, 1, 1],  # q1
            [-1, -1, -1, 16, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, 2],  # q2
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 12, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, -1],  # q3
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, -1],  # q4
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1],  # q5
            [-1, -1, -1, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, -1],  # q6
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, -1],  # q7
            [-1, -1, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1],  # q8
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, -1],  # q9
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, 11, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, -1],  # q10
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, -1],  # q11
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, -1],  # q12
            [-1, -1, -1, -1, 14, -1, -1, -1, -1, -1, 14, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, -1],  # q13
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, -1],  # q14
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, -1],  # q15
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, 17],  # q16
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, 17],  # q17
            [-1, -1, -1, 20, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, 18],  # q18
            [-1, -1, -1, 22, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, 19],  # q19
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, 21],  # q20
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, 21],  # q21
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, 23],  # q22
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, 23],  # q23
            ]
palavras_reservadas = [
                        'and', 'array', 'asm', 'begin', 'case', 'const',
                        'constructor', 'destructor', 'div', 'do', 'downto',
                        'else', 'end', 'file', 'for', 'foward', 'function',
                        'goto', 'if', 'implementation', 'in', 'inline',
                        'interface', 'label', 'mod', 'nil', 'not', 'object',
                        'of', 'or', 'packed', 'procedure', 'program', 'record',
                        'repeat', 'set', 'shl', 'shr', 'string', 'string',
                        'then', 'to', 'type', 'unit', 'until', 'uses', 'var',
                        'while', 'with', 'xor'
                        ]
special_symbols = [
                    '\'', ',', ';', ')', '=', '[', ']', '{', '}',
                    ':', '(', '*', '.', '>', '<', '-', '+'
                ]
double_special_symbol = [
                    ':=', '(*', '*)', '..', '>=', '<=', '<>'
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
double_special_symbol_states = [
                                4, 9, 11, 7, 12, 14
                            ]
special_symbol_state = 15
positive_number_state = 19
negative_number_state = 18
real_positive_number_state = 23
real_negative_number_state = 21
integer_state = 2
real_number_state = 17
non_final_states = [20, 22, 16]


def print_state(c, cur_state):
    if cur_state == special_symbol_state:
        print(c + ' é símbolo especial', cur_state)
    elif cur_state in double_special_symbol_states:
        print(c + ' é um símbolo especial duplo', cur_state)
    elif cur_state == positive_number_state:
        print(c + ' é um número positivo', cur_state)
    elif cur_state == negative_number_state:
        print(c + ' é um número negativo', cur_state)
    elif cur_state == real_number_state:
        print(c + ' é um número quebrado', cur_state)
    elif cur_state == real_negative_number_state:
        print(c + ' é um número quebrado negativo', cur_state)
    elif cur_state == real_positive_number_state:
        print(c + ' é um número quebrado positivo', cur_state)
    elif cur_state == integer_state:
        print(c + ' é um numero inteiro', cur_state)
    else:
        print(c, 'pertence ao estado', cur_state)


def validation(c):
    if c in special_symbols:
        return 1
    elif c in letters or c in cap_letters:
        return 1
    elif c in numbers:
        return 1
    elif c == ' ' or c == '\n':
        return 1
    else:
        return 0


def get_column(c):
    if c == ':':
        return 0
    elif c == '(':
        return 1
    elif c == '*':
        return 2
    elif c == '.':
        return 3
    elif c == '>':
        return 4
    elif c == '<':
        return 5
    elif c == '\\':
        return 6
    elif c == ',':
        return 7
    elif c == ';':
        return 8
    elif c == ')':
        return 9
    elif c == '=':
        return 10
    elif c == '*':
        return 11
    elif c == '[':
        return 12
    elif c == ']':
        return 13
    elif c == '{':
        return 14
    elif c == '}':
        return 15
    elif c == '_':
        return 16
    elif c == '-':
        return 17
    elif c == '+':
        return 18
    elif c in letters or c in cap_letters:
        return 19
    elif c in numbers:
        return 20
    else:
        return -1


def main(argv):
    # declaração do alfabeto
    cur_state = 0
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
        text = f.read()
        token = ''
        known = []
        for ind, atom in enumerate(text[:-1]):
            print('lido', atom, 'no estado atual', cur_state)
            if ind in known:
                continue
            if atom == ' ':
                if cur_state != 0 and cur_state not in non_final_states:
                    print_state(token, cur_state)
                    cur_state = 0
                    token = ''
                    continue
                if cur_state in non_final_states:
                    break
                continue
            if not validation(atom):
                print('ERRO!', atom, 'é um caracter invalido')
                cur_state = 0
                break
            col = get_column(atom)
            state = states[int(cur_state)][int(col)]
            if state == -1:
                print('codar aqui')
            else:
                token = token + atom
                cur_state = state
    if cur_state in non_final_states:
        print('ERRO!', token, 'não é um token válido.')
    elif cur_state != 0:
        print_state(token, cur_state)
    print('FIM')
    output.close()


main(sys.argv[1:])
