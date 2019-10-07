#include <stdlib.h>
#include <string>
#include <iostream>
#include <stdio.h>
#include <fstream>
#include "graph.h"
#include "list.h"

string nome_grafo;
int cores;

void process_graph_name(string s)
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

void process_k(string s)
{
    int pos;
    std::string delimiter = "=";
    pos = s.find(delimiter);
    std::string token = s.substr(0, pos);
    s.erase(0, pos + delimiter.length());
    cores = stoi(s);
    cout << nome_grafo + " -> Physical Registers: " << to_string(cores) << endl;
}

void build_line(string s)
{

}

int main(int argc, char const *argv[])
{
    string line;
    int count;
    count = 0;
    while (cin){
        if (count == 0){
            getline(cin, line);
            process_graph_name(line);
            count++;
        }else if (count == 1){
            getline(cin, line);
            process_k(line);
            count++;
        }else{
            getline(cin, line);
            build_line(line);
            count++;
        }
    }
}

