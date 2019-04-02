size = 211


def new_table():
    table = []
    i = 1
    while i < size:
        new_list = []
        table.append(new_list)
        i = i + 1
    return table


def hash(string):
    # TODO -- refazer função hash
    value = ord(string[0])
    value = value % size
    return value


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
