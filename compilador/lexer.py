import sys  # biblioteca responsável pela manipulação de elementos do sistema
import getopt   # biblioteca utilizada na separação dos argumentos
import hash_table as ht  # biblioteca da hash_table
import re


class record:
    def __init__(self, token, category):
        self.token = token
        self.category = category

    def getToken(self):
        return self.token

    def getCategory(self):
        return self.category


class identifier:
    """Identifier object"""

    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name


identificadores = []  # inicialização da lista de identificadores
states = [  # : ( * . > < ' , ; ) = * [ ] { } _ - + a...z 0...9 /
            [5, 8, 10, 6, 3, 13, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 0,
             18, 19, 1, 2, 15],  # q0
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             1, -1, -1, 1, 1, -1],  # q1
            [-1, -1, -1, 16, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, 2, -1],  # q2
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 12, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, -1, -1],  # q3
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, -1, -1],  # q4
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, -1],  # q5
            [-1, -1, -1, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, -1, -1],  # q6
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, -1, -1],  # q7
            [-1, -1, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, -1],  # q8
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, -1, -1],  # q9
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, 11, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, -1, -1],  # q10
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, -1, -1],  # q11
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, -1, -1],  # q12
            [-1, -1, -1, -1, 14, -1, -1, -1, -1, -1, 14, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, -1, -1],  # q13
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, -1, -1],  # q14
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, -1, -1],  # q15
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, 17, -1],  # q16
            [-1, -1, -1, -1, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, 17, -1],  # q17
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, 20, -1],  # q18
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, 22, -1],  # q19
            [-1, -1, -1, 21, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, -1, -1],  # q20
            [-1, -1, -1, -1, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, 24, -1],  # q21
            [-1, -1, -1, 23, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, -1, -1],  # q22
            [-1, -1, -1, -1, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, 25, -1],  # q23
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, 24, -1],  # q24
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
             -1, -1, -1, -1, 25, -1],  # q25
            ]
palavras_reservadas = [
                        'AND', 'ARRAY', 'ASM', 'BEGIN', 'CASE',
                        'CONST', 'CONSTRUCTOR', 'CONTINUE', 'DESTRUCTOR',
                        'DIV', 'DO', 'DOWNTO', 'ELSE', 'END', 'FILE',
                        'FOR', 'FUNCTION', 'GOTO', 'IF', 'IMPLEMENTATION',
                        'IN', 'INLINE', 'INTERFACE', 'LABEL', 'MOD', 'NIL',
                        'NOT', 'OBJECT', 'OF', 'OR', 'INHERITED',
                        'PACKED', 'PROCEDURE', 'PROGRAM', 'RECORD', 'REPEAT',
                        'SET', 'SHL', 'SHR', 'STRING', 'THEN', 'TO', 'TRUE',
                        'TYPE', 'UNIT', 'UNTIL', 'USES', 'VAR', 'WHILE',
                        'WITH', 'XOR', 'and', 'array', 'asm', 'begin', 'case',
                        'const', 'constructor', 'continue', 'destructor',
                        'div', 'do', 'downto', 'else', 'end', 'file',
                        'for', 'function', 'goto', 'if', 'implementation',
                        'in', 'inline', 'interface', 'label', 'mod', 'nil',
                        'not', 'object', 'of', 'or', 'inherited',
                        'packed', 'procedure', 'program', 'record', 'repeat',
                        'set', 'shl', 'shr', 'string', 'then', 'to', 'true',
                        'type', 'unit', 'until', 'uses', 'var', 'while',
                        'with', 'xor'
                        ]

special_symbols = [
                    '\'', '/', ',', ';', ')', '=', '[', ']', '{', '}',
                    ':', '(', '*', '.', '>', '<', '-', '+', '_'
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
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                'A', 'B', 'C', 'D', 'E',  'F', 'G', 'H', 'I', 'J', 'K', 'L',
                'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                'Y', 'Z'
                ]
numbers = [
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
            ]
identif_state = 1
integer_state = 2
special_symbol_states = [
                        3, 5, 6, 8, 10, 13, 15, 18, 19
                        ]
double_special_symbol_states = [
                                4, 7, 9, 11, 12, 14
                                ]
real_number_state = 17
negative_number_state = 20
positive_number_state = 22
non_final_states = [21, 23, 16]
real_positive_number_state = 25
real_negative_number_state = 24


def removeComments(code):
    regex = re.compile(r"\(\*.*?\*\)", re.DOTALL)
    code = re.sub(regex, "", code)
    return code


# Identifica o estado dado
def get_state_string(state):
    if state == identif_state:
        return 'identificador'
    elif state == integer_state:
        return 'numero inteiro'
    elif state in special_symbol_states:
        return 'simbolo especial'
    elif state in double_special_symbol_states:
        return 'simbolo especial composto'
    elif state == real_number_state:
        return 'numero real'
    elif state == negative_number_state:
        return 'numero negativo'
    elif state == positive_number_state:
        return 'numero positivo'
    elif state == real_positive_number_state:
        return 'numero real positivo'
    elif state == real_negative_number_state:
        return 'numero real negativo'


#  Checa se o símbolo válido pertence ao alfabeto
def validation(c):
    if c in special_symbols:
        return 1
    elif c in letters or c in cap_letters:
        return 1
    elif c in numbers:
        return 1
    elif c == ' ' or c == '\n' or c == '	':
        return 1
    else:
        return 0


