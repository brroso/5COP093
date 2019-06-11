import sys
import getopt
import hash_table as ht

keywords = [
            'AND', 'ARRAY', 'ASM', 'BEGIN', 'CASE', 'FLOAT',
            'CONST', 'CONSTRUCTOR', 'CONTINUE', 'DESTRUCTOR',
            'DIV', 'DO', 'DOWNTO', 'ELSE', 'END', 'FALSE', 'FILE',
            'FOR', 'FUNCTION', 'GOTO', 'IF', 'IMPLEMENTATION',
            'IN', 'INLINE', 'INTEGER', 'INTERFACE', 'LABEL', 'MOD', 'NIL',
            'NOT', 'OBJECT', 'OF', 'OR', 'INHERITED',
            'PACKED', 'PROCEDURE', 'PROGRAM', 'READ', 'RECORD',
            'REPEAT', 'SET', 'SHL', 'SHR', 'STRING', 'THEN', 'TO', 'TRUE',
            'TYPE', 'UNIT', 'UNTIL', 'USES', 'VAR', 'WHILE',
            'WITH', 'WRITE', 'XOR'
            ]

relacao_list = [    # RELACAO production (Kowaltowski pg73 - item 26)
    "=", "<>", "<", "<=", ">=", ">"
]

maismenos = [
    "+", "-"
]

maismenosor = [
    "+", "-", "OR"
]

divand = [
    "*", "div", "and"
]


def align(indice, ident, cat, nivel, tipo, desloc, passagem):
    return "{:7} | {:10} | {:15} | {:5} | {:10} | {:13} | {:10}".format(
                str(indice),
                str(ident), str(cat), str(nivel), str(tipo), str(desloc),
                str(passagem)
                )


class ParamTipo(object):

    def __init__(self, tipo, passagem):
        self.tipo = tipo
        self.passagem = passagem

    def getTipo(self):
        return self.tipo

    def getPassagem(self):
        return self.passagem

    def setTipo(self, tipo):
        self.tipo = tipo

    def setPassagem(self, passagem):
        self.passagem = passagem


class ForPar(object):

    def __init__(self, name, category):
        self.name = name
        self.category = "parâmetro formal"
        self.nivel = None
        self.tipo = None
        self.desloc = None
        self.passagem = None

    def getName(self):
        return self.name

    def getCat(self):
        return self.category

    def getNivel(self):
        return self.nivel

    def getTipo(self):
        return self.tipo

    def getDesloc(self):
        return self.desloc

    def getPassagem(self):
        return self.passagem

    def setNivel(self, nivel):
        self.nivel = nivel

    def setTipo(self, tipo):
        self.tipo = tipo

    def setDesloc(self, desloc):
        self.desloc = desloc

    def setPassagem(self, passagem):
        self.passagem = passagem


class SimVar(object):

    def __init__(self, name, category):
        self.name = name
        self.category = "variável simples"
        self.nivel = None
        self.tipo = None
        self.desloc = None

    def getName(self):
        return self.name

    def getCat(self):
        return self.category

    def getNivel(self):
        return self.nivel

    def getTipo(self):
        return self.tipo

    def getDesloc(self):
        return self.desloc

    def setNivel(self, nivel):
        self.nivel = nivel

    def setTipo(self, tipo):
        self.tipo = tipo

    def setDesloc(self, desloc):
        self.desloc = desloc


class ProcDef(object):

    def __init__(self, name, category, nparam):
        self.name = name
        self.category = "procedimento"
        self.nivel = None
        self.rotulo = None
        self.nparam = nparam
        self.param_list = [None] * nparam

    def setName(self, name):
        self.name = name

    def setCategory(self, category):
        self.category = category

    def setNivel(self, nivel):
        self.nivel = nivel

    def setRotulo(self, rotulo):
        self.rotulo = rotulo

    def addParam(self, tipo, passagem):
        ptipo = ParamTipo(tipo, passagem)
        for index, item in enumerate(self.param_list):
            if item is None:
                self.param_list[index] = ptipo
                break

    def getName(self):
        return self.name

    def getCategory(self):
        return self.category

    def getNivel(self):
        return self.nivel

    def getRotulo(self):
        return self.rotulo


class FuncDef(object):

    def __init__(self, name, category, nparam):
        self.name = name
        self.category = "função"
        self.nivel = None
        self.rotulo = None
        self.nparam = nparam
        self.param_list = [None] * nparam
        self.return_type = None

    def setName(self, name):
        self.name = name

    def setCategory(self, category):
        self.category = category

    def setNivel(self, nivel):
        self.nivel = nivel

    def setRotulo(self, rotulo):
        self.rotulo = rotulo

    def addParam(self, tipo, passagem):
        ptipo = ParamTipo(tipo, passagem)
        for index, item in enumerate(self.param_list):
            if item is None:
                self.param_list[index] = ptipo
                break

    def setReturnType(self, tipo):
        self.return_type = tipo

    def getName(self):
        return self.name

    def getCategory(self):
        return self.category

    def getNivel(self):
        return self.nivel

    def getRotulo(self):
        return self.rotulo

    def getReturnType(self):
        return self.return_type


class Token(object):    # The token class
    def __init__(self, name, category):
        self.name = name
        self.category = category

    def getName(self):
        return self.name

    def getCat(self):
        return self.category


class Parser:   # The parser class
    def __init__(self, token_list):
        self.token_list = token_list
        self.index = 0
        self.current = token_list[self.index]
        self.level = 0
        self.table = ht.new_table()

    def next_token(self):   # Puts the next token in current
        self.index += 1
        self.current = self.token_list[self.index]

    def start_parse(self):
        self.program()
        return 0

    def getIndex(self):
        return self.index

    # Checks if the passed token equals the current one
    def eat(self, token):
        print("ATUAL:", self.current.getName(), "DEVE SER:", token)
        if token == "." and len(self.token_list) - 1 == self.index:
            print("Fim da analise, nao houveram erros")
            quit()
        elif token == 'identificador':
            if self.current:
                if self.current.getCat() == 'identificador':
                    self.next_token()
                else:
                    print('Erro sintático em', self.current.getName())
                    quit()
        elif token == 'numero':
            if self.current:
                if 'numero' in self.current.getCat():
                    self.next_token()
                else:
                    print('Erro sintático em', self.current.getName())
                    quit()
        elif token == 'relacao':
            if self.current:
                if self.current.getName() in relacao_list:
                    self.next_token()
                else:
                    print('Erro sintático em', self.current.getName())
                    quit()
        else:
            if self.current:
                if self.current.getName().upper() == token.upper():
                    self.next_token()
                else:
                    print('Erro sintático em', self.current.getName())
                    quit()

    # PROGRAMAS E BLOCOS
    # PROGRAM production (Kowaltowksi pg. 72 - item 1)
    def program(self):
        if self.current.getName().upper() == 'PROGRAM':

            self.eat("PROGRAM")
            self.eat("identificador")
            self.eat("(")
            self.eat("identificador")
            self.bloco_id()
            self.eat(")")
            self.eat(";")
            self.bloco()
            while self.current.getName() != ".":
                self.bloco()
            self.eat(".")

    # BLOCO production (Kowaltowski pg. 72 - item 2)
    def bloco(self):

        if self.current.getName().upper() == "LABEL":
            self.label()
        if self.current.getName().upper() == "TYPE":
            self.type_keyword()
        if self.current.getName().upper() == "VAR":
            self.pt_dec_var()
        if self.current.getName().upper() == "PROCEDURE" \
                or self.current.getName().upper() == "FUNCTION":
            self.sub_routines()
        self.comando_composto()

    # DECLARAÇÕES
    # LABEL production (Kowaltowski pg. 72 - item 3)
    def label(self):

        if self.current.getName().upper() == 'LABEL':
            self.eat("LABEL")
            self.eat("number")
            while self.current.getName() == ",":
                self.eat(",")
                self.eat("number")
            self.eat(";")

    # TYPE production (Kowaltowski pg. 72 - item 4)
    def type_keyword(self):

        if self.current.getName().upper() == 'TYPE':
            self.eat("TYPE")
            self.typedef()
            self.eat(";")
            while self.current.getCat() == "identificador":
                self.typedef()
                self.eat(";")

    # DEFINIÇÃO DE TIPO production (Kowaltowski pg. 72 - item 5)
    def typedef(self):

        if self.current.getCat() == 'identificador':
            self.eat("identificador")
            self.eat("=")
            self.tipo()

    # TIPO production (Kowaltowski pg. 72 - item 6) TODO
    def tipo(self):

        if self.current.getCat() == 'identificador':
            token_name = self.current.getName()
            self.eat("identificador")
            return token_name.upper()
        elif self.current.getName().upper() == 'ARRAY':
            token_name = 'ARRAY OF '
            self.eat("ARRAY")
            self.eat("[")
            self.bloco_index()
            while self.current.getName() == ",":
                self.eat(",")
                self.bloco_index()
            self.eat("]")
            self.eat("OF")
            tipo_name = self.tipo().upper()
            token_name = token_name + tipo_name
            return token_name

    # INDICE production (Kowaltowski pg 72 - item 7)
    def bloco_index(self):

        if "numero" in self.current.getCat():
            self.eat("numero")
            self.eat("..")
            self.eat("numero")

    # PARTE DE DECLARAÇÕES DE VARIAVEIS production (Kowaltowski pg.72 - item 8)
    def pt_dec_var(self):

        if self.current.getName().upper() == 'VAR':
            self.eat("VAR")
            self.var_declaration()
            self.eat(";")
            while self.current.getCat() == 'identificador':
                self.var_declaration()
                self.eat(";")

    # DECLARAÇÂO DE VARIAVEIS production (Kowaltowksi pg.72 - item 9)
    def var_declaration(self):

        if self.current.getCat() == 'identificador':
            self.eat("identificador")
            while self.current.getName() == ",":
                self.eat(",")
                self.eat("identificador")
            self.eat(":")
            self.tipo()
            #colocar na hash

    # LISTA DE IDENTIFICADORES production (Kowaltowksi pg. 72 - item 10)
    def bloco_id(self):

        if self.current.getName() == ',':
            self.eat(",")
            self.eat("identificador")
            self.bloco_id()

    # PARTE DE DECLARAÇÃO DE SUB-ROTINAS production(Kowaltowski pg72 - item 11)
    def sub_routines(self):

        while self.current.getName().upper() == "PROCEDURE"  \
                or self.current.getName().upper() == "FUNCTION":
            if self.current.getName().upper() == "PROCEDURE":
                self.procedure()
                self.eat(";")
            elif self.current.getName().upper() == "FUNCTION":
                self.function()
                self.eat(";")

    # DECLARAÇÃO DE PROCEDIMENTO production(Kowaltoswki pg72 - item 12)
    def procedure(self):

        if self.current.getName().upper() == 'PROCEDURE':
            self.level += 1
            self.eat("PROCEDURE")
            self.eat("identificador")
            self.formal_parameters()
            self.eat(";")
            # colocar na hash
            self.bloco()
            self.level -= 1

    # DECLARAÇÃO DE FUNÇÃO production(Kowaltoswki pg72 - item 13)
    def function(self):

        if self.current.getName().upper() == 'FUNCTION':
            self.level += 1
            self.eat("FUNCTION")
            self.eat("identificador")
            self.formal_parameters()
            self.eat(":")
            self.eat("identificador")
            self.eat(";")
            # colocar na hash
            self.bloco()
            self.level -= 1

    # PARÂMETROS FORMAIS production (Kowaltowski pg72 - item 14)
    def formal_parameters(self):

        if self.current.getName() == '(':
            self.eat("(")
            self.formal_parameters_section()
            while self.current.getName() == ";":
                self.eat(";")
                self.formal_parameters_section()
            self.eat(")")

    # SEÇÃO DE PARÂMETROS FORMAIS production (Kowaltowski pg72 - item 15)
    def formal_parameters_section(self):

        if self.current.getName().upper() == 'VAR':
            self.eat("VAR")
            self.eat("identificador")
            while self.current.getName() == ",":
                self.eat(",")
                self.eat("identificador")
            self.eat(":")
            self.eat("identificador")
        elif self.current.getName().upper() == 'FUNCTION':
            self.eat("FUNCTION")
            self.eat("identificador")
            while self.current.getName() == ",":
                self.eat(",")
                self.eat("identificador")
            self.eat(":")
            self.eat("identificador")
        elif self.current.getName().upper() == 'PROCEDURE':
            self.eat("PROCEDURE")
            self.eat("identificador")
            while self.current.getName() == ",":
                self.eat(",")
                self.eat("identificador")
        elif self.current.getCat() == "identificador":
            self.eat("identificador")
            while self.current.getName() == ",":
                self.eat(",")
                self.eat("identificador")
            self.eat(":")
            self.eat("identificador")
        # colocar na hash

    # COMANDOS
    # COMANDO COMPOSTO production (Kowaltoski pg73 - item 16)
    def comando_composto(self):

        if self.current.getName().upper() == "BEGIN":
            self.eat("BEGIN")
            self.comando()
            while self.current.getName() == ";":
                self.eat(";")
                self.comando()
            self.eat("END")

    # COMANDO production (Kowaltowski pg73 - item 17)
    def comando(self):

        if "numero" in self.current.getCat():
            self.eat("numero")
            self.eat(":")
        self.comando_sem_rotulo()

    # COMANDO SEM RÓTULO production (Kowaltowski pg73 - item 18) TODO OR
    def comando_sem_rotulo(self):

        self.atribuicao()
        self.procedure_call()
        self.desvio()
        self.comando_composto()
        self.conditional_command()
        self.repetitive_command()
        self.read()
        self.write()

    # ATRIBUICAO production (Kowaltowski pg 73 - item 19)
    def atribuicao(self):

        if self.current.getCat() == "identificador" \
                and self.current.getName().upper() not in keywords:
            # and is a varsimples
            self.variavel()
            self.eat(":=")
            self.expression()

    # CHAMADA DE PROCEDIMENTO production (Kowaltoskwi pg73 - item 20)
    def procedure_call(self):

        if self.current.getCat() == "identificador":
            # and is a procedure
            self.eat("identificador")
            if self.current.getName() == "(":
                self.eat("(")
                self.expressions_list()
                self.eat(")")

    # DESVIO production (Kowaltowski pg73 - item 21)
    def desvio(self):

        if self.current.getName().upper() == "GOTO":
            self.eat("GOTO")
            self.eat("numero")

    # COMANDO CONDICIONAL production (Kowaltowski pg73 - item 22)
    def conditional_command(self):

        if self.current.getName().upper() == "IF":
            self.eat("IF")
            self.expression()
            self.eat("THEN")
            self.comando_sem_rotulo()
            if self.current.getName().upper() == "ELSE":
                self.eat("ELSE")
                self.comando_sem_rotulo()

    # COMANDO REPETITIVO production (Kowaltowksi pg 73 - item 23)
    def repetitive_command(self):

        if self.current.getName().upper() == "WHILE":
            self.eat("WHILE")
            self.expression()
            self.eat("DO")
            self.comando_sem_rotulo()

    # EXPRESSOES
    # LISTA DE EXPRESSÕES production (Kowaltowski pg 73 - item 24)
    def expressions_list(self):

        self.expression()
        while self.current.getName() == ",":
            self.eat(",")
            self.expression()

    # EXPRESSÂO production (Kowaltowski pg 73 - item 25)
    def expression(self):

        self.simple_expression()
        if self.current.getName() in relacao_list:
            self.eat("relacao")
            self.simple_expression()

    # EXPRESSÃO SIMPLES production (Kowaltowski pg 73 - item 27)
    def simple_expression(self):

        if "+" in self.current.getName() or "-" in self.current.getName():
            if "numero" in self.current.getCat():
                self.eat("numero")
            else:
                self.eat(self.current.getName())
                self.termo()
        else:
            self.termo()
        while "+" in self.current.getName() or "-" in self.current.getName():
            if "numero" in self.current.getCat():
                self.eat("numero")
            else:
                self.eat(self.current.getName())
                self.termo()
        while self.current.getName().upper() == "OR":
            self.eat("OR")
            self.termo()

    # TERMO production (Kowaltowski pg 74 - item 28)
    def termo(self):

        self.fator()
        while self.current.getName() in divand:
            self.eat(self.current.getName())
            self.fator()

    # FATOR production (Kowaltowski pg 74 - item 29) TODO diferenciar func e variavel
    def fator(self):

        if self.current.getCat() == "identificador":
            self.variavel()
        elif "numero" in self.current.getCat():
            self.eat("numero")
        elif self.current.getName() == "(":
            self.eat("(")
            self.expression()
            self.eat(")")
        elif self.current.getName().upper() == "NOT":
            self.eat("NOT")
            self.fator()
        elif self.current.getName().upper() == "TRUE":
            self.eat("TRUE")
        elif self.current.getName().upper() == "FALSE":
            self.eat("FALSE")
        else:
            self.function_call()

    # VARIAVEL production (Kowaltowski pg 74 - item 30)
    def variavel(self):

        if self.current.getCat() == "identificador":
            self.eat("identificador")
            if self.current.getName() == "[":
                self.eat("[")
                self.expressions_list()
                self.eat("]")

    # CHAMADA DE FUNÇÃO production (Kowaltowski pg 74 - item 31)
    def function_call(self):

        if self.current.getCat() == "identificador":
            self.eat("identificador")
            self.expressions_list()

    # READ E WRITE
    def read(self):

        if self.current.getName().upper() == "READ":
            self.eat("READ")
            self.eat("(")
            self.variavel()
            while self.current.getName() == ",":
                self.eat(",")
                self.variavel()
            self.eat(")")

    def write(self):

        if self.current.getName().upper() == "WRITE":
            self.eat("WRITE")
            self.eat("(")
            self.expression()
            while self.current.getName() == ",":
                self.eat(",")
                self.expression()
            self.eat(")")


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
    parser = parser.start_parse()


main(sys.argv[1:])
