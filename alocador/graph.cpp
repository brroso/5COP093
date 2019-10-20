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
    VerNode *minGrauNode = no;
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

VerNode *Graph::get_n_max_grau()
{
    int maxGrau = 0;
    VerNode *no = adj_list->head;
    VerNode *maxGrauNode = no;
    while (no) // RODA AS CABEÇAS
    {
        if (no->v->link_list->lenght() > maxGrau)
        {
            maxGrau = no->v->link_list->lenght();
            maxGrauNode = no;
        }
        no = no->next;
    }

    return maxGrauNode;
}

Graph *Graph::get_copy()
{
    Graph *copy = new Graph;
    VerNode *org_root = adj_list->head;
    while (org_root)
    {
        Vertice *top_vert = new Vertice(org_root->get()->getVerticeName());
        Node *vnode = org_root->get()->getVerticeLinks()->head;
        while (vnode)
        {
            Vertice vert(vnode->get());
            top_vert->insertLink(vert);
            vnode = vnode->next;
        }
        copy->adj_list->insertVertice(top_vert);
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

Graph *Graph::remove_and_rebuild(VerNode *vert, int k, VerList *stack)
{

    VerNode *copy_root = adj_list->head;
    while(copy_root)
    {
        if (copy_root->get()->getVerticeName().compare(vert->get()->getVerticeName()) == 0)
        {
            if (copy_root->get()->getVerticeLinks()->lenght() >= k)
            {
                vert = get_n_max_grau();
                adj_list->removeVerNode(vert);
                stack->insertVertice(vert->get());
                cout << "Push: " + vert->get()->getVerticeName() + " *"<< endl;
            }
            else{
                copy_root = adj_list->head;
                adj_list->removeVerNode(vert);
                stack->insertVertice(vert->get());
                cout << "Push: " + vert->get()->getVerticeName() << endl;
            }
        }
        if (adj_list->head == NULL)
        {
            return this;
        }
        copy_root = copy_root->next;
    }

    copy_root = adj_list->head;
    while(copy_root){
        Node *no_interno = copy_root->get()->getVerticeLinks()->head;
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

    VerNode *no = adj_list->head; // PRINT GRAFO TESTE

    /*while (no) // RODA AS CABEÇAS
    {
        cout << no->v->name + " -->";
        Node *no_interno = no->v->link_list->head;
        cout << "GRAU: " << to_string(no->v->link_list->lenght()) << " || ";
        while (no_interno) // RODA OS VÉRTICES
        {
            cout << " ";
            cout << no_interno->value;
            no_interno = no_interno->next;
        }
        no = no->next;
        cout << endl;
    }
    */

    return this;
}