#  Pega a coluna respectiva ao caracter lido na matriz de transições
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
    elif c == '\'':
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
    elif c == '/':
        return 21
    else:
        return -1


def main(argv):
    records_list = []
    table = ht.new_table()
    cur_state = 0
    input_file = ''
    output_file = ''
    try:   # Leitura dos argumentos
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
    with open(input_file, "r") as f:   # Roda todo o arquivo char por char
        text = f.read()
        text = removeComments(text)
        erro = ''
        token = ''
        linha = 1
        for atom in text:
            if atom == '_' and cur_state != 1:
                erro = 'é um caracter inválido no contexto. '
                cur_state = 0
                break
            # Se o caracter for um espaço
            if atom == ' ' or atom == '\n' or atom == '	':
                # Se o token for palavra reservada
                if atom == '\n':
                    linha = linha + 1
                if token.lower() in palavras_reservadas:
                    rec = record(token, 'palavra reservada')
                    records_list.append(rec)
                    cur_state = 0
                    token = ''
                    continue
                # Se o token acaba em um estado final:
                if cur_state != 0 and cur_state not in non_final_states:
                    if cur_state == identif_state:
                        rec = record(token, get_state_string(cur_state))
                        records_list.append(rec)
                        if ht.hash_search(table, token) != -1:
                            token = atom
                            col = get_column(atom)
                            cur_state = states[0][int(col)]
                        else:
                            ident = identifier(token)
                            ht.hash_insert(table, ident)
                            token = atom
                            col = get_column(atom)
                            cur_state = states[0][int(col)]
                    else:
                        rec = record(token, get_state_string(cur_state))
                        records_list.append(rec)
                        token = atom
                        col = get_column(atom)
                        cur_state = states[0][int(col)]
                    cur_state = 0
                    token = ''
                    continue
                #  Se o token acaba em um estado não final:
                if cur_state in non_final_states:
                    break
                continue
                #  Se o caracter não pertencer ao alfabeto:
            if not validation(atom):
                erro = 'é um caracter inválido.'
                cur_state = 0
                break
            col = get_column(atom)
            # Coloca em next_state o próximo estado do autômato
            next_state = states[int(cur_state)][int(col)]
            # Se a transição não for possível(token acabou):
            if next_state == -1:
                if cur_state == 16 and atom == '.':
                    rec = record(token[:-1], 'numero inteiro')
                    records_list.append(rec)
                    rec = record('..', 'simbolo especial composto')
                    records_list.append(rec)
                    cur_state = 0
                    token = ''
                    continue
                if cur_state == 2 and (atom in letters or atom in cap_letters):
                    erro = 'Identificador iniciado em numero. /'
                    break
                # Se o estado que trouxe ao fim do token não for final
                if cur_state in non_final_states:
                    erro = 'não é um token válido. /'
                    break
                # Se o estado que trouxe ao fim do token for final
                elif token.lower() in palavras_reservadas:
                    rec = record(token, 'palavra reservada')
                    records_list.append(rec)
                    token = atom
                    col = get_column(atom)
                    cur_state = states[0][int(col)]
                    continue
                else:
                    if cur_state == identif_state:
                        rec = record(token, get_state_string(cur_state))
                        records_list.append(rec)
                        if ht.hash_search(table, token) != -1:
                            token = atom
                            col = get_column(atom)
                            cur_state = states[0][int(col)]
                        else:
                            ident = identifier(token)
                            ht.hash_insert(table, ident)
                            token = atom
                            col = get_column(atom)
                            cur_state = states[0][int(col)]
                    else:
                        rec = record(token, get_state_string(cur_state))
                        records_list.append(rec)
                        token = atom
                        col = get_column(atom)
                        cur_state = states[0][int(col)]
            #  Se a transição for possível (token continua)
            else:
                token = token + atom
                cur_state = next_state
    #  Se o programa finalizar em um estado não final ou deu erro
    if cur_state in non_final_states or erro != '':
        # Acabou em estado não final
        if erro == '':
            print('ERRO! token', token, 'invalido. :', linha,
                  file=output)
            erro = 1
        # Deu algum erro durante o código
        else:
            print('ERRO EM', token+atom, erro, 'linha:', linha, file=output)
    #  Se programa finalizar em um estado final válido.
    if erro == '':
        col = get_column(atom)
        next_state = states[int(cur_state)][int(col)]
        # Se for palavra reservada
        if token.lower() in palavras_reservadas:
            rec = record(token, 'palavra reservada')
            records_list.append(rec)
        # Se não for palavra reservada
        elif atom != '\n' and atom != ' ':
            #  caso seja identificador
            if cur_state == identif_state:
                rec = record(token, get_state_string(cur_state))
                records_list.append(rec)
                if ht.hash_search(table, token) != -1:
                    token = atom
                    col = get_column(atom)
                    cur_state = states[0][int(col)]
                else:
                    ident = identifier(token)
                    ht.hash_insert(table, ident)
                    token = atom
                    col = get_column(atom)
                    cur_state = states[0][int(col)]
            else:
                rec = record(token, get_state_string(cur_state))
                records_list.append(rec)
                token = atom
                col = get_column(atom)
                cur_state = states[0][int(col)]
    #  printa os resultados
    print('Identificadores:\n', file=output)
    for list in table:
        for object in list:
            print(object.getName(), ht.hash(object.getName()), file=output)
    print('\nRecords:\n', file=output)
    for object in records_list:
        print(object.getToken(), 'da categoria', object.getCategory(),
              file=output)
    print('FIM')
    output.close()


main(sys.argv[1:])
