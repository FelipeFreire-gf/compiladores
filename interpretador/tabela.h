#ifndef TABELA_H
#define TABELA_H

#include <stdbool.h>

typedef struct Simbolo {
    char *nome;          
    char *tipo;          
    int escopo;          
    struct Simbolo *proximo;
} Simbolo;

typedef struct TabelaSimbolos {
    Simbolo *primeiro; 
} TabelaSimbolos;

TabelaSimbolos* criar_tabela();
void destruir_tabela(TabelaSimbolos *tabela);
bool inserir_simbolo(TabelaSimbolos *tabela, const char *nome, const char *tipo, int escopo);
Simbolo* buscar_simbolo(TabelaSimbolos *tabela, const char *nome, int escopo);
void imprimir_tabela(TabelaSimbolos *tabela);

#endif 