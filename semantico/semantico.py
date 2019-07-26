import pickle
from modules import *

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

    var_list = []
    for no in node.children:
        if no.name == 'tabela de simbolos':
            symTab = no.ht
    main = routine(node.name, symTab)
    var_battery.append(var_list)
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

    var_list = []
    name = node.children[0].name  # o nome da rotina=sempre seu primeiro filho
    print('rotina', name)
    for filho in node.children:
        if filho.name == name:
            continue
        elif filho.name == 'bloco':
            break
        else:
            var = variavel(filho.name, filho.children[0].name, nivel)
            var_list.append(var)
    for no in node.children:  # procura a tabela de símbolos para salvar no nó
        if no.name == 'tabela de simbolos':
            symTab = no.ht
    rout = routine(name, symTab, current_routine)  # cria a rotina em si
    for rotina in routines_battery:
        if rotina.name == rout.name:  # checa se já tem uma rotina c esse nome
            print('erro semântico: já há um identificador visivel de nome',
                  rout.name)
            quit()
    else:  # checa se já tem uma variavel com esse nome no <= nivel
        for lista in var_battery:
            for identificador in lista:
                if identificador.name == rout.name:
                    print('erro semântico: já há um identificador visivel',
                          'de nome', rout.name)
                    quit()
    nivel += 1
    routines_battery.append(rout)
    current_routine = rout
    var_battery.append(var_list)


def var_dec(node):

    global current_routine
    global routines_battery
    global nivel
    global var_battery

    # Cria um obj variavel pra cada var declarada na rotina
    for no in node.children:
        var = variavel(no.name, no.children[0].name, nivel)
        # Ve todas as variaveis na pilha:
        for variable in var_battery[-1]:
            # Caso já tenha na lista atual uma variavel com esse nome:
            if variable.name == var.name:
                print('Já existe variável visível de nome', var.name)
                quit()
        # Ve todas as rotinas da pilha
        for rotina in routines_battery:
            # Caso já tenha na pilha atual uma rotina com esse nome:
            if rotina.name == var.name:
                print('erro semântico: já há uma rotina visivel',
                      'de nome', var.name)
                quit()
        var_battery[-1].append(var)


def main(argv):
    global current_routine
    global routines_battery
    global nivel
    global var_battery

    first = True
    for pre, fill, node in ast:
        if first:  # se for a primeira vez:
            first = semantigo(node, first)

        # caso encontre uma dec de variavel na arvre:
        if node.name == 'var declaration':
            var_dec(node)

        # elif node.name == 'atribuicao':
        #     for lista in var_battery:
        #         for variable in lista:
        #             rightmo = 
        #             if(variable.tipo != rightmo.tipo):
        #                 print("Tipos incompatíveis, {} é do tipo {} atribuição de tipo {}".format(variable.name, variable.tipo, rightmo.tipo))

        # caso encontre uma dec de proc na arvre:
        elif node.name == 'procedure dec':
            routine_dec(node)
            
        # elif 'Proc call' in node.name:
        #     # proccall

        # caso encontre uma dec de func na arvre:
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

        # o nó 'tabela de símbolos' siginficia dentro da arvre o fim de rotina
        if node.name == 'tabela de simbolos':
            var_battery.pop()  # da pop na pilha das variaveis
            routines_battery.pop()  # da pop na pilha das rotinas
            nivel -= 1
            if len(routines_battery) > 0:
                # coloca a rotina atual como a ultima
                current_routine = routines_battery[-1]
    print("Análise finalizada com sucesso.")


main('')
