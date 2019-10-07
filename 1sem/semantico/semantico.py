import pickle
from modules import *
import re

ast = open('../ast', 'rb')
ast = pickle.load(ast)

operations = ['+', '-', '*', '/', '>', '<', '>=', '<=', '<>', '=', 'div']
current_routine = None
nivel = 0
var_battery = []
output = []


def reemovNestings(l):

    for i in l:
        if type(i) == list:
            reemovNestings(i)
        else:
            output.append(i)

    return output


def semantigo(node, first):  # Inicia a análise
    global current_routine

    var_list = []
    for no in node.children:
        if no.name == 'tabela de simbolos':
            symTab = no.ht
    main = routine(node.name, symTab)
    var_battery.append(var_list)
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
        self.children = []


def get_rotinas_acessaveis(rotina):

    rotinas_acessaveis = []

    while 1:
        if rotina.parent is None:
            for filho in rotina.children:
                rotinas_acessaveis.append(filho)
            return rotinas_acessaveis
        else:
            rotinas_acessaveis.append(rotina.parent)
            rotina = rotina.parent
            for filho in rotina.children:
                rotinas_acessaveis.append(filho)


def routine_dec(node):  # lida com declarações de rotinas

    global current_routine
    global nivel
    global output

    rotinas_acessaveis = get_rotinas_acessaveis(current_routine)

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
                    output = []
                    if item.getParList() is not None:
                        parlist = reemovNestings(item.getParList())
                    nparam = item.getNparam()
                if item.getCategory() == 'procedure':
                    output = []
                    if item.getParList() is not None:
                        parlist = reemovNestings(item.getParList())
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
                    for rotina in rotinas_acessaveis:
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
    if parlist is not None:
        for index, item in enumerate(parlist):
            if item.tipo.upper() == 'INTEGER' or \
                    item.tipo.upper() == 'FLOAT':
                parlist[index].tipo = 'numero'
    rout = routine(name, symTab, current_routine, retType,
                   parlist, nparam)  # cria a rotina
    for rotina in rotinas_acessaveis:
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
    current_routine.children.append(rout)
    current_routine = rout
    var_battery.append(var_list)


def var_dec(node):

    global current_routine
    global nivel
    global var_battery

    rotinas_acessaveis = get_rotinas_acessaveis(current_routine)

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
        for rotina in rotinas_acessaveis:
            # Caso já tenha na pilha atual uma rotina com esse nome:
            if rotina.name == var.name:
                print('erro: já há uma rotina visivel',
                      'de nome', var.name)
                quit()
        var_battery[-1].append(var)


def routine_call(node):

    global var_battery

    rotinas_acessaveis = get_rotinas_acessaveis(current_routine)

    params_passados = 0
    params_list = []

    rout_name = re.findall(r'"(.*?)"', node.name)
    rout_name = str(rout_name[0])

    for filho in node.children:
        params_passados += 1
        if filho.name in operations:
            params_list.append(operation_routine(filho))
        elif filho.name.isdigit():
            params_list.append('numero')
        else:
            for variable in var_battery[-1]:
                if variable.name == filho.name:
                    params_list.append(variable)
            for routine in rotinas_acessaveis:
                if filho.name == routine.name:
                    if routine.retType is None:
                        print("Rotina", routine.name, "não pode ser",
                              "utilizada como parâmetro.")
                        quit()
                    else:
                        params_list.append(routine)

    for rotina in rotinas_acessaveis:
        if rout_name == rotina.name:
            if params_passados > rotina.nparam or \
                    params_passados < rotina.nparam:
                print("erro: a rotina", rout_name, "exige", rotina.nparam,
                      "parâmetros. foram passados", params_passados)
                quit()
            else:
                for index, item in enumerate(params_list):
                    if isinstance(item, variavel):
                        if item.tipo.upper() == 'FLOAT' or item.tipo.upper() == 'INTEGER':
                            item.tipo = 'numero'
                        if item.tipo.upper() != rotina.parlist[index].tipo.upper():
                            print('parametro', item.name, 'incorreto')
                            quit()
                    if item == 'numero':
                        if rotina.parlist[index].passagem == 'Referencia':
                            print('O parametro precisa ser por referencia')
                            quit()
                        else:
                            if rotina.parlist[index].tipo.upper == 'BOOLEAN':
                                print('Parametro numerico passado para',
                                      'booleano')
                                quit()
                    if isinstance(item, type(rotina)):
                        if item.retType is None:
                            print('Passada rotina sem retorno')
                            quit()
                        else:
                            if rotina.parlist[index].passagem == 'Referencia':
                                print('O parametro precisa ser por referencia')
                                quit()
                            if item.retType.upper() == 'BOOLEAN':
                                if rotina.parlist[index].tipo.upper != 'BOOLEAN':
                                    print('booleano passado para numerico')
                                    quit()
                            if item.retType.upper() == 'FLOAT' or item.retType.upper() == 'INTEGER':
                                if rotina.parlist[index].tipo.upper != 'NUMERO':
                                    print('passada rotina com retorno errado.')
                                    quit()
                            


