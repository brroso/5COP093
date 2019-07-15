import pickle
from modules import *

ast = open('../ast', 'rb')
ast = pickle.load(ast)
for pre, fill, node in ast:
    print(pre, node.name)
    if node.name == 'tabela de simbolos':
        print_hash(node.ht)