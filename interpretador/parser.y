%{
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "tabela.h" // Inclua a tabela de símbolos

TabelaSimbolos *tabela; // Tabela de símbolos global

extern int yylex();
extern FILE *yyin;

void yyerror(const char *s);
%}

%union {
    char *str;
    int valor;
}

%token <str> NUMERO PALAVRA SIMBOLO
%token <valor> TRUE FALSE

/* Palavras reservadas */
%token IF ELSE WHILE FOR DO BREAK CONTINUE RETURN
%token INT FLOAT CHAR VOID
%token AND OR NOT
%token PRINT SCAN

/* Símbolos especiais */
%token ABRE_PARENTESES FECHA_PARENTESES
%token ABRE_CHAVES FECHA_CHAVES
%token PONTO_VIRGULA

/* Tipos de retorno */
%type <str> tipo
%type <valor> condicao
%type <valor> expressao

/* Precedência e associatividade */
%right ELSE
%left '+' '-'
%left '*' '/'

%%

programa: 
    /* vazio */
    | programa linha
;

linha:
    declaracao
    | atribuicao
    | estrutura
;

declaracao:
    tipo PALAVRA PONTO_VIRGULA {
        if (!inserir_simbolo(tabela, $2, $1, 0)) {
            printf("Erro: Variável '%s' já declarada no escopo atual.\n", $2);
        } else {
            printf("Variável '%s' do tipo '%s' declarada com sucesso.\n", $2, $1);
        }
        free($2);
    }
;

atribuicao:
    PALAVRA '=' expressao PONTO_VIRGULA {
        printf("Token PALAVRA: %s\n", $1);
        printf("Valor da expressao: %d\n", $3);
        if (!buscar_simbolo(tabela, $1, 0)) {
            printf("Erro: Variável '%s' não declarada.\n", $1);
        } else {
            printf("Atribuição válida para a variável '%s'.\n", $1);
        }
        free($1);
    }
;

expressao:
    NUMERO {
        $$ = $1; // Retorna o valor do número
    }
    | expressao '+' expressao {
        $$ = $1 + $3; // Soma
    }
    | expressao '-' expressao {
        $$ = $1 - $3; // Subtração
    }
    | expressao '*' expressao {
        $$ = $1 * $3; // Multiplicação
    }
    | expressao '/' expressao {
        if ($3 == 0) {
            yyerror("Erro: Divisão por zero.");
            $$ = 0;
        } else {
            $$ = $1 / $3; // Divisão
        }
    }
;

tipo:
    INT { $$ = "int"; }
    | FLOAT { $$ = "float"; }
    | CHAR { $$ = "char"; }
;

estrutura:
    if_stmt
    | print_stmt
    | bloco
;

if_stmt:
    IF ABRE_PARENTESES condicao FECHA_PARENTESES bloco
    | IF ABRE_PARENTESES condicao FECHA_PARENTESES bloco ELSE bloco
;

print_stmt:
    PRINT ABRE_PARENTESES PALAVRA FECHA_PARENTESES PONTO_VIRGULA
    { printf("Imprimindo: %s\n", $3); free($3); }
;

bloco:
    ABRE_CHAVES conteudo_bloco FECHA_CHAVES
;

conteudo_bloco:
    /* vazio */
    | conteudo_bloco linha
;

token:
    NUMERO              { printf("Número: %s\n", $1); free($1); }
    | PALAVRA           { printf("Palavra: %s\n", $1); free($1); }
    | '+'               { printf("Operador: +\n"); }
    | '-'               { printf("Operador: -\n"); }
    | '*'               { printf("Operador: *\n"); }
    | '/'               { printf("Operador: /\n"); }
    | SIMBOLO           { printf("Símbolo: %s\n", $1); free($1); }
    | IF               { printf("Palavra reservada: if\n"); }
    | ELSE             { printf("Palavra reservada: else\n"); }
    | WHILE            { printf("Palavra reservada: while\n"); }
    | FOR              { printf("Palavra reservada: for\n"); }
    | DO               { printf("Palavra reservada: do\n"); }
    | BREAK            { printf("Palavra reservada: break\n"); }
    | CONTINUE         { printf("Palavra reservada: continue\n"); }
    | RETURN           { printf("Palavra reservada: return\n"); }
    | INT              { printf("Palavra reservada: int\n"); }
    | FLOAT            { printf("Palavra reservada: float\n"); }
    | CHAR             { printf("Palavra reservada: char\n"); }
    | VOID             { printf("Palavra reservada: void\n"); }
    | TRUE             { printf("Palavra reservada: true\n"); }
    | FALSE            { printf("Palavra reservada: false\n"); }
    | AND              { printf("Palavra reservada: and\n"); }
    | OR               { printf("Palavra reservada: or\n"); }
    | NOT              { printf("Palavra reservada: not\n"); }
    | PRINT            { printf("Palavra reservada: print\n"); }
    | SCAN             { printf("Palavra reservada: scan\n"); }
;

condicao:
    TRUE    { $$ = 1; }
    | FALSE { $$ = 0; }
    | PALAVRA {
        if (!buscar_simbolo(tabela, $1, 0)) {
            printf("Erro: Variável '%s' não declarada na condição.\n", $1);
        } else {
            printf("Avaliando condição: %s\n", $1);
        }
        free($1);
        $$ = 1;
    }
;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Erro sintático: %s\n", s);
}

int main(int argc, char *argv[]) {
    tabela = criar_tabela(); // Inicializa a tabela de símbolos
    if (argc > 1) {
        yyin = fopen(argv[1], "r");
        if (!yyin) {
            perror("Erro ao abrir o arquivo");
            return 1;
        }
    }
    yyparse();
    imprimir_tabela(tabela); // Imprime a tabela ao final
    destruir_tabela(tabela); // Libera a memória da tabela
    fclose(yyin);
    return 0;
}