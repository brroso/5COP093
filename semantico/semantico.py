import pickle
from modules import *
import re

ast = open('../ast', 'rb')
ast = pickle.load(ast)

operations = ['+', '-', '*', '/', '>', '<', '>=', '<=', '<>', '=']
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
    def __init__(self, name, tipo, nivel, passagem=None, desloc=None):
        self.name = name
        self.tipo = tipo
        self.nivel = nivel
        self.passagem = passagem
        self.desloc = desloc


class routine(object):
    def __init__(self, name, symTab, parent=None, retType=None, parlist=None, nparam=None):
        self.name = name
        self.symTab = symTab
        self.parent = parent
        self.retType = retType
        self.parlist = parlist
        self.nparam = nparam


def routine_dec(node):  # lida com declarações de rotinas

    global current_routine
    global routines_battery
    global nivel

    var_list = []
    name = node.children[0].name  # o nome da rotina=sempre seu primeiro filho
    retType = None
    parlist = None
    nparam = None
    symTab = None
    for no in node.children:  # procura a tabela de símbolos para salvar no nó
        if no.name == 'tabela de simbolos':
            symTab = no.ht
    for lista in current_routine.symTab:
        for item in lista:
            if item.getName() == name:
                if item.getCategory() == 'function':
                    retType = item.getReturnType()
                    parlist = item.getParList()
                    nparam = item.getNparam()
                if item.getCategory == 'procedure':
                    parlist = item.getParList()
                    nparam = item.getNparam()

    for filho in node.children:  # coloca os parametros formais como variáveis
        if filho.name == name:
            continue
        elif filho.name == 'bloco':
            break
        else:
            for lista in symTab:
                for item in lista:
                    # Checa se existe rotina com o nome do forpar
                    for rotina in routines_battery:
                        if rotina.name == filho.name:
                            print("erro: Parâmetro formal", filho.name,
                                  "da rotina", name,
                                  "não pode ser declarado pois existe" +
                                  " rotina com esse nome.")
                            quit()
                    # Pega o deslocamento e tipo de passagem do forpar
                    if item.getCategory() == 'parametro formal' and \
                            item.getName() == filho.name:
                        var = variavel(filho.name, filho.children[0].name,
                                       nivel, item.getPassagem(),
                                       item.getDesloc())
                        var_list.append(var)
    rout = routine(name, symTab, current_routine, retType,
                   parlist, nparam)  # cria a rotina
    for rotina in routines_battery:
        if rotina.name == rout.name:  # checa se já tem uma rotina c esse nome
            print('erro: já há um identificador visivel de nome',
                  rout.name)
            quit()
    else:  # checa se já tem uma variavel com esse nome no <= nivel
        for lista in var_battery:
            for identificador in lista:
                if identificador.name == rout.name:
                    print('erro: já há um identificador visivel',
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
                print('erro: Já existe variável visível de nome', var.name)
                quit()
        # Ve todas as rotinas da pilha
        for rotina in routines_battery:
            # Caso já tenha na pilha atual uma rotina com esse nome:
            if rotina.name == var.name:
                print('erro: já há uma rotina visivel',
                      'de nome', var.name)
                quit()
        var_battery[-1].append(var)


def routine_call(node):

    global routines_battery
    global var_battery

    rout_name = re.findall(r'"(.*?)"', node.name)
    rout_name = str(rout_name[0])

    for rotina in routines_battery:
        if rout_name == rotina.name:
            print("CHAMADA DA ROTINA:", rotina.name, rotina.retType,
                  rotina.nparam, rotina.parlist)


def operation_routine(node):

    global routines_battery
    global var_battery

    leftmo = node.children[0]
    rightmo = node.children[1]
    leftmo_tipo = None
    rightmo_tipo = None

    if leftmo.name.isdigit():
        leftmo_tipo = 'numero'

    if rightmo.name.isdigit():
        rightmo_tipo = 'numero'

    if leftmo.name in operations:
        leftmo_tipo = operation_routine(leftmo)

    if rightmo.name in operations:
        rightmo_tipo = operation_routine(rightmo)

    for variable in var_battery[-1]:
        if variable.name == leftmo.name:
            leftmo_tipo = variable.tipo
        if variable.name == rightmo.name:
            rightmo_tipo = variable.tipo

    if leftmo_tipo is None:
        if 'Function call' not in leftmo.name:
            print('Não existe essa variavel', leftmo.name)
            quit()
    if rightmo_tipo is None:
        if 'Function call' not in rightmo.name:
            print('Não existe essa variavel', rightmo.name)
            quit()

    if leftmo_tipo.upper() == 'FLOAT' or leftmo_tipo.upper() == 'INTEGER':
        leftmo_tipo = 'numero'

    if rightmo_tipo.upper() == 'FLOAT' or rightmo_tipo.upper() == 'INTEGER':
        rightmo_tipo = 'numero'

    for routine in routines_battery:
        if leftmo_tipo is None:
            if routine.name == str(re.findall(r'"(.*?)"', leftmo.name)[0]):
                leftmo_tipo = routine.retType
        if rightmo_tipo is None:
            if routine.name == str(re.findall(r'"(.*?)"', rightmo.name)[0]):
                rightmo_tipo = routine.retType

    if leftmo_tipo is None or rightmo_tipo is None:
        print("Operação inválida!")
        quit()
    else:
        if rightmo_tipo == leftmo_tipo:
            return rightmo_tipo
        else:
            print(leftmo_tipo, rightmo_tipo)
            print("DOIS TIOS DIFERENTES")
            quit()


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
        elif 'Proc call' in node.name:
            routine_call(node)
        # caso encontre uma dec de func na arvre:
        elif node.name == 'function dec':
            routine_dec(node)

        elif 'Function call' in node.name:
            routine_call(node)

        # elif node.name == 'Write':
        #     # write

        # elif node.name == 'Read':
        #     # read

        elif node.name in operations:
            operation_routine(node)

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
