#include <stdlib.h>
#include <string>
#include <iostream>
#include <stdio.h>
#include <fstream>
#include "graph.h"
#include "VerList.h"
#include "list.h"

string nome_grafo;
int cores;
Graph *grafo;

void process_graph_name(string s) // PEGA O NOME DO GRAFO
{
    int pos;
    std::string delimiter = " ";
    pos = s.find(delimiter);
    std::string token = s.substr(0, pos);
    s.erase(0, pos + delimiter.length());
    delimiter = ":";
    token = s.substr(0, s.find(delimiter));
    nome_grafo = "Graph " + token;
}

void process_k(string s) // PEGA A QTD DE CORES
{
    int pos;
    std::string delimiter = "=";
    pos = s.find(delimiter);
    std::string token = s.substr(0, pos);
    s.erase(0, pos + delimiter.length());
    cores = stoi(s);
    cout << nome_grafo + " -> Physical Registers: " << to_string(cores) << endl;
    cout << "----------------------------------------" << endl;
    cout << "----------------------------------------" << endl;
}

void build_line(string s) // CRIA O GRAFO
{
    int pos;
    std::string delimiter = " -->";
    pos = s.find(delimiter);
    std::string token = s.substr(0, pos);
    Vertice *top_vert = new Vertice(token);
    s.erase(0, pos + delimiter.length());
    s.erase(0, 1);
    delimiter = " ";
    while ((pos = s.find(delimiter)) != std::string::npos)
    {
        pos = s.find(delimiter);
        token = s.substr(0, pos);
        Vertice vert(token);
        top_vert->insertLink(vert);
        s.erase(0, pos + delimiter.length());
    }
    if (s.c_str()[s.size() - 1] == '\n' or s.c_str()[s.size() - 1] == ' ')
    {
        s.erase(s.size() - 1);
    }
    Vertice vert(s);
    top_vert->insertLink(vert);
    grafo->adj_list->insertVertice(top_vert);
}

int getMinFromAvColors(int *avColors, int k)
{
    int min = 9999;
    int i;
    for (i = 0; i < k; i++)
    {
        if (avColors[i] >= 0 && avColors[i] < min)
        {
            min = avColors[i];
        }
    }
    return min;
}

int isAvailable(int *avColors, string vname, int k)
{
    int ret = 0;
    int i;
    for (i = 0; i < k; i++)
    {
        if (to_string(avColors[i]).compare(vname) == 0)
        {
            ret = 1;
        }
    }
    return ret;
}

void removeFromAvColors(int *avColors, string vname, int k)
{
    int i;
    for (i = 0; i < k; i++)
    {
        if (to_string(avColors[i]).compare(vname) == 0)
        {
            avColors[i] = -1;
        }
    }
}

string assign(VerNode *node, VerList *stack, int k)
{
    int *avColors = (int *) malloc(sizeof(int) * k);

    int i;

    for (i = 0; i < k; i++)
    {
        avColors[i] = i;
    }

    Node *auxNode = node->get()->getVerticeLinks()->head;

    while(auxNode)
    {
        if (isAvailable(avColors, auxNode->get(), k))
        {
            removeFromAvColors(avColors, auxNode->get(), k);
        }
        auxNode = auxNode->next;
    }

    int ret = getMinFromAvColors(avColors, k);

    VerNode *auxNodeStack = stack->tail;

    while (auxNodeStack) // MUDA A REFERENCIA PELO VALOR
    {
        Node *no_interno = auxNodeStack->v->link_list->head;
        while (no_interno) // RODA OS VÉRTICES
        {
            if (no_interno->get().compare(node->get()->getVerticeName()) == 0)
            {
                no_interno->setValue(to_string(ret));  
            }
            no_interno = no_interno->next;
        }
        auxNodeStack = auxNodeStack->previous;
    }

    free(avColors);

    return to_string(ret);

}

int main(int argc, char const *argv[])
{
    grafo = new Graph;
    string line;
    int count;
    count = 0;
    Vertice *lastOne;

    while (cin){
        if (count == 0){ // PEGA O NOME DO GRAFO DA PRIMEIRA LINHA
            getline(cin, line);
            process_graph_name(line);
            count++;
        }else if (count == 1){ // PEGA O K DA SEGUNDA LINHA
            getline(cin, line);
            process_k(line);
            count++;
        }else{ // COLOCA VERTICE NO GRAFO
            getline(cin, line);
            build_line(line);
            count++;
        }
    }

    grafo->adj_list->removeLast(); // CIN PEGA 2X A ULTIMA LINHA
    // Começa o algoritmo
    
    int k = cores;

    int *result = (int *) malloc(sizeof(int *) * cores - 2);

    Graph *grafo_aux = new Graph;
    VerNode *min;

    for (k; k > 1; k--) // SIMPLIFY
    {
        result[k-2] = 1;
        VerList *stack = new VerList;
        cout << "K = " + to_string(k) + "\n" << endl;
        grafo_aux = grafo->get_copy();
        min = grafo_aux->get_n_min_grau();


        while (min) // FAZ O PUSH
        {
            min = grafo_aux->get_n_min_grau();
            grafo_aux = grafo_aux->remove_and_rebuild(min, k, stack);
        }

        VerNode *node;
        node = stack->tail;

        while (node) // ASSIGN
        {
            string color = assign(node, stack, k);
            if (atoi(color.c_str()) == 9999)
            {
                cout << "Pop: " + node->get()->getVerticeName() + " -> " + "NO COLOR AVAILABLE" << endl;
                result[k-2] = 0;
                break;
            }else{
                cout << "Pop: " + node->get()->getVerticeName() + " -> " + color << endl;
            }
            node = node->previous;
        }

        cout << "----------------------------------------" << endl;
    }

    cout << "----------------------------------------" << endl;

    int i;

    for (i = cores; i > 1; i--)
    {
        if ( i >= 10)
        {
            if (result[i-2] == 1){
            cout << nome_grafo + " -> " + "K = " + to_string(i) + ": Successful Allocation";
            }else{
                cout << nome_grafo + " -> " + "K = " + to_string(i) + ": SPILL";
            }
        }else
        {
            if (result[i-2] == 1){
            cout << nome_grafo + " -> " + "K =  " + to_string(i) + ": Successful Allocation";
            }else{
                cout << nome_grafo + " -> " + "K =  " + to_string(i) + ": SPILL";
            }
        }
        if (i != 2)
        {
            cout << endl;
        }
    }

}

/*
    VerNode *no = grafo->adj_list->head; // PRINT GRAFO TESTE

    while (no) // RODA AS CABEÇAS
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