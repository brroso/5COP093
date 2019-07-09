import sys
import getopt
import hash_table as ht
from anytree import Node, RenderTree

out_file = None

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


def flatlist(lista):
    return ''.join(flatten(lista))


def flatten(lista):
    return sum(([x] if not isinstance(x, list) else flatten(x)
                for x in lista), [])


def print_hash(hash_table):

    global out_file

    for index, lista in enumerate(hash_table):
        for item in lista:
            if isinstance(item, ForPar):
                print("{:7} | {:10} | {:15} | {:5} | {:13} | {:5} |\
                        {:10}".format(
                    str(index), str(item.getName()), str(item.getCategory()),
                    str(item.getNivel()), str(item.getTipo()),
                    str(item.getDesloc()), str(item.getPassagem()),
                ), file=out_file)
            elif isinstance(item, SimVar):
                print("{:7} | {:10} | {:15} | {:5} | {:13} | {:10}".format(
                    str(index), str(item.getName()), str(item.getCategory()),
                    str(item.getNivel()), str(item.getTipo()),
                    str(item.getDesloc())
                ), file=out_file)
            elif isinstance(item, FuncDef):
                print("{:7} | {:10} | {:15} | {:5} | {:10} | {:13} |\
                        {:13}".format(
                    str(index), str(item.getName()), str(item.getCategory()),
                    str(item.getNivel()),
                    str(item.getRotulo()), str(item.getNparam()),
                    str(item.getReturnType())), file=out_file)
                print('Parametros', file=out_file)
                if item.getParList():
                    for lista in item.getParList():
                        for par in lista:
                            print(par.getTipo(), par.getPassagem(), file=out_file)
            elif isinstance(item, ProcDef):
                print("{:7} | {:10} | {:15} | {:5} | {:13} | {:10}".format(
                    str(index), str(item.getName()), str(item.getCategory()),
                    str(item.getNivel()),
                    str(item.getRotulo()), str(item.getNparam())), file=out_file)
                print('Parametros', file=out_file)
                if item.getParList():
                    for lista in item.getParList():
                        for par in lista:
                            print(par.getTipo(), par.getPassagem(), file=out_file)
            elif isinstance(item, Token):
                print("{:7} | {:10} | {:15}".format(
                    str(index), str(item.getName()), str(item.getCategory())
                ), file=out_file)

    print('\n\n\n', file=out_file)


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

    def __init__(self, name, tipo, level, passagem):
        self.name = name
        self.category = "parametro formal"
        self.nivel = level
        self.tipo = tipo
        self.desloc = None
        self.passagem = passagem

    def getName(self):
        return self.name

    def getCategory(self):
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

    def __init__(self, name, tipo, nivel, desloc):
        self.name = name
        self.category = "variavel simples"
        self.nivel = nivel
        self.tipo = tipo
        self.desloc = desloc

    def getName(self):
        return self.name

    def getCategory(self):
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

    def __init__(self, name, nivel, nparam, param_list):
        self.name = name
        self.category = "procedure"
        self.nivel = nivel
        self.rotulo = None
        self.nparam = nparam
        self.param_list = param_list
        self.Symtab = []

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

    def getNparam(self):
        return self.nparam

    def getNivel(self):
        return self.nivel

    def getRotulo(self):
        return self.rotulo

    def getParList(self):
        return self.param_list

    def setSymtab(self, Symtab):
        self.Symtab = Symtab

    def getSymtab(self):
        return self.Symtab


class FuncDef(object):

    def __init__(self, name, tipo, nivel, nparam, param_list):
        self.name = name
        self.category = "function"
        self.nivel = nivel
        self.rotulo = None
        self.nparam = nparam
        self.param_list = param_list
        self.return_type = tipo
        self.Symtab = None

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

    def getNparam(self):
        return self.nparam

    def getRotulo(self):
        return self.rotulo

    def getReturnType(self):
        return self.return_type

    def getParList(self):
        return self.param_list

    def setSymtab(self, Symtab):
        self.Symtab = Symtab

    def getSymtab(self):
        return self.Symtab


class Token(object):    # The token class
    def __init__(self, name, category):
        self.name = name
        self.category = category

    def getName(self):
        return self.name

    def getCategory(self):
        return self.category


