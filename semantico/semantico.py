import pickle
from modules import *

ast = open('../ast', 'rb')
ast = pickle.load(ast)
for pre, fill, node in ast:
    print(pre, node.name)