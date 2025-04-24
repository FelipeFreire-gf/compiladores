%{
#include "parser.tab.h"  // Cabeçalho gerado pelo Bison
%}

DIGITO    [0-9]
LETRA     [a-zA-Z]
SIMBOLO   [!@#$%^&*()\-_=+\[\]{};:'",.<>/?\\|]

%%

{DIGITO}+               { yylval.str = strdup(yytext); return NUMERO; }
{DIGITO}+"."{DIGITO}+   { yylval.str = strdup(yytext); return NUMERO; }
{LETRA}+                { yylval.str = strdup(yytext); return PALAVRA; }
{SIMBOLO}+             { yylval.str = strdup(yytext); return SIMBOLO; }
[ \t\n]                 ;  // Ignora espaços, tabs e novas linhas
.                       { printf("Caractere desconhecido: %s\n", yytext); }

%%

// Função auxiliar para relatar erros léxicos
void yyerror(const char *s) {
    fprintf(stderr, "Erro léxico: %s\n", s);
}