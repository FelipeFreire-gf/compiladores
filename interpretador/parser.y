%{
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

extern int yylex();
extern FILE *yyin;

void yyerror(const char *s);
%}

%union {
    char *str;
}

%token <str> NUMERO PALAVRA SIMBOLO

/* Palavras reservadas */
%token IF ELSE WHILE FOR DO BREAK CONTINUE RETURN
%token INT FLOAT CHAR VOID
%token TRUE FALSE
%token AND OR NOT
%token PRINT SCAN

%%

input:
    /* vazio */
    | input token
;

token:
    NUMERO   { printf("Número: %s\n", $1); free($1); }
    | PALAVRA { printf("Palavra: %s\n", $1); free($1); }
    | SIMBOLO { printf("Símbolo: %s\n", $1); free($1); }
    | IF { printf("Palavra reservada: if\n"); }
    | ELSE { printf("Palavra reservada: else\n"); }
    | WHILE { printf("Palavra reservada: while\n"); }
    | FOR { printf("Palavra reservada: for\n"); }
    | DO { printf("Palavra reservada: do\n"); }
    | BREAK { printf("Palavra reservada: break\n"); }
    | CONTINUE { printf("Palavra reservada: continue\n"); }
    | RETURN { printf("Palavra reservada: return\n"); }
    | INT { printf("Palavra reservada: int\n"); }
    | FLOAT { printf("Palavra reservada: float\n"); }
    | CHAR { printf("Palavra reservada: char\n"); }
    | VOID { printf("Palavra reservada: void\n"); }
    | TRUE { printf("Palavra reservada: true\n"); }
    | FALSE { printf("Palavra reservada: false\n"); }
    | AND { printf("Palavra reservada: and\n"); }
    | OR { printf("Palavra reservada: or\n"); }
    | NOT { printf("Palavra reservada: not\n"); }
    | PRINT { printf("Palavra reservada: print\n"); }
    | SCAN { printf("Palavra reservada: scan\n"); }
;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Erro sintático: %s\n", s);
}

int main(int argc, char *argv[]) {
    if (argc > 1) {
        yyin = fopen(argv[1], "r");
        if (!yyin) {
            perror("Erro ao abrir o arquivo");
            return 1;
        }
    }
    yyparse();
    fclose(yyin);
    return 0;
}