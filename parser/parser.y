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

%%

input:
    /* vazio */
    | input token
;

token:
    NUMERO   { printf("Número: %s\n", $1); free($1); }
    | PALAVRA { printf("Palavra: %s\n", $1); free($1); }
    | SIMBOLO { printf("Símbolo: %s\n", $1); free($1); }
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