#ifndef list_H
#define list_H
#include <string>
#include <stdio.h>
#include <iostream>

using namespace std;

class Node
{
    public:
        string value;
        Node *next;
        Node *previous;

        Node();
        bool operator==(const Node &s) const { return value == s.value &&
                                                      next == s.next &&
                                                      previous == s.previous; }
        void newNode(string value);
        string get();
        Node *getNext();
        void setValue(string s);
};

class List
{
    public:
        Node *head;
        Node *tail;
        int size;

        List();
        int lenght();
        int isListEmpty();
        void insert(string value);
        void removeNode(Node *node);
        Node getFirst();
        Node *popNode();
        void printList();
};

#endif
