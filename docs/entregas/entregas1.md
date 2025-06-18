# Interpretador de C em Python

Este projeto implementa um interpretador simplificado para um subconjunto da linguagem C, utilizando Python e a biblioteca [PLY (Python Lex-Yacc)](http://www.dabeaz.com/ply/).

Nesse primeiro momento implementamos toda a tabela de simbolos e palavras reservadas do C, além de já implementar os condicionais if e else. Começamo o while, contudo temos que refinar melhor esse laço.

---

## 📌 Visão Geral

- **Linguagem de entrada**: Subconjunto de C (inteiros, `if`, `return`)
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
python main.py testes.c

```

## 🧱 Arquitetura do Projeto

### 📦 Componentes Principais

| Arquivo          | Responsabilidade                                        |
|------------------|----------------------------------------------------------|
| `lexer.py`       | 🧪 Análise léxica — define tokens da linguagem C         |
| `parser.py`      | 🧠 Análise sintática — constrói a AST (Árvore Sintática Abstrata) |
| `interpreter.py` | ⚙️ Interpretador — executa a AST em tempo de execução    |
| `main.py`        | 🖥️ Orquestrador — coordena lexer, parser e interpretação |
| `testes.c`       | 🧾 Arquivo de exemplo com código C testável              |

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

No arquivo de testes.c
  
```bash
int main() {
    int x = 4;
    int y = 3;

    if ((2+6) > (x+y)) {
        return 1;
    }

    return 0;
}
```
### Espera-se a saída:

```bash
Tokens:
  INT: int
  ID: main
  ...
  RETURN: return
  NUMBER: 0

Abstract Syntax Tree:
└─ Program
  └─ Function: main (int)
    └─ Body
      └─ Declare: x (int)
        └─ Value
          └─ Num: 4
      └─ Declare: y (int)
        └─ Value
          └─ Num: 3
      └─ If
        └─ Condition
          └─ Op: >
            └─ Left
              └─ Op: +
                └─ Num: 2
                └─ Num: 6
            └─ Right
              └─ Op: +
                └─ Var: x
                └─ Var: y
        └─ Body
          └─ Return
            └─ Num: 1
      └─ Return
        └─ Num: 0

Resultado: 0
Variáveis finais: {'x': 4, 'y': 3}

```

---
# Tabela de Versionamento 

| Versão | Data       | Descrição                           | Autor(es) | Revisor(es) |
|--------|------------|-------------------------------------|-----------|-------------|
| 1.0    | 30/04/2025 | Desenvolvimento do tópico da entrega 1        | [Felipe das Neves](https://github.com/FelipeFreire-gf) | [Lucas Soares](https://github.com/lucaaassb) |