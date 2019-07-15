import pickle
from modules import *

ast = open('../ast', 'rb')
ast = pickle.load(ast)

operations = ['+', '-', '*', '/', '>', '<', '>=', '<=', '<>']
routines_battery = []
current_symTab = []


class routine(object):
    def __init__(self, name, symTab, parent=None):
        self.name = name
        self.symTab = symTab
        self.parent = parent


def main(argv):
    first = True
    for pre, fill, node in ast:
        if first:
            for no in node.children:
                if no.name == 'tabela de simbolos':
                    symTab = no.ht
            main = routine(node.name, symTab)
            print_hash(main.symTab)
            first = False
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