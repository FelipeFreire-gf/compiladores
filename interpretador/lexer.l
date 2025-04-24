%{
#include "parser.tab.h"  // Cabeçalho gerado pelo Bison
%}

DIGITO    [0-9]
LETRA     [a-zA-Z]
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

{DIGITO}+               { yylval.str = strdup(yytext); return NUMERO; }
{DIGITO}+"."{DIGITO}+   { yylval.str = strdup(yytext); return NUMERO; }
{LETRA}+                { yylval.str = strdup(yytext); return PALAVRA; }
{SIMBOLO}+             { yylval.str = strdup(yytext); return SIMBOLO; }
[ \t\n]                 ;  // Ignora espaços, tabs e novas linhas
.                       { printf("Caractere desconhecido: %s\n", yytext); }

%%

