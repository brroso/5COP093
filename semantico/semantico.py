import pickle
from modules import *

# Checar funcionamento de parâmetros formais

ast = open('../ast', 'rb')
ast = pickle.load(ast)

operations = ['+', '-', '*', '/', '>', '<', '>=', '<=', '<>']
routines_battery = []
current_routine = None
nivel = 0
var_battery = []


def semantigo(node, first):  # Inicia a análise
    global current_routine
    global routines_battery

    for no in node.children:
        if no.name == 'tabela de simbolos':
            symTab = no.ht
    main = routine(node.name, symTab)
    routines_battery.append(main)
    current_routine = main
    first = False
    return first


class variavel(object):
    def __init__(self, name, tipo, nivel):
        self.name = name
        self.tipo = tipo
        self.nivel = nivel


class routine(object):
    def __init__(self, name, symTab, parent=None):
        self.name = name
        self.symTab = symTab
        self.parent = parent


def routine_dec(node):  # lida com declarações de rotinas

    global current_routine
    global routines_battery
    global nivel

    name = node.children[0].name  # o nome da rotina=sempre seu primeiro filho
    print('rotina', name)
    for no in node.children:  # procura a tabela de símbolos para salvar no nó
        if no.name == 'tabela de simbolos':
            symTab = no.ht
    rout = routine(name, symTab, current_routine)  # cria a rotina em si
    for rotina in routines_battery:
        if rotina.name == rout.name:  # checa se já tem uma rotina c esse nome
            print('erro semântico: já há um identificador visivel de nome',
                  rout.name)
            quit()
        else:  # checa se já tem uma variavel com esse nome
            for lista in rotina.symTab:
                for identificador in lista:
                    if identificador.getName() == rout.name and \
                            identificador.getNivel() <= nivel:
                        print('erro semântico: já há um identificador visivel',
                              'de nome', rout.name)
                        quit()
    nivel += 1
    routines_battery.append(rout)
    current_routine = rout


def var_dec(node):

    global current_routine
    global routines_battery
    global nivel
    global var_battery

    var_list = []

    for no in node.children:
        var = variavel(no.name, no.children[0].name, nivel)
        print(no.name)
        for lista in var_battery:
            for variable in lista:
                if variable.name == var.name and \
                        variable.nivel == var.nivel:
                    print('Já existe variável visível de nome', var.name)
                    quit()
        for rotina in routines_battery:
            if rotina.name == var.name:
                print('erro semântico: já há uma rotina visivel',
                      'de nome', var.name)
                quit()
        var_list.append(var)
        var_battery.append(var_list)


def main(argv):
    global current_routine
    global routines_battery
    global nivel
    global var_battery

    first = True
    for pre, fill, node in ast:
        if first:
            first = semantigo(node, first)
        if node.name == 'var declaration':
            var_dec(node)
        # elif node.name == 'atribuicao':
        #     # atrib
        elif node.name == 'procedure dec':
            routine_dec(node)
        # elif 'Proc call' in node.name:
        #     # proccall
        elif node.name == 'function dec':
            routine_dec(node)
        # elif 'Function call' in node.name:
        #     # funccall
        # elif node.name == 'Write':
        #     # write
        # elif node.name == 'Read':
        #     # read
        # elif node.name in operations:
        #     # comparacao
        if node.name == 'tabela de simbolos':
            var_battery.pop()
            routines_battery.pop()
            nivel -= 1
            if len(routines_battery) > 0:
                current_routine = routines_battery[-1]


main('')
