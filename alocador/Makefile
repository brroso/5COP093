# My first makefile
 
all: regalloc
 
regalloc: regalloc.o graph.o
	gcc -o regalloc regalloc.o graph.o
 
regalloc.o: regalloc.cpp graph.h
	gcc -o regalloc.o regalloc.cpp -c -W -Wall -ansi -pedantic
 
graph.o: graph.cpp graph.h
	gcc -o graph.o graph.cpp -c -W -Wall -ansi -pedantic
 
clean:
	rm -rf *.o *~ regalloc
