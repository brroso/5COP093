#ifndef VERLIST_h
#define VERLIST_h
#include <string>
#include <stdio.h>
#include <iostream>
#include "list.h"

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
};

class VerNode
{
public:
    Vertice *v;
    VerNode *next;
    VerNode *previous;
    VerNode();
    bool operator==(const VerNode &s) const { return v == s.v &&
                                                  next == s.next &&
                                                  previous == s.previous; }
    void newVerNode(Vertice v);
    Vertice *get();
    VerNode *getNext();
    void setValue(Vertice v);
};

class VerList
{
public:
    VerNode *head;
    VerNode *tail;
    int size;

    VerList();
    int lenght();
    int isListEmpty();
    void insertVertice(Vertice *v);
    void removeVerNode(VerNode *node);
    VerNode getFirst();
    VerNode *popVert();
    void printList();
    void removeLast();
};

#endif
