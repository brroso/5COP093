#include "graph.h"

Vertice::Vertice(string name_)
{
    name = name_;
    link_list = new List;
}

string Vertice::getVerticeName()
{
    return name;
}

List *Vertice::getVerticeLinks()
{
    return link_list;
}

void Vertice::insertLink(Vertice destino){
    link_list->insert(destino.name);
}