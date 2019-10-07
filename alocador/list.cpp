#include "list.h"
#include <stdlib.h>

List::List(){
    head = NULL;
    tail = NULL;
    size = 0;
}
int List::lenght()
{
    return size;
}

int List::isListEmpty()
{
    return size == 0;
}

void List::insert(string _value)
{
    Node *node = new Node;
    node->value = _value;
    if (head == NULL)
    {
        head = node;
        tail = node;
    }
    else
    {
        tail->next = node;
        node->previous = tail;
        tail = node;
    }
    size++;
}

void List::removeNode(Node *node)
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
        delete node;
        size--;
    }
}

Node *List::popNode()
{
    Node *node;

	if(tail != NULL){
	    node = tail;
	    if( tail == head ){
	        tail = NULL;
	        head = NULL;
	    }
	    else{
	        tail = tail->previous;
	        tail->next == NULL;
	    }
	    delete node;
	    size--;
	}
	return node;
}

void List::printList()
{
    Node *node = new Node;
    node = head;
    cout << "printing" << endl;
    while (node != NULL){
        cout << node->value + " ";
        node = node->next;
    }
        
}

    /* FUNCOES NODE ========================================================================== */

Node::Node()
{
    value = "";
    next = NULL;
    previous = NULL;
}

void Node::newNode(string _value)
{   
    value = _value;
}

Node *Node::getNext()
{
    return next;
}


string Node::get()
{
    return value;
}

void Node::setValue(string s)
{
    value = s;
}
