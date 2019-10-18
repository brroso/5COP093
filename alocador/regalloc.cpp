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
    Vertice vert(s);
    top_vert->insertLink(vert);
    grafo->adj_list->insertVertice(top_vert);
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

    Graph *ordenado = new Graph;
    VerNode *noOrdenado;
    VerNode *min;

    for (k; k > 1; k--)
    {
        cout << "K = " + to_string(k) + "\n" << endl;

        ordenado = grafo->ord_by_grau();

        min = ordenado->get_n_min_grau();
        noOrdenado = ordenado->adj_list->head;


        while (min) // FAZ O PUSH
        {
            min = ordenado->get_n_min_grau();
            ordenado = ordenado->remove_and_rebuild(min);
            
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