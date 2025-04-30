# Semana 4 - Prática: Implementação Inicial do Parser

## Conexão com o Cronograma e as Sprints

- **Cronograma:** foco em análise sintática (plano de ensino)
- **Projeto do compilador:**
  - Sprint anterior: fase léxica concluída ou avançada
  - Agora: fase sintática com Bison, aproveitando os tokens gerados

**Objetivo:** cada equipe deve produzir um parser inicial que reconheça construções básicas da linguagem escolhida.

---

## Passo a Passo (Exemplo em Flex + Bison)

### Definir Tokens no Arquivo `.y`

```yacc
%token NUM
%token PLUS MINUS TIMES DIVIDE
%token LPAREN RPAREN

%union {
    int intValue;
}

%type <intValue> NUM
```

- Definição do conjunto de tokens que serão usados no parser, coerentes com o scanner `.l`

---

## Arquivo Sintático (`parser.y`) - Parte 2

```c
%{
#include <stdio.h>
#include <stdlib.h>

int yylex(void);
void yyerror(const char *s);
%}

%union {
    int intValue;
}

%token <intValue> NUM
%type <intValue> expr
%token PLUS MINUS TIMES DIVIDE LPAREN RPAREN

%%

expr:
      expr PLUS expr    { $$ = $1 + $3; }
    | expr MINUS expr   { $$ = $1 - $3; }
    | expr TIMES expr   { $$ = $1 * $3; }
    | expr DIVIDE expr  { $$ = $1 / $3; }
    | LPAREN expr RPAREN{ $$ = $2; }
    | NUM               { $$ = $1; }
    ;

%%

int main(void) { return yyparse(); }
void yyerror(const char *s) { fprintf(stderr, "Erro sintático: %s\n", s); }
```

---

## Arquivo Léxico (`scanner.l`) - Parte 3

```c
%{
#include <stdio.h>
#include <stdlib.h>
#include "parser.tab.h"
%}

%%

[0-9]+  { yylval.intValue = atoi(yytext); return NUM; }
"+"     { return PLUS; }
"-"     { return MINUS; }
"*"     { return TIMES; }
"/"     { return DIVIDE; }
"("     { return LPAREN; }
")"     { return RPAREN; }
[ \t\n]+ { /* ignorar espaços */ }
.       { printf("Caractere não reconhecido: %s\n", yytext); }

%%

int yywrap(void) { return 1; }
```

---

## Compilação e Execução - Parte 4

```bash
# Gerar arquivos Bison
bison -d parser.y

# Gerar arquivo Flex
flex scanner.l

# Compilar tudo
gcc -o parser parser.tab.c lex.yy.c -lfl

# Executar
./parser
```

- Digite uma expressão, como `3+4*2`
- Se estiver correto, não aparece erro; caso contrário, verifique mensagens

---

# Tabela de Versionamento 

| Versão | Data       | Descrição                           | Autor(es) | Revisor(es) |
|--------|------------|-------------------------------------|-----------|-------------|
| 1.0    | 28/04/2025 | Criação da atividade de desenvolvimento 4        | [Júlio Cesar](https://github.com/Julio1099) | [Felipe das Neves](https://github.com/FelipeFreire-gf) |

