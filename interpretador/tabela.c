#include "tabela.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

TabelaSimbolos* criar_tabela() {
    TabelaSimbolos *tabela = (TabelaSimbolos *)malloc(sizeof(TabelaSimbolos));
    tabela->primeiro = NULL;
    return tabela;
}

void destruir_tabela(TabelaSimbolos *tabela) {
    Simbolo *atual = tabela->primeiro;
    while (atual) {
        Simbolo *temp = atual;
        atual = atual->proximo;
        free(temp->nome);
        free(temp->tipo);
        free(temp);
    }
    free(tabela);
}

bool inserir_simbolo(TabelaSimbolos *tabela, const char *nome, const char *tipo, int escopo) {
    if (buscar_simbolo(tabela, nome, escopo)) {
        return false; 
    }

    Simbolo *novo = (Simbolo *)malloc(sizeof(Simbolo));
    novo->nome = strdup(nome);
    novo->tipo = strdup(tipo);
    novo->escopo = escopo;
    novo->proximo = tabela->primeiro;
    tabela->primeiro = novo;
    return true;
}

Simbolo* buscar_simbolo(TabelaSimbolos *tabela, const char *nome, int escopo) {
    Simbolo *atual = tabela->primeiro;
    while (atual) {
        if (strcmp(atual->nome, nome) == 0 && atual->escopo == escopo) {
            return atual;
        }
        atual = atual->proximo;
    }
    return NULL;
}

void imprimir_tabela(TabelaSimbolos *tabela) {
    Simbolo *atual = tabela->primeiro;
    printf("Tabela de Símbolos:\n");
    printf("Nome\tTipo\tEscopo\n");
    while (atual) {
        printf("%s\t%s\t%d\n", atual->nome, atual->tipo, atual->escopo);
        atual = atual->proximo;
    }
}