def operation_routine(node):

    global var_battery

    rotinas_acessaveis = get_rotinas_acessaveis(current_routine)

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

    for routine in rotinas_acessaveis:
        if 'Function call' in leftmo.name:
            if routine.name == str(re.findall(r'"(.*?)"', leftmo.name)[0]):
                leftmo_tipo = routine.retType
        if 'Function call' in rightmo.name:
            if routine.name == str(re.findall(r'"(.*?)"', rightmo.name)[0]):
                rightmo_tipo = routine.retType

    if leftmo_tipo is None or rightmo_tipo is None:
        print("Operação inválida!", leftmo.name, "com", rightmo.name)
        quit()

    else:
        if leftmo_tipo.upper() == 'FLOAT' or leftmo_tipo.upper() == 'INTEGER':
            leftmo_tipo = 'numero'

        if rightmo_tipo.upper() == 'FLOAT' or rightmo_tipo.upper() == 'INTEGER':
            rightmo_tipo = 'numero'

        if rightmo_tipo == leftmo_tipo:
            return rightmo_tipo
        else:
            print(leftmo_tipo, leftmo.name, rightmo_tipo, rightmo.name)
            print("DOIS TIPOS DIFERENTES")
            quit()


def atrib(node):

    global var_battery

    rotinas_acessaveis = get_rotinas_acessaveis(current_routine)

    leftmo = node.children[0]
    rightmo = node.children[1]
    leftmo_tipo = None
    rightmo_tipo = None

    if leftmo.name.isdigit():
        print("Atribuição inválida. (numero recebe valor)")
        quit()

    if rightmo.name.isdigit():
        rightmo_tipo = 'numero'

    if leftmo.name in operations:
        print("Atribuição inválida. (exp recebe valor)")

    if rightmo.name in operations:
        rightmo_tipo = operation_routine(rightmo)

    for variable in var_battery[-1]:
        if variable.name == leftmo.name:
            leftmo_tipo = variable.tipo
        if variable.name == rightmo.name:
            rightmo_tipo = variable.tipo

    for routine in rotinas_acessaveis:
        if leftmo.name == routine.name:
            leftmo_tipo = routine.retType

    for routine in rotinas_acessaveis:
        if 'Function call' in rightmo.name:
            if routine.name == str(re.findall(r'"(.*?)"', rightmo.name)[0]):
                rightmo_tipo = routine.retType

    if leftmo_tipo is None or rightmo_tipo is None:
        print("erro: Variável inválida em operação.")
        quit()

    else:
        if leftmo_tipo.upper() == 'FLOAT' or leftmo_tipo.upper() == 'INTEGER':
            leftmo_tipo = 'numero'

        if rightmo_tipo.upper() == 'FLOAT' or rightmo_tipo.upper() == 'INTEGER':
            rightmo_tipo = 'numero'

        if rightmo_tipo == leftmo_tipo:
            return rightmo_tipo
        else:
            print("DOIS TIPOS DIFERENTES")
            quit()


def write(node):

    left_write = None
    right_write = None

    rotinas_acessaveis = get_rotinas_acessaveis(current_routine)

    if len(node.children) != 2:
        print(node.name, end=" ")
        for filho in node.children:
            print(filho.name, end=" ")
        print("erro: write aceita apenas dois parametros.")
        quit()
    else:
        for variable in var_battery[-1]:
            if variable.name == node.children[0].name:
                left_write = variable

        for routine in rotinas_acessaveis:
            if 'Function call' in node.children[0].name:
                if routine.name == str(re.findall(r'"(.*?)"', node.children[0].name)[0]):
                    left_write = routine

        if node.children[0].name.isdigit():
            left_write = node.children[0].name

        for variable in var_battery[-1]:
            if variable.name == node.children[1].name:
                right_write = variable

        for routine in rotinas_acessaveis:
            if 'Function call' in node.children[1].name:
                if routine.name == str(re.findall(r'"(.*?)"', node.children[1].name)[0]):
                    left_write = routine

        if node.children[1].name.isdigit():
            right_write = node.children[1].name

        if left_write is None or right_write is None:
            print(node.name, end=" ")
            for filho in node.children:
                print(filho.name, end="| ")
            print("erro: write em var inalcançável.")
            quit()
        else:
            pass


def read(node):

    var_read = None

    rotinas_acessaveis = get_rotinas_acessaveis(current_routine)

    if len(node.children) != 1:
        print(node.name, end=" ")
        for filho in node.children:
            print(filho.name, end=" ")
        print("erro: read aceita apenas um parametro.")
        quit()
    else:
        for variable in var_battery[-1]:
            if variable.name == node.children[0].name:
                var_read = variable

        for routine in rotinas_acessaveis:
            if 'Function call' in node.children[0].name:
                if routine.name == str(re.findall(r'"(.*?)"', node.children[0].name)[0]):
                    var_read = routine

        for lista in current_routine.symTab:
            for item in lista:
                if item.getName() == node.children[0].name:
                    var_read = item.getName()

        if var_read is None:
            print(node.name, end=" ")
            for filho in node.children:
                print(filho.name, end="| ")
            print("erro: read em variavel inalcançável.")
            quit()
        else:
            pass


def main(argv):
    global current_routine
    global nivel
    global var_battery

    first = True
    for pre, fill, node in ast:
        if first:  # se for a primeira vez:
            first = semantigo(node, first)

        # caso encontre uma dec de variavel na arvre:
        if node.name == 'var declaration':
            var_dec(node)

        # caso encontre uma atribuicao na arvre:
        elif node.name == 'atribuicao':
            atrib(node)

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

        elif node.name == 'Write':
            write(node)

        elif node.name == 'Read':
            read(node)

        elif node.name in operations:
            operation_routine(node)

        # o nó 'tabela de símbolos' siginficia dentro da arvre o fim de rotina
        if node.name == 'tabela de simbolos':
            var_battery.pop()  # da pop na pilha das variaveis
            nivel -= 1
            if current_routine.parent is not None:
                # coloca a rotina atual como a ultima
                current_routine = current_routine.parent
    print("Análise finalizada com sucesso.")


main('')
