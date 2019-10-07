#ifndef GRAPH_H
#define GRAPH_H
#include <string>
#include <stdio.h>
#include <list>

using namespace std;
class Aresta
{

private:
    string name;
    list <Aresta> link_list;

public:
    Aresta(string name_);
    string getArestaName();
    list <Aresta> getArestaLinks();
    void insertLink(Aresta origem, Aresta destino);
    ~Aresta();
};
#endif