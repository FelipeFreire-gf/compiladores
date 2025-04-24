%{
#include "parser.tab.h"  // Cabeçalho gerado pelo Bison
extern void yyerror(const char *s);  // Declaração externa da função
%}

DIGITO    [0-9]
LETRA     [a-zA-Z]
SIMBOLO   [!@#$%^&*()\-_=+\[\]{};:'",.<>/?\\|~`´¨ªº°§¬¢£¥€©®™±×÷√∞µ∑∏∂∫∆∇∮∯∰∱∲∳∴∵∶∷≅≈≠≡≤≥≪≫≬≭≮≯≰≱≲≳≴≵≶≷≸≹≺≻≼≽≾≿⊀⊁⊂⊃⊄⊅⊆⊇⊈⊉⊊⊋⊌⊍⊎⊏⊐⊑⊒⊓⊔⊕⊖⊗⊘⊙⊚⊛⊜⊝⊞⊟⊠⊡⊢⊣⊤⊥⊦⊧⊨⊩⊪⊫⊬⊭⊮⊯⊰⊱⊲⊳⊴⊵⊶⊷⊸⊹⊺⊻⊼⊽⊾⊿⋀⋁⋂⋃⋄⋅⋆⋇⋈⋉⋊⋋⋌⋍⋎⋏⋐⋑⋒⋓⋔⋕⋖⋗⋘⋙⋚⋛⋜⋝⋞⋟⋠⋡⋢⋣⋤⋥⋦⋧⋨⋩⋪⋫⋬⋭⋮⋯⋰⋱⋲⋳⋴⋵⋶⋷⋸⋹⋺⋻⋼⋽⋾⋿]

%%

{DIGITO}+               { yylval.str = strdup(yytext); return NUMERO; }
{DIGITO}+"."{DIGITO}+   { yylval.str = strdup(yytext); return NUMERO; }
{LETRA}+                { yylval.str = strdup(yytext); return PALAVRA; }
{SIMBOLO}+             { yylval.str = strdup(yytext); return SIMBOLO; }
[ \t\n]                 ;  // Ignora espaços, tabs e novas linhas
.                       { printf("Caractere desconhecido: %s\n", yytext); }

%% 