class Parser:   # The parser class
    def __init__(self, token_list):
        self.token_list = token_list
        self.index = 0
        self.current = token_list[self.index]
        self.level = 0
        self.table_pile = []
        self.root = None
        self.curr_root = None
        self.curr_desloc = -3
        self.curr_Symtab = None

    def next_token(self):   # Puts the next token in current
        self.index += 1
        self.current = self.token_list[self.index]

    def start_parse(self):
        self.program()
        return 0

    def getIndex(self):
        return self.index

    def setRoot(self, node):
        self.root = node

    def setCurrRoot(self, node):
        self.curr_root = node

    def getCurrRoot(self):
        return self.curr_root

    def getRoot(self):
        return self.root

    def getDesloc(self):
        return self.curr_desloc

    def setDesloc(self, value):
        self.curr_desloc = value

    def getSymtab(self):
        return self.curr_Symtab

    def newSymtab(self):
        table = ht.new_table()
        self.table_pile.append(table)
        self.curr_Symtab = self.table_pile[-1]

    def popSymtab(self, name):
        print('HASH DE', name, file=out_file)
        print_hash(self.table_pile.pop())
        if len(self.table_pile):
            self.curr_Symtab = self.table_pile[-1]
        else:
            self.curr_Symtab = None

    # Checks if the passed token equals the current one
    def eat(self, token):

        if token == "." and len(self.token_list) - 1 == self.index:
            print("Fim da analise, nao houveram erros")
            print("TREE\n\n", file=out_file)
            for pre, fill, node in RenderTree(self.getRoot()):
                print(pre, node.name, file=out_file)
                if node.name == 'tabela de simbolos':
                    for lista in node.ht:
                        for item in lista:
                            print(pre, item.getName(), file=out_file)
            quit()
        elif token == 'identificador':
            if self.current:
                if self.current.getCategory() == 'identificador':
                    self.next_token()
                else:
                    print('Erro sintático', self.current.getName())
                    quit()
        elif token == 'numero':
            if self.current:
                if 'numero' in self.current.getCategory():
                    self.next_token()
                else:
                    print('Erro sintático', self.current.getName())
                    quit()
        elif token == 'relacao':
            if self.current:
                if self.current.getName() in relacao_list:
                    self.next_token()
                else:
                    print('Erro sintático', self.current.getName())
                    quit()
        else:
            if self.current:
                if self.current.getName().upper() == token.upper():
                    self.next_token()
                else:
                    print('Erro sintático', self.current.getName())
                    quit()

    # PROGRAMAS E BLOCOS
    # PROGRAM production (Kowaltowksi pg. 72 - item 1)
    def program(self):
        if self.current.getName().upper() == 'PROGRAM':

            self.newSymtab()
            self.eat("PROGRAM")
            program = Token(self.current.getName(), 'program')
            progname = self.current.getName()
            ht.hash_insert(self.getSymtab(), program)
            node = Node(self.current.getName())
            self.setCurrRoot(node)
            self.setRoot(node)
            self.eat("identificador")
            self.eat("(")
            self.eat("identificador")
            self.bloco_id()
            self.eat(")")
            self.eat(";")
            self.bloco()
            while self.current.getName() != ".":
                self.bloco()
            no = Node(name='tabela de simbolos', parent=node, ht=self.table_pile[-1])
            self.popSymtab(progname)
            self.eat(".")

    # BLOCO production (Kowaltowski pg. 72 - item 2)
    def bloco(self):

        label = None
        bloco_node = Node("bloco", parent=self.getCurrRoot())
        prev_root = self.getCurrRoot()
        self.setCurrRoot(bloco_node)
        if self.current.getName().upper() == "LABEL":
            label = self.label()
        if self.current.getName().upper() == "TYPE":
            self.type_keyword()
        if self.current.getName().upper() == "VAR":
            self.pt_dec_var()
        if self.current.getName().upper() == "PROCEDURE" \
                or self.current.getName().upper() == "FUNCTION":
            self.sub_routines()
        self.comando_composto()
        self.setCurrRoot(prev_root)
        return label

    # DECLARAÇÕES
    # LABEL production (Kowaltowski pg. 72 - item 3)
    def label(self):

        label = []
        if self.current.getName().upper() == 'LABEL':

            label_node = Node("label", parent=self.getCurrRoot())
            prev_root = self.getCurrRoot()
            self.setCurrRoot(label_node)
            self.eat("LABEL")
            Node(self.current.getName(), parent=self.getCurrRoot())
            label.append(self.current.getName())
            self.eat("numero")
            while self.current.getName() == ",":
                self.eat(",")
                label.append(self.current.getName())
                Node(self.current.getName(), parent=self.getCurrRoot())
                self.eat("numero")
            self.eat(";")
            self.setCurrRoot(prev_root)

        return flatlist(label)

    # TYPE production (Kowaltowski pg. 72 - item 4)
    def type_keyword(self):

        if self.current.getName().upper() == 'TYPE':
            type_node = Node("type definition", parent=self.getCurrRoot())
            prev_root = self.getCurrRoot()
            self.setCurrRoot(type_node)
            self.eat("TYPE")
            self.typedef()
            self.eat(";")
            while self.current.getCategory() == "identificador":
                self.typedef()
                self.eat(";")
            self.setCurrRoot(prev_root)

    # DEFINIÇÃO DE TIPO production (Kowaltowski pg. 72 - item 5)
    def typedef(self):

        if self.current.getCategory() == 'identificador':
            ident = Node(self.current.getName(), self.getCurrRoot())
            self.eat("identificador")
            self.eat("=")
            Node(self.tipo(), ident)

    # TIPO production (Kowaltowski pg. 72 - item 6) TODO
    def tipo(self):

        if self.current.getCategory() == 'identificador':
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

        if "numero" in self.current.getCategory():
            self.eat("numero")
            self.eat("..")
            self.eat("numero")

    # PARTE DE DECLARAÇÕES DE VARIAVEIS production (Kowaltowski pg.72 - item 8)
    def pt_dec_var(self):

        if self.current.getName().upper() == 'VAR':
            desloc = 0
            var_node = Node("var declaration", parent=self.getCurrRoot())
            prev_root = self.getCurrRoot()
            self.setCurrRoot(var_node)
            self.eat("VAR")
            desloc += self.var_declaration(desloc)
            self.eat(";")
            while self.current.getCategory() == 'identificador':
                desloc += self.var_declaration(desloc)
                self.eat(";")
            self.setCurrRoot(prev_root)

    # DECLARAÇÂO DE VARIAVEIS production (Kowaltowksi pg.72 - item 9)
    def var_declaration(self, deslocamento):

        ids_list = []
        if self.current.getCategory() == 'identificador':
            ids_list.append(self.current.getName())
            self.eat("identificador")
            while self.current.getName() == ",":
                self.eat(",")
                ids_list.append(self.current.getName())
                self.eat("identificador")
            self.eat(":")
            vartipo = self.tipo()
            for desloc, item in enumerate(ids_list):
                ident = Node(item, self.getCurrRoot())
                Node(vartipo, ident)
                varobject = SimVar(item, vartipo, self.level, desloc +
                                   deslocamento)
                ht.hash_insert(self.getSymtab(), varobject)
            # self.appendSymtab(ids_list)
            return len(ids_list)

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
                proc_node = Node("procedure dec", parent=self.getCurrRoot())
                prev_root = self.getCurrRoot()
                self.setCurrRoot(proc_node)
                self.procedure()
                self.eat(";")
                self.setCurrRoot(prev_root)
            elif self.current.getName().upper() == "FUNCTION":
                label_node = Node("function dec", parent=self.getCurrRoot())
                prev_root = self.getCurrRoot()
                self.setCurrRoot(label_node)
                self.function()
                self.eat(";")
                self.setCurrRoot(prev_root)

    # DECLARAÇÃO DE PROCEDIMENTO production(Kowaltoswki pg72 - item 12)
    def procedure(self):

        if self.current.getName().upper() == 'PROCEDURE':


            oldtab = self.getSymtab()
            self.newSymtab()
            nparam = 0
            self.eat("PROCEDURE")
            proc_name = self.current.getName()
            Node(self.current.getName(), self.getCurrRoot())
            self.eat("identificador")
            parameters = self.formal_parameters()
            self.setDesloc(-3)
            if parameters:
                for lista in parameters:
                    for item in lista:
                        if isinstance(item, int):
                            nparam += item
                            lista.pop(item)
            self.eat(";")
            self.level += 1
            proc = ProcDef(proc_name, self.level, nparam, parameters)
            ht.hash_insert(oldtab, proc)
            label = self.bloco()
            for lista in self.table_pile[-1]:
                for item in lista:
                    if isinstance(item, ProcDef):
                        if item.getName() == proc_name and \
                                item.getNivel() == self.level:
                            item.setRotulo(label)
            no = Node(name='tabela de simbolos', ht=self.table_pile[-1], parent=self.getCurrRoot())
            self.popSymtab(proc_name)
            self.level -= 1

    # DECLARAÇÃO DE FUNÇÃO production(Kowaltoswki pg72 - item 13)
    def function(self):

        if self.current.getName().upper() == 'FUNCTION':
            oldtab = self.getSymtab()
            self.newSymtab()
            nparam = 0
            self.eat("FUNCTION")
            func_name = self.current.getName()
            Node(self.current.getName(), self.getCurrRoot())
            self.eat("identificador")
            parameters = self.formal_parameters()
            self.setDesloc(-3)
            if parameters:
                for lista in parameters:
                    for item in lista:
                        if isinstance(item, int):
                            nparam += item
                            lista.pop(item)
            self.eat(":")
            ret_type = self.current.getName()
            self.eat("identificador")
            self.eat(";")
            self.level += 1
            func = FuncDef(func_name, ret_type, self.level, nparam, parameters)
            ht.hash_insert(oldtab, func)
            label = self.bloco()
            for lista in self.table_pile[-1]:
                for item in lista:
                    if isinstance(item, FuncDef):
                        if item.getName() == func_name and \
                                item.getNivel() == self.level and \
                                item.getReturnType() == ret_type:
                            item.setRotulo(label)
            no = Node(name='tabela de simbolos', ht=self.table_pile[-1], parent=self.getCurrRoot())
            self.popSymtab(func_name)
            self.level -= 1

    # PARÂMETROS FORMAIS production (Kowaltowski pg72 - item 14)
    def formal_parameters(self):

        size = []
        objs_list = []
        if self.current.getName() == '(':
            self.eat("(")
            sizex, objs = self.formal_parameters_section()
            objs_list.append(objs)
            size.append(sizex)
            while self.current.getName() == ";":
                self.eat(";")
                sizex, objs = self.formal_parameters_section()
                objs_list.append(objs)
                size.append(sizex)
            self.eat(")")
            for lista in objs_list[::-1]:
                for forpar in lista:
                    forpar.setDesloc(self.getDesloc())
                    self.setDesloc(self.getDesloc() - 1)
            self.setDesloc(-3)
            return size

    # SEÇÃO DE PARÂMETROS FORMAIS production (Kowaltowski pg72 - item 15)
    def formal_parameters_section(self):

        ids = []
        forpars = []
        objs = []

        if self.current.getName().upper() == 'VAR':
            self.eat("VAR")
            ids.append(self.current.getName())
            self.eat("identificador")
            while self.current.getName() == ",":
                self.eat(",")
                ids.append(self.current.getName())
                self.eat("identificador")
            self.eat(":")
            tipo = self.current.getName()
            self.eat("identificador")
            for item in ids[::-1]:
                ident = Node(item, self.getCurrRoot())
                Node(tipo, ident)
                objpar = ForPar(item, tipo, self.level, 'Referencia')
                objs.append(objpar)
                newforpar = ParamTipo(tipo, 'Referencia')
                forpars.append(newforpar)
                ht.hash_insert(self.getSymtab(), objpar)

        elif self.current.getName().upper() == 'FUNCTION':
            self.eat("FUNCTION")
            ids.append(self.current.getName())
            self.eat("identificador")
            while self.current.getName() == ",":
                self.eat(",")
                ids.append(self.current.getName())
                self.eat("identificador")
            self.eat(":")
            tipo = self.current.getName()
            self.eat("identificador")
            for item in ids[::-1]:
                ident = Node(item, self.getCurrRoot())
                Node(tipo, ident)
                objpar = ForPar(item, tipo, self.level, 'Valor')
                objs.append(objpar)
                newforpar = ParamTipo(tipo, 'Valor')
                forpars.append(newforpar)
                ht.hash_insert(self.getSymtab(), objpar)

        elif self.current.getName().upper() == 'PROCEDURE':
            self.eat("PROCEDURE")
            ids.append(self.current.getName())
            self.eat("identificador")
            while self.current.getName() == ",":
                self.eat(",")
                ids.append(self.current.getName())
                self.eat("identificador")
            for item in ids[::-1]:
                ident = Node(item, self.getCurrRoot())
                objpar = ForPar(item, tipo, self.level, 'Valor')
                objs.append(objpar)
                newforpar = ParamTipo(tipo, 'Valor')
                forpars.append(newforpar)
                ht.hash_insert(self.getSymtab(), objpar)

        elif self.current.getCategory() == "identificador":
            ids.append(self.current.getName())
            self.eat("identificador")
            while self.current.getName() == ",":
                self.eat(",")
                ids.append(self.current.getName())
                self.eat("identificador")
            self.eat(":")
            tipo = self.current.getName()
            self.eat("identificador")
            for item in ids[::-1]:
                ident = Node(item, self.getCurrRoot())
                Node(tipo, ident)
                objpar = ForPar(item, tipo, self.level, 'Valor')
                objs.append(objpar)
                newforpar = ParamTipo(tipo, 'Valor')
                forpars.append(newforpar)
                ht.hash_insert(self.getSymtab(), objpar)

        forpars.append(len(ids))
        return forpars, objs

    # COMANDOS
    # COMANDO COMPOSTO production (Kowaltoski pg73 - item 16)
    def comando_composto(self):

        if self.current.getName().upper() == "BEGIN":
            comcomnode = Node("comando composto", parent=self.getCurrRoot())
            prev_root = self.getCurrRoot()
            self.setCurrRoot(comcomnode)
            self.eat("BEGIN")
            self.comando()
            while self.current.getName() == ";":
                self.eat(";")
                self.comando()
            self.eat("END")
            self.setCurrRoot(prev_root)

    # COMANDO production (Kowaltowski pg73 - item 17)
    def comando(self):

        if "numero" in self.current.getCategory():
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
        self.read()
        self.write()

    # ATRIBUICAO production (Kowaltowski pg 73 - item 19)
    def atribuicao(self):

        if self.current.getCategory() == "identificador" \
                and self.current.getName().upper() not in keywords:
            for table in self.table_pile:
                for lista in table:
                    for item in lista:
                        if self.current.getName() == item.getName():
                            if item.getCategory() == 'variavel simples' or \
                                    item.getCategory() == 'parametro formal' or \
                                    item.getCategory() == 'function':
                                atrib_node = Node(
                                    "atribuicao", parent=self.getCurrRoot())
                                prev_root = self.getCurrRoot()
                                self.setCurrRoot(atrib_node)
                                Node(flatlist(self.variavel()),
                                     parent=self.getCurrRoot())
                                self.eat(":=")
                                right_node = self.expression()
                                right_node.parent = self.getCurrRoot()
                                self.setCurrRoot(prev_root)

    # CHAMADA DE PROCEDIMENTO production (Kowaltoskwi pg73 - item 20)
    def procedure_call(self):

        if self.current.getCategory() == "identificador":
            for table in self.table_pile:
                for lista in table:
                    for item in lista:
                        if self.current.getName() == item.getName():
                            if item.getCategory() == 'procedure':
                                pname = self.current.getName()
                                self.eat("identificador")
                                proccall_bloco = Node(
                                    "Proc call \"" + pname + "\"",
                                    parent=self.getCurrRoot())
                                prev_root = self.getCurrRoot()
                                self.setCurrRoot(proccall_bloco)
                                if self.current.getName() == "(":
                                    self.eat("(")
                                    self.expressions_list()
                                    self.eat(")")
                                self.setCurrRoot(prev_root)

    # DESVIO production (Kowaltowski pg73 - item 21)
    def desvio(self):

        if self.current.getName().upper() == "GOTO":
            Node(self.current.getName(), parent=self.getCurrRoot())
            self.eat("GOTO")
            Node(self.current.getName(), parent=self.getCurrRoot())
            self.eat("numero")

    # COMANDO CONDICIONAL production (Kowaltowski pg73 - item 22)
    def conditional_command(self):

        if self.current.getName().upper() == "IF":
            ifnode = Node("If", parent=self.getCurrRoot())
            prev_root = self.getCurrRoot()
            self.setCurrRoot(ifnode)
            self.eat("IF")
            self.expression(),
            self.eat("THEN")
            self.comando_sem_rotulo()
            if self.current.getName().upper() == "ELSE":
                self.eat("ELSE")
                self.comando_sem_rotulo()
            self.setCurrRoot(prev_root)

    # COMANDO REPETITIVO production (Kowaltowksi pg 73 - item 23)
    def repetitive_command(self):

        if self.current.getName().upper() == "WHILE":
            whilenode = Node("While", parent=self.getCurrRoot())
            prev_root = self.getCurrRoot()

            self.setCurrRoot(whilenode)
            self.eat("WHILE")

            self.expression()

            self.eat("DO")
            self.comando_sem_rotulo()

            self.setCurrRoot(prev_root)

    # EXPRESSOES
    # LISTA DE EXPRESSÕES production (Kowaltowski pg 73 - item 24)
    def expressions_list(self):

        exp_list_node = self.expression()
        exp_list_node.parent = self.getCurrRoot()
        while self.current.getName() == ",":
            self.eat(",")
            node = self.expression()
            node.parent = self.getCurrRoot()
        return exp_list_node

    # EXPRESSÂO production (Kowaltowski pg 73 - item 25)
    def expression(self):

        expnode = self.simple_expression()
        if self.current.getName() in relacao_list:
            node = Node(self.current.getName(), self.getCurrRoot())
            prev_node = self.getCurrRoot()
            self.setCurrRoot(node)
            self.eat("relacao")
            exp_right_node = self.simple_expression()
            expnode.parent = node
            exp_right_node.parent = node
            self.setCurrRoot(prev_node)

        return expnode

    # EXPRESSÃO SIMPLES production (Kowaltowski pg 73 - item 27)
    def simple_expression(self):

        left_term_node = None
        right_term_node = None
        sign_node = None
        main_sign = None
        if "+" in self.current.getName() or "-" in self.current.getName():

            if "numero" in self.current.getCategory():
                left_term_node = self.termo()
            else:
                sign = self.current.getName()
                self.eat(self.current.getName())
                left_term_node = self.termo()
                left_term_node.name = flatten(sign) + \
                    flatten(left_term_node.name)

        else:

            left_term_node = self.termo()

        while "+" in self.current.getName() or "-" in self.current.getName() \
                or self.current.getName().upper() == "OR":

            if '+' in self.current.getName():
                if sign_node is None:
                    sign = '+'
                    sign_node = Node(sign)
                    left_term_node.parent = sign_node

                if "numero" in self.current.getCategory():
                    right_term_node = self.termo()
                    right_term_node.name = \
                        right_term_node.name.replace(sign, '')

                else:
                    self.eat(self.current.getName())
                    right_term_node = self.termo()

                right_term_node.parent = sign_node

            elif '-' in self.current.getName():
                if sign_node is None:
                    sign = '-'
                    sign_node = Node(sign)
                    left_term_node.parent = sign_node

                if "numero" in self.current.getCategory():
                    right_term_node = self.termo()
                    right_term_node.name = \
                        right_term_node.name.replace(sign, '')
                else:
                    self.eat(self.current.getName())
                    right_term_node = self.termo()

                right_term_node.parent = sign_node

            elif self.current.getName().upper() == "OR":
                if sign_node is None:
                    sign = 'OR'
                    sign_node = Node(sign)
                self.eat("OR")
                right_term_node = self.termo()
                right_term_node.parent = sign_node

            if "+" in self.current.getName() or "-" in self.current.getName() \
                    or self.current.getName().upper() == "OR":
                if "+" in self.current.getName():
                    sign = "+"
                if "-" in self.current.getName():
                    sign = "-"
                if "OR" in self.current.getName():
                    sign = "OR"

                main_sign = Node(sign)
                sign_node.parent = main_sign
                sign_node = main_sign
            else:
                main_sign = sign_node

        if main_sign is None:
            main_sign = left_term_node

        return main_sign

    # TERMO production (Kowaltowski pg 74 - item 28)
    def termo(self):

        left_term_node = self.fator()
        right_term_node = None
        term_node = None
        main_node = None
        while self.current.getName() in divand:

            if term_node is None:
                term_node = Node(self.current.getName())
                left_term_node.parent = term_node
            self.eat(self.current.getName())

            right_term_node = self.fator()

            if '+' in left_term_node.name:
                left_term_node.name = left_term_node.name.replace('+', '')

            if '-' in left_term_node.name:
                left_term_node.name = left_term_node.name.replace('-', '')

            if '+' in right_term_node.name:
                right_term_node.name = right_term_node.name.replace('+', '')

            if '-' in right_term_node.name:
                right_term_node.name = right_term_node.name.replace('-', '')

            right_term_node.parent = term_node

            if self.current.getName() in divand:
                main_node = Node(self.current.getName())
                term_node.parent = main_node
                term_node = main_node
            else:
                main_node = term_node

        if main_node is None:
            main_node = left_term_node
        return main_node

    # FATOR production (Kowaltowski pg 74 - item 29)
    def fator(self):

        fator = None
        if self.current.getCategory() == "identificador":
                for table in self.table_pile:
                    for lista in table:
                        for item in lista:
                            if self.current.getName() == item.getName():
                                if item.getCategory() == 'variavel simples' or \
                                        item.getCategory() == 'parametro formal':
                                    fator = Node(self.variavel())
                                elif item.getCategory() == 'function':
                                    fator = self.function_call()
        elif "numero" in self.current.getCategory():
            fator = Node(self.current.getName())
            self.eat("numero")
        elif self.current.getName() == "(":
            self.eat("(")
            fator = self.expression()
            self.eat(")")
        elif self.current.getName().upper() == "NOT":
            fator = Node(self.current.getName())
            self.eat("NOT")
            fator = Node(self.fator())
        elif self.current.getName().upper() == "TRUE":
            fator = Node(self.current.getName())
            self.eat("TRUE")
        elif self.current.getName().upper() == "FALSE":
            fator = Node(self.current.getName())
            self.eat("FALSE")
        return fator

    # VARIAVEL production (Kowaltowski pg 74 - item 30)
    def variavel(self):

        if self.current.getCategory() == "identificador":
            var = self.current.getName()
            self.eat("identificador")
            if self.current.getName() == "[":
                self.eat("[")
                self.expressions_list()
                self.eat("]")
        return var

    # CHAMADA DE FUNÇÃO production (Kowaltowski pg 74 - item 31) TODO
    def function_call(self):

        if self.current.getCategory() == "identificador":
            for table in self.table_pile:
                for lista in table:
                    for item in lista:
                        if self.current.getName() == item.getName():
                            if item.getCategory() == 'function':
                                f = self.current.getName()
                                node = Node("Function call \"" + f + "\"")
                                prev_root = self.getCurrRoot()
                                self.setCurrRoot(node)
                                self.eat("identificador")
                                if self.current.getName() == "(":
                                    self.eat("(")
                                    explist = self.expressions_list()
                                    self.eat(")")
                                self.setCurrRoot(prev_root)
        explist.parent = node
        return node
    # READ E WRITE
    def read(self):

        if self.current.getName().upper() == "READ":
            readnode = Node(
                "Read", parent=self.getCurrRoot())
            prev_root = self.getCurrRoot()
            self.setCurrRoot(readnode)
            self.eat("READ")
            self.eat("(")
            Node(flatlist(self.variavel()),
                 parent=self.getCurrRoot())
            while self.current.getName() == ",":
                self.eat(",")
                Node(flatlist(self.variavel()),
                     parent=self.getCurrRoot())
            self.eat(")")
            self.setCurrRoot(prev_root)

    def write(self):

        if self.current.getName().upper() == "WRITE":
            writenode = Node(
                "Write", parent=self.getCurrRoot())
            prev_root = self.getCurrRoot()
            self.setCurrRoot(writenode)
            self.eat("WRITE")
            self.eat("(")
            self.expression().parent = self.getCurrRoot()
            while self.current.getName() == ",":
                self.eat(",")
                self.expression().parent = self.getCurrRoot()
            self.eat(")")
            self.setCurrRoot(prev_root)


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
    global out_file
    out_file = open(output_file, 'w+')
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
