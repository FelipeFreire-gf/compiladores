# Interpretador de C em Python

Nesta Etapa focamos na resolução dos problemas da entrega 1.

---

## 📌 Visão Geral

- **Linguagem de entrada**: Subconjunto de C (inteiros, `if`, `else`, `while`, `for`, `return`)
- **Tecnologias**: Python + PLY

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

Obs.: vc pode colocar o código utilizado para teste da equipe, localizado na pasta Testes dentro de interpretadorPython.

## 🧱 Arquitetura do Projeto

### 📦 Componentes Principais

| Arquivo          | Responsabilidade                                        |
|------------------|----------------------------------------------------------|
| `lexer.py`       | 🧪 Análise léxica — define tokens da linguagem C         |
| `parser.py`      | 🧠 Análise sintática — constrói a AST (Árvore Sintática Abstrata) |
| `interpreter.py` | ⚙️ Interpretador — executa a AST em tempo de execução    |
| `main.py`        | 🖥️ Orquestrador — coordena lexer, parser e interpretação |
| `testes.c`       | 🧾 Arquivo de exemplo com código C testável (na pasta `interpretadorPython`) |
| `Testes/`        | 📂 Diretório contendo arquivos `.c` para testes específicos (na pasta `interpretadorPython`) |

---

### 🔁 Fluxo de Execução

```mermaid
flowchart TDEsta alteração no diagrama:
-   Inicia com o "Código-fonte (.c)".
-   Mostra explicitamente o `main.py` como o primeiro receptor e orquestrador (🖥️).
-   Em seguida, detalha o fluxo através dos componentes `lexer.py` (🧪), `parser.py` (🧠), e `interpreter.py` (⚙️), usando os mesmos ícones e nomenclaturas da sua tabela de componentes.
-   Conclui com o "Resultado Final" (📤).

    Input[📄 Código-fonte (.c)] --> Main[🖥️ main.py]
    Main --> Lexer[🧪 lexer.py<br/>(Análise Léxica/Tokenização)]
    Lexer --> Parser[🧠 parser.py<br/>(Análise Sintática/Geração de AST)]
    Parser --> Interpreter[⚙️ interpreter.py<br/>(Interpretação/Execução da AST)]
    Interpreter --> Output[📤 Resultado Final]
```

## 📂 Exemplo Completo

No arquivo de testes.c com o código de teste de array:
  
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