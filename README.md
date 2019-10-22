# 5COP093

Trabalhos da disciplina de compiladores de 2019.

# COMPILADOR

## Instrução de execução:

`python3 lexer.py/parser.py -i [arquivo de entrada] -o [arquivo de saída]`

lexer.py faz a analise léxica de um código da linguagem pascal utilizada no livro Implementação de linguagens de programação de Thomasz Kowaltowski.

parser.py faz a análise sintática dos resultados da análise léxica anterior.

o arquivo semantico.py vai pegar a ast gerada pelo sintático e fazer a análise semântica.

# REGALLOC

## Descrição

Trabalho de alocação de registradores usando algoritmo de coloração de grafo.