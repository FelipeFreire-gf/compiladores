# Semana 5 - Prática: Continuação do Parser e Tratamento de Erros Sintáticos

## Objetivos da Aula

1. Revisar o estado atual do parser (Bison) após a aula anterior.
2. Introduzir métodos de tratamento de erros sintáticos (mensagens claras, recuperação).
3. Demonstrar um exemplo de parser com tratamento de erros.
4. Orientar a adaptação do exemplo para os projetos das equipes.
5. Alinhar atividades com as sprints do projeto de compilador.

---

## Conexão com as Sprints

- **Sprint anterior:** Início da implementação do parser básico.
- **Sprint atual:**
  - Aperfeiçoar o parser, incluindo tratamento de erros.
  - Reforçar testes de parsing.
  - Incluir "testes de erros sintáticos" e "melhorias de mensageria" no backlog.

---

## Conceito: Tratamento de Erros Sintáticos

1. **Detecção de erro:** Identificar tokens fora da ordem esperada.
2. **Recuperação de erro:** Retomar análise usando estratégias como panic mode e phrase-level.
3. **Mensagem ao usuário:** Indicar causa e possível posição do erro (linha, token, etc.).

---

## Exemplo de Parser com Tratamento de Erro (Bison)

### Arquivo `parser.y`

```c
%{
#include <stdio.h>
#include <stdlib.h>

int yylex(void);
void yyerror(const char *s);
%}

%union { int intValue; }

%token <intValue> NUM
%token PLUS MINUS TIMES DIVIDE LPAREN RPAREN SEMI
%type <intValue> expr

%left PLUS MINUS
%left TIMES DIVIDE

%start input

%%

input:
      /* vazio */
    | input expr SEMICOLON      { printf("Resultado: %d\n", $2); }
    | input error SEMICOLON     { 
          fprintf(stderr, "[ERRO SINTATICO] Erro recuperado até ';'\n");
          yyerrok;
          yyclearin;
      }
    ;

expr:
      expr PLUS expr    { $$ = $1 + $3; }
    | expr MINUS expr   { $$ = $1 - $3; }
    | expr TIMES expr   { $$ = $1 * $3; }
    | expr DIVIDE expr  { $$ = ($3 == 0) ? (fprintf(stderr, "[ERRO SEMANTICO] Divisao por zero!\n"), 0) : ($1 / $3); }
    | LPAREN expr RPAREN{ $$ = $2; }
    | NUM               { $$ = $1; }
    ;

%%
```

---

## Arquivo Léxico (`scanner.l`) de Exemplo

```c
%{
#include <stdio.h>
#include <stdlib.h>
#include "parser.tab.h"
%}

%%

[0-9]+     { yylval.intValue = atoi(yytext); return NUM; }
"+"        { return PLUS; }
"-"        { return MINUS; }
"*"        { return TIMES; }
"/"        { return DIVIDE; }
"("        { return LPAREN; }
")"        { return RPAREN; }
";"        { return SEMICOLON; }
[ \t\n]+   { /* ignorar */ }
.          { printf("Caractere não reconhecido: %s\n", yytext); }

%%

int yywrap(void) { return 1; }
```

---

## Tarefa para a Aula Prática

1. Baixar/clonar o exemplo base ou criar a partir dos slides.
2. Compilar usando `make`.
3. Testar:
   - Expressões válidas: `3+4;`
   - Erros sintáticos: `(3++2;`, `3+4))`
4. Adaptar o projeto:
   - Substituir ou complementar regras gramaticais.
   - Escolher abordagem de recuperação (panic mode, phrase-level).
   - Documentar as mudanças no repositório.
5. Planejar:
   - Incluir "tratamento de erros" no backlog.
   - Discutir mensagens mais claras sobre erros.

---

## Alinhamento com a Disciplina

- **Cronograma:** Aula prática 5, após implementação inicial do parser.
- **Objetivo:** Tornar o compilador mais robusto.
- **Próximos passos:**
  - Estrutura de dados para AST
  - Tabela de símbolos
  - Preparação para P1

---

## Conclusões e Recomendações

1. Tratamento de erros melhora a experiência do usuário e facilita a depuração.
2. Usar Bison: `error`, `yyerrok`, `yyclearin`.
3. Documentar claramente:
   - Quais erros podem ser tratados.
   - Comportamento do parser ao encontrar erros.
4. Avançar com a prática em aula.
5. Integrar com as sprints, mantendo backlog e commits atualizados.

---

# Tabela de Versionamento 

| Versão | Data       | Descrição                           | Autor(es) | Revisor(es) |
|--------|------------|-------------------------------------|-----------|-------------|
| 1.0    | 28/04/2025 | Criação da atividade de desenvolvimento 5        | [Júlio Cesar](https://github.com/Julio1099) | [Felipe das Neves](https://github.com/FelipeFreire-gf) |

