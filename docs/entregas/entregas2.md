# Interpretador de C em Python

Este projeto implementa um interpretador simplificado para um subconjunto da linguagem C, utilizando Python e a biblioteca [PLY (Python Lex-Yacc)](http://www.dabeaz.com/ply/).

Nesse primeiro momento implementamos toda a tabela de simbolos e palavras reservadas do C, além de já implementar os condicionais if e else. Começamo o while, contudo temos que refinar melhor esse laço.

---

## 📌 Visão Geral

- **Linguagem de entrada**: Subconjunto de C (inteiros, `if`, `else`, `while`, `for`, `return`)
- **Tecnologias**: Python + PLY
- **Etapas**: Análise léxica → Sintática (AST) → Interpretação
- **Objetivo**: Didático — compreender como funciona um compilador simples

---

## ⚙️ Instalação

### Pré-requisitos

- Python 3.8+
- PLY

### Instale as dependências

```bash
pip install -r requirements.txt

```

### Para executar, faça:

```bash
python main.py testes2.c

```

## 🧱 Arquitetura do Projeto

### 📦 Componentes Principais

| Arquivo          | Responsabilidade                                        |
|------------------|----------------------------------------------------------|
| `lexer.py`       | 🧪 Análise léxica — define tokens da linguagem C         |
| `parser.py`      | 🧠 Análise sintática — constrói a AST (Árvore Sintática Abstrata) |
| `interpreter.py` | ⚙️ Interpretador — executa a AST em tempo de execução    |
| `main.py`        | 🖥️ Orquestrador — coordena lexer, parser e interpretação |
| `testes2.c`       | 🧾 Arquivo de exemplo com código C testável              |

---

### 🔁 Fluxo de Execução

```mermaid
flowchart TD
    A[📄 Código-fonte (.c)] --> B[🔍 Lexer<br/>(Tokenização)]
    B --> C[🧩 Parser<br/>(Geração de AST)]
    C --> D[🧮 Interpretador<br/>(Execução da AST)]
    D --> E[📤 Resultado Final]
```

## 📂 Exemplo Completo

No arquivo de testes_arrays.c
  
```bash
int main() {
    int x[3];
    x[0] = 1;
    x[1] = 2;
    x[2] = x[0] + x[1];
    return x[2];
}
```
### Espera-se a saída:

```bash
=== Analyzing testes.c ===

=== TOKENIZATION ===
Line 1: INT             = int
Line 1: ID              = main
Line 1: LPAREN          = (
Line 1: RPAREN          = )
Line 1: LBRACE          = {
Line 2: INT             = int
Line 2: ID              = x
Line 2: LBRACKET        = [
Line 2: NUMBER          = 3
Line 2: RBRACKET        = ]
Line 2: SEMI            = ;
Line 3: ID              = x
Line 3: LBRACKET        = [
Line 3: NUMBER          = 0
Line 3: RBRACKET        = ]
Line 3: ASSIGN          = =
Line 3: NUMBER          = 1
Line 3: SEMI            = ;
Line 4: ID              = x
Line 4: LBRACKET        = [
Line 4: NUMBER          = 1
Line 4: RBRACKET        = ]
Line 4: ASSIGN          = =
Line 4: NUMBER          = 2
Line 4: SEMI            = ;
Line 5: ID              = x
Line 5: LBRACKET        = [
Line 5: NUMBER          = 2
Line 5: RBRACKET        = ]
Line 5: ASSIGN          = =
Line 5: ID              = x
Line 5: LBRACKET        = [
Line 5: NUMBER          = 0
Line 5: RBRACKET        = ]
Line 5: PLUS            = +
Line 5: ID              = x
Line 5: LBRACKET        = [
Line 5: NUMBER          = 1
Line 5: RBRACKET        = ]
Line 5: SEMI            = ;
Line 6: RETURN          = return
Line 6: ID              = x
Line 6: LBRACKET        = [
Line 6: NUMBER          = 2
Line 6: RBRACKET        = ]
Line 6: SEMI            = ;
Line 7: RBRACE          = }

Total tokens: 47

=== SYNTAX TREE ===
└─ Program
  └─ Function: main (returns ('type', 'int', 0))
    └─ Body
      └─ Array Declare: x (int)[3]
      └─ Array Assign: x[0]
        └─ Value
          └─ Num: 1
      └─ Array Assign: x[1]
        └─ Value
          └─ Num: 2
      └─ Array Assign: x[2]
        └─ Value
          └─ Binop: +
            └─ Left
              └─ Array Access: x[0]
            └─ Right
              └─ Array Access: x[1]
      └─ Return
        └─ Value
          └─ Array Access: x[2]


=== EXECUTION ===
Variáveis locais: {'x': {'type': 'array', 'size': 3}}

Variáveis locais da função main: {}

=== FINAL STATE ===
Return value: 3

Global variables:

Arrays:
  x: [1, 2, 3]

Memory used: -3096 bytes
```

---
# Tabela de Versionamento 

| Versão | Data       | Descrição                           | Autor(es) | Revisor(es) |
|--------|------------|-------------------------------------|-----------|-------------|
| 1.0    | 18/06/2025 | Desenvolvimento do tópico da entrega 2        | [Felipe das Neves](https://github.com/FelipeFreire-gf) | [Lucas Soares](https://github.com/lucaaassb) |