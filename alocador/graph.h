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
        VerNode *get_n_min_grau();
        VerNode *get_n_max_grau();
        Graph *get_copy();
        Graph *ord_by_grau();
        Graph *remove_and_rebuild(VerNode *vert, int k);
};

#endif