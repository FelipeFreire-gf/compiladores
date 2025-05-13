%{
#include "parser.tab.h"  // Cabeçalho gerado pelo Bison
%}

DIGITO    [0-9]
LETRA     [a-zA-Z]
ID        [a-zA-Z][a-zA-Z0-9_]*
SIMBOLO   [!@#$%^&*()\-_=+\[\]{};:'",.<>/?\\|~`´¨ªº°§¬¢£¥€©®™±×÷√∞µ∑∏∂∫∆∇∮∯∰∱∲∳∴∵∶∷≅≈≠≡≤≥≪≫≬≭≮≯≰≱≲≳≴≵≶≷≸≹≺≻≼≽≾≿⊀⊁⊂⊃⊄⊅⊆⊇⊈⊉⊊⊋⊌⊍⊎⊏⊐⊑⊒⊓⊔⊕⊖⊗⊘⊙⊚⊛⊜⊝⊞⊟⊠⊡⊢⊣⊤⊥⊦⊧⊨⊩⊪⊫⊬⊭⊮⊯⊰⊱⊲⊳⊴⊵⊶⊷⊸⊹⊺⊻⊼⊽⊾⊿⋀⋁⋂⋃⋄⋅⋆⋇⋈⋉⋊⋋⋌⋍⋎⋏⋐⋑⋒⋓⋔⋕⋖⋗⋘⋙⋚⋛⋜⋝⋞⋟⋠⋡⋢⋣⋤⋥⋦⋧⋨⋩⋪⋫⋬⋭⋮⋯⋰⋱⋲⋳⋴⋵⋶⋷⋸⋹⋺⋻⋼⋽⋾⋿]

%%

"if"       { return IF; }
"else"     { return ELSE; }
"while"    { return WHILE; }
"for"      { return FOR; }
"do"       { return DO; }
"break"    { return BREAK; }
"continue" { return CONTINUE; }
"return"   { return RETURN; }
"int"      { return INT; }
"float"    { return FLOAT; }
"char"     { return CHAR; }
"void"     { return VOID; }
"true"     { return TRUE; }
"false"    { return FALSE; }
"and"      { return AND; }
"or"       { return OR; }
"not"      { return NOT; }
"print"    { return PRINT; }
"scan"     { return SCAN; }

"("        { return ABRE_PARENTESES; }
")"        { return FECHA_PARENTESES; }
"{"        { return ABRE_CHAVES; }
"}"        { return FECHA_CHAVES; }
";"        { return PONTO_VIRGULA; }
"="        { return '='; }
"+"        { return '+'; }
"-"        { return '-'; }
"*"        { return '*'; }
"/"        { return '/'; }

{DIGITO}+               { yylval.valor = atoi(yytext); return NUMERO; }
{DIGITO}+"."{DIGITO}+   { yylval.valor = atof(yytext); return NUMERO; }
{ID}                    { yylval.str = strdup(yytext); return PALAVRA; }
{SIMBOLO}               { yylval.str = strdup(yytext); return SIMBOLO; }
[ \t\n]                 ;  // Ignora espaços, tabs e novas linhas
.                       { printf("Caractere desconhecido: %s\n", yytext); }

%%

