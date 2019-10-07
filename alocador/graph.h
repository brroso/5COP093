#ifndef GRAPH_H
#define GRAPH_H
#include <string>
#include <stdio.h>
#include "list.h"
#include <string>

using namespace std;
class Vertice
{
public:
    string name;
    List *link_list;
    Vertice(string name_);
    string getVerticeName();
    List *getVerticeLinks();
    void insertLink(Vertice destino);
    ~Vertice();
};

#endif