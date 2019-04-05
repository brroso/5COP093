size = 211


def new_table():
    table = []
    i = 0
    while i < size:
        new_list = []
        table.append(new_list)
        i = i + 1
    return table


def hash(key):
    hash_value = 0
    alfa = 7
    for i in range(len(key)):
        hash_value = alfa * hash_value + ord(key[i])
    hash_value = hash_value % (size)
    return hash_value


def hash_insert(table, object):
    index = hash(object.getName())
    table[index].append(object)
    return 0


def hash_search(table, string):
    index = hash(string)
    for object in table[index]:
        if object.getName() == string:
            return object
    return -1
