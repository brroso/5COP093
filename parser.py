import sys
import getopt

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

    def next_token(self):   # Puts the next token in current
        self.index += 1
        self.current = self.token_list[self.index]

    def start_parse(self):
        self.program()
        return 0

    # Checks if the passed token equals the current one
    def eat(self, token):
        print("ATUAL E TOKEN", self.current.getName(), token)
        if token == 'identificador':
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
            self.eat(".")

    # BLOCO production (Kowaltowski pg. 72 - item 2)
    def bloco(self):
        if self.current.getName().upper() == "LABEL":
            self.label()
        elif self.current.getName().upper() == "TYPE":
            self.type_keyword()
        elif self.current.getName().upper() == "VAR":
            self.pt_dec_var()
        self.sub_routines()
        self.comando_composto()

    # DECLARAÇÕES
    # LABEL production (Kowaltowski pg. 72 - item 3)
    def label(self):
        if self.current.getName().upper() == 'LABEL':

            self.eat("LABEL")
            self.eat("number")
            self.bloco_label()
            self.eat(";")
            # FINISHED

    def bloco_label(self):
        if self.current == ",":
            self.eat(",")
            self.eat("number")
            self.bloco_label()
        else:
            pass

    # TYPE production (Kowaltowski pg. 72 - item 4)
    def type_keyword(self):
        if self.current.getName().upper() == 'type':

            self.eat("TYPE")
            self.typedef()

    # DEFINIÇÃO DE TIPO production (Kowaltowski pg. 72 - item 5)
    def typedef(self):
        if self.current.getCat() == 'identificador':

            self.eat("identificador")
            self.eat("=")
            self.tipo()
            self.eat(";")
            self.typedef()

        else:
            pass

    # TIPO production (Kowaltowski pg. 72 - item 6)
    def tipo(self):
        if self.current.getCat() == 'identificador':

            self.eat("identificador")

        elif self.current.getName().upper == 'ARRAY':

            self.eat("ARRAY")
            self.eat("[")
            self.eat("number")
            self.eat("..")
            self.eat("number")
            self.bloco_index()
            self.eat("]")
            self.eat("OF")
            self.tipo()

    # INDICE production (Kowaltowski pg 72 - item 7)
    def bloco_index(self):

        if self.current.getName() == ',':
            self.eat(",")
            self.eat("number")
            self.eat("..")
            self.eat("number")
            self.bloco_index()
        else:
            pass

    # PARTE DE DECLARAÇÕES DE VARIAVEIS production (Kowaltowski pg.72 - item 8)
    def pt_dec_var(self):

        if self.current.getName().upper() == 'VAR':
            self.eat("VAR")
            self.var_declaration()

    # DECLARAÇÂO DE VARIAVEIS production (Kowaltowksi pg.72 - item 9)
    def var_declaration(self):

        if self.current.getCat() == 'identificador':
            self.eat("identificador")
            self.bloco_id()
            self.eat(":")
            self.tipo()
            self.eat(";")
            self.var_declaration()

    # LISTA DE IDENTIFICADORES production (Kowaltowksi pg. 72 - item 10)
    def bloco_id(self):
        if self.current.getName() == ',':
            self.eat(",")
            self.eat("identificador")
            self.bloco_id()
        else:
            pass
        # FINISHED

    # PARTE DE DECLARAÇÃO DE SUB-ROTINAS production(Kowaltowski pg72 - item 11)
    def sub_routines(self):
        if self.current.getName() == '{':
            self.eat("{")
            self.procedure()
            self.function()
            self.eat("}")

    # DECLARAÇÃO DE PROCEDIMENTO production(Kowaltoswki pg72 - item 12)
    def procedure(self):

        if self.current.getName().upper() == 'PROCEDURE':
            self.eat("PROCEDURE")
            self.eat("identificador")
            self.formal_parameters()
            self.eat(";")
            self.bloco()

    # DECLARAÇÃO DE FUNÇÃO production(Kowaltoswki pg72 - item 13)
    def function(self):

        if self.current.getName().upper() == 'FUNCTION':
            self.eat("FUNCTION")
            self.eat("identificador")
            self.formal_parameters()
            self.eat(";")
            self.bloco()

    # PARÂMETROS FORMAIS production (Kowaltowski pg72 - item 14)
    def formal_parameters(self):
        if self.current.getName() == '(':
            self.eat("(")
            self.formal_parameters_section()
            while self.current.getName() == ";":
                self.formal_parameters_section()
            self.eat(")")

    # SEÇÃO DE PARÂMETROS FORMAIS production (Kowaltowski pg72 - item 15)
    def formal_parameters_section(self):
        if self.current.getName().upper() == 'VAR':
            self.eat("VAR")
            self.eat("identificador")
            self.bloco_id()
            self.eat(":")
            self.eat("identificador")
        elif self.current.getName().upper() == 'FUNCTION':
            self.eat("FUNCTION")
            self.eat("identificador")
            self.bloco_id()
            self.eat(":")
            self.eat("identificador")
        elif self.current.getName().upper() == 'PROCEDURE':
            self.eat("PROCEDURE")
            self.eat("identificador")
            self.bloco_id()

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

    # COMANDO SEM RÓTULO production (Kowaltowski pg73 - item 18)
    def comando_sem_rotulo(self):
        self.atribuicao()
        self.procedure_call()
        self.desvio()
        self.comando_composto()
        self.conditional_command()
        self.repetitive_command()

    # ATRIBUICAO production (Kowaltowski pg 73 - item 19)
    def atribuicao(self):
        if self.current.getCat() == "identificador":
            self.variavel()
            self.eat(":=")
            self.expression()

    # CHAMADA DE PROCEDIMENTO production (Kowaltoskwi pg73 - item 20)
    def procedure_call(self):
        if self.current.getCat() == "identificador":
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
        if self.current.getCat() in maismenos:
            self.eat(self.current.getName())
        self.termo()
        if self.current.getName() in maismenosor:
            self.eat(self.current.getName())
            self.termo()

    # TERMO production (Kowaltowski pg 74 - item 28)
    def termo(self):

        self.fator()
        if self.current.getName() in divand:
            self.eat(self.current.getName())
            self.fator()

    # FATOR production (Kowaltowski pg 74 - item 29)
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
        self.eat("identificador")
        self.expressions_list()


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
