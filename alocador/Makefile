CXX = g++
CXXFLAGS = -std=c++0x

OBJECTS = regalloc.o list.o VerList.o graph.o

regalloc: $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $@ $^

$(OBJECTS): regalloc.cpp list.cpp VerList.cpp graph.cpp

clean:
	rm *.omak