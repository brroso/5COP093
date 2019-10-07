#include "graph.h"

Aresta::Aresta(string name_)
{
    name = name_;
}

string Aresta::getArestaName()
{
    return name;
}

list <Aresta> Aresta::getArestaLinks()
{
    return link_list;
}

void insertLink(Aresta origem, Aresta destino){
    origem.getArestaLinks().push_back(destino);
}