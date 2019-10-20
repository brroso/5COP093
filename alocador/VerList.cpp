#include "VerList.h"
#include <stdlib.h>

VerList::VerList()
{
    head = NULL;
    tail = NULL;
    size = 0;
}
int VerList::lenght()
{
    return size;
}

int VerList::isListEmpty()
{
    return size == 0;
}

void VerList::insertVertice(Vertice *v)
{
    VerNode *node = new VerNode;
    node->v = v;
    if (head == NULL)
    {
        head = node;
        tail = node;
    }
    else
    {
        tail->next = node;
        node->previous = tail;
        tail = node;;
    }
    size++;
}

void VerList::removeLast()
{
    tail = tail->previous;
    tail->next = NULL;
}

void VerList::removeVerNode(VerNode *node)
{
    if (node != NULL)
    {
        if (node->previous == NULL)
        {
            head = node->next;
        }
        else
        {
            node->previous->next = node->next;
        }
        if (node->next == NULL)
        {
            tail = node->previous;
        }
        else
        {
            node->next->previous = node->previous;
        }
        size--;
    }
}

VerNode *VerList::popVert()
{
    VerNode *node;

    if (tail != NULL)
    {
        node = tail;
        if (tail == head)
        {
            tail = NULL;
            head = NULL;
        }
        else
        {
            tail = tail->previous;
            tail->next == NULL;
        }
        delete node;
        size--;
    }
    return node;
}

VerNode::~VerNode()
{
    delete []v;
    delete []next;
    delete []previous;
}

/* FUNCOES NODE ========================================================================== */

VerNode::VerNode()
{
    v = NULL;
    next = NULL;
    previous = NULL;
}

Vertice *VerNode::get()
{
    return v;
}
// VERTICE

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

void Vertice::insertLink(Vertice destino)
{
    link_list->insert(destino.name);
}