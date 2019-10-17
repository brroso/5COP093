#include "graph.h"

// módulos do grafo

Graph::Graph()
{
    adj_list = new VerList;
}

VerNode *Graph::get_n_min_grau()
{
    int minGrau = 9999;
    VerNode *no = adj_list->head; 
    VerNode *minGrauNode = NULL;
    while (no) // RODA AS CABEÇAS
    {
        if (no->v->link_list->lenght() < minGrau)
        {
            minGrau = no->v->link_list->lenght();
            minGrauNode = no;
        }
        no = no->next;
    }

    return minGrauNode;
}

Graph *Graph::get_copy()
{
    Graph *copy = new Graph;
    VerNode *org_root = adj_list->head;
    while (org_root)
    {
        copy->adj_list->insertVertice(org_root->get());
        org_root = org_root->next;
    }

    return copy;
}

Graph *Graph::ord_by_grau()
{
    Graph *copy = new Graph;
    copy = get_copy();
    Graph *ordenado = new Graph;
    VerNode *org_root = copy->adj_list->head;
    while(org_root)
    {
        ordenado->adj_list->insertVertice(copy->get_n_min_grau()->get());
        copy->adj_list->removeVerNode(copy->get_n_min_grau());
        org_root = copy->adj_list->head;
    }

    return ordenado;
}

Graph *Graph::remove_and_rebuild(VerNode *vert)
{
    Graph *copy = new Graph;
    copy = get_copy();

    VerNode *copy_root = copy->adj_list->head;
    while(copy_root)
    {
        if (copy_root->get()->getVerticeName().compare(vert->get()->getVerticeName()) == 0)
        {
            copy_root = copy_root->next;
            copy->adj_list->removeVerNode(vert);
        }else
        {
            Node *no_interno = copy_root->v->link_list->head;
            while (no_interno) // RODA OS VÉRTICES
            {
                if (no_interno->value.compare(vert->get()->getVerticeName()) == 0)
                {
                    copy_root->v->link_list->removeNode(no_interno);
                }
                no_interno = no_interno->next;
            }
            copy_root = copy_root->next;
        }

    }
    return copy;
}