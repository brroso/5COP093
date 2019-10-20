CXX = g++
CXXFLAGS = -std=c++17

OBJECTS = regalloc.o list.o VerList.o graph.o

regalloc: $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $@ $^

$(OBJECTS): regalloc.cpp list.cpp VerList.cpp graph.cpp

clean:
	rm *.o