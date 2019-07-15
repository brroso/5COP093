import pickle
from modules import *

ast = open('../ast', 'rb')
ast = pickle.load(ast)

operations = ['+', '-', '*', '/', '>', '<', '>=', '<=', '<>']
routines_battery = []
current_routine = None


def semantigo(node, first):
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


class routine(object):
    def __init__(self, name, symTab, parent=None):
        self.name = name
        self.symTab = symTab
        self.parent = parent


def main(argv):
    first = True
    for pre, fill, node in ast:
        if first:
            first = semantigo(node, first)
        # if node.name == 'var declaration':
        #     # vardec
        # elif node.name == 'atribuicao':
        #     # atrib
        # elif node.name == 'procedure dec':
        #     # procdec
        # elif 'Proc call' in node.name:
        #     # proccall
        # elif node.name == 'function dec':
        #     # funcdec
        # elif 'Function call' in node.name:
        #     # funccall
        # elif node.name == 'Write':
        #     # write
        # elif node.name == 'Read':
        #     # read
        # elif node.name in operations:
        #     # comparacao


main('')