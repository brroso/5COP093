import sys
import getopt

#reserved_word = 0
#special_symbol = 1
#double_special_symbol = 2
#integer_numer = 3
#float_number = 4
#positive_float_number = 5
#negative_float_number = 6
#identifier = 7

def get_token_value(token):
    if token == 'palavra reservada':
        return 0
    elif token == 'simbolo especial':
        return 1
    elif token == 'simbolo especial composto':
        return 2
    elif token == 'número inteiro':
        return 3
    elif token == 'número real':
        return 4
    elif token == 'numero real positivo':
        return 5
    elif token == 'numero real negativo':
        return 6
    elif token == 'identificador':
        return 7
    else:
        return -1

def main(argv):
    # Leitura dos argumentos
    token_values = []
    try:   
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('main.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
    print('Input file is "', input_file, '"')
    print('Output file is "', output_file, '"')
    output = open(output_file, "w")
    with open(input_file, "r") as f:   # Roda todo o arquivo char por char
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            if 'categoria' in line:
                category = line.split("da categoria ", 1)[1]
                token_values.append(get_token_value(category))
    token_values = [x for x in token_values if x != -1]
    print(token_values, file=output)

main(sys.argv[1:])
