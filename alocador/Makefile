############################# Makefile ##########################
all: regalloc
regalloc: list.o graph.o VerList.o 
	g++ -g list.cpp graph.cpp VerList.cpp regalloc.cpp -o regalloc
	rm -rf *.o
