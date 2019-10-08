#ifndef GRAPH_H
#define GRAPH_H
#include <string>
#include <stdio.h>
#include "VerList.h"
#include <string>

using namespace std;

class Graph
{
    public:
        VerList *adj_list;
        Graph();
};

#endif