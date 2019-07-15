import pickle
from modules import *

ast = open('../ast', 'rb')
ast = pickle.load(ast)


operations = ['+', '-', '*', '/', '>', '<', '>=', '<=', '<>']

def main(argv):
    global ast
    for pre, fill, node in ast:
        print(pre, node.name)
        if node.name == 'var declaration':
            # vardec
        elif node.name == 'atribuicao':
            # atrib
        elif node.name == 'procedure dec':
            # procdec
        elif 'Proc call' in node.name:
            # proccall
        elif node.name == 'function dec':
            # funcdec
        elif 'Function call' in node.name:
            # funccall
        elif node.name == 'Write':
            # write
        elif node.name == 'Read':
            # read
        elif node.name in operations:
            # comparacao
