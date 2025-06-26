# Interpretador de C em Python

> Este documento detalha a implementação de um interpretador para um subconjunto da linguagem C, desenvolvido em Python. Abordaremos a estrutura do projeto, desde a análise sintática do código-fonte até a sua execução, explicando as técnicas utilizadas para implementar cada funcionalidade da linguagem.


---

## Estrutura do Interpretador

O interpretador funciona em duas fases principais:

1. **Análise Sintática (`parser.py`)**: O código C de entrada é lido e transformado em uma estrutura de dados em árvore, conhecida como Árvore Sintática Abstrata (AST). Essa árvore representa a estrutura hierárquica do programa.
2. **Execução (`interpreter.py`)**: Um componente, o "interpretador", percorre a AST gerada na fase anterior e executa as instruções nó por nó, simulando o comportamento do programa C.

### 1. Análise Sintática (parser.py)

O `parser.py` é responsável por definir a gramática da nossa linguagem C. Ele utiliza a biblioteca `ply.yacc` para construir a AST. Cada função `p_...` define uma regra da gramática que reconhece uma parte da linguagem (como uma declaração de variável, um `if`, etc.) e especifica qual nó da AST deve ser criado.

A AST é composta por tuplas, onde o primeiro elemento é uma string que identifica o tipo do nó (ex: `'var_decl'`, `'if'`, `'bin_op'`) e os elementos seguintes são seus filhos (outros nós ou valores).

### 2. Execução (interpreter.py)

O `interpreter.py` contém a classe `Interpreter`, que é o cérebro do projeto. Ela utiliza o padrão de projeto *Visitor* para percorrer a AST. Para cada tipo de nó definido no parser (ex: `'var_decl'`), existe um método correspondente na classe `Interpreter` (ex: `visit_var_decl`).

O interpretador mantém uma **Tabela de Símbolos** (`self.symbol_table`), que é um dicionário Python usado para armazenar as variáveis e seus valores durante a execução do programa.

---

## Funcionalidades da Linguagem

A seguir, detalhamos como cada construção da linguagem C é tratada pelo parser e pelo interpretador.

### Tipos e Declaração de Variáveis (`int`)

O nosso interpretador suporta apenas o tipo de dado `int`.

* **Parser**:

```python
# parser.py
def p_declaration(p):
    '''declaration : type_specifier ID SEMI
                   | type_specifier ID ASSIGN expression SEMI'''
    if len(p) == 4:
        p[0] = ('var_decl', p[1], p[2], None) # ex: int x;
    else:
        p[0] = ('var_decl', p[1], p[2], p[4]) # ex: int x = 10;
```

* **Interpretador**:

```python
# interpreter.py
def visit_var_decl(self, node):
    _type, var_name, value_node = node[1:]
    if value_node:
        value = self.visit(value_node)
    else:
        value = 0  # Default value for int
    self.symbol_table[var_name] = value
```

### Atribuição

Permite alterar o valor de uma variável já declarada.

* **Parser**:

```python
# parser.py
def p_assignment(p):
    'assignment : ID ASSIGN expression SEMI'
    p[0] = ('assign', p[1], p[3])
```

* **Interpretador**:

```python
# interpreter.py
def visit_assign(self, node):
    var_name, value_node = node[1:]
    if var_name not in self.symbol_table:
        raise NameError(f"Variable '{var_name}' not declared.")
    value = self.visit(value_node)
    self.symbol_table[var_name] = value
```

### Operadores (Aritméticos, Comparação e Lógicos)

O interpretador suporta operações matemáticas, de comparação e lógicas.

* **Parser**:

```python
# parser.py
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression EQ expression
                  | expression NEQ expression
                  | expression LT expression
                  | expression GT expression
                  | expression AND expression
                  | expression OR expression'''
    p[0] = ('bin_op', p[2], p[1], p[3])
```

* **Interpretador**:

```python
# interpreter.py
def visit_bin_op(self, node):
    _op, left_node, right_node = node[1:]
    left_val = self.visit(left_node)
    right_val = self.visit(right_node)

    if _op == '+': return left_val + right_val
    elif _op == '-': return left_val - right_val
    elif _op == '*': return left_val * right_val
    elif _op == '/': return left_val // right_val
    elif _op == '==': return 1 if left_val == right_val else 0
    elif _op == '!=': return 1 if left_val != right_val else 0
    elif _op == '<': return 1 if left_val < right_val else 0
    elif _op == '>': return 1 if left_val > right_val else 0
    elif _op == '&&': return 1 if left_val != 0 and right_val != 0 else 0
    elif _op == '||': return 1 if left_val != 0 or right_val != 0 else 0
```

### Estruturas de Controle (`if`, `else`, `while`)

* **`if-else`**:

```python
# parser.py
def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN statement
                    | IF LPAREN expression RPAREN statement ELSE statement'''
    if len(p) == 6:
        p[0] = ('if', p[3], p[5], None)
    else:
        p[0] = ('if', p[3], p[5], p[7])
```

```python
# interpreter.py
def visit_if(self, node):
    condition, true_block, false_block = node[1:]
    if self.visit(condition) != 0:
        self.visit(true_block)
    elif false_block:
        self.visit(false_block)
```

* **`while`**:

```python
# parser.py
def p_while_statement(p):
    'while_statement : WHILE LPAREN expression RPAREN statement'
    p[0] = ('while', p[3], p[5])
```

```python
# interpreter.py
def visit_while(self, node):
    condition, body = node[1:]
    while self.visit(condition) != 0:
        self.visit(body)
```

### Saída (`print`)

* **Parser**:

```python
# parser.py
def p_print_statement(p):
    'print_statement : PRINT LPAREN expression RPAREN SEMI'
    p[0] = ('print', p[3])
```

* **Interpretador**:

```python
# interpreter.py
def visit_print(self, node):
    value = self.visit(node[1])
    print(value)
```

### Arrays

* **Declaração**:

```python
# parser.py
def p_array_declaration(p):
    'array_declaration : type_specifier ID LBRACKET NUMBER RBRACKET SEMI'
    p[0] = ('array_decl', p[2], p[4])
```

```python
# interpreter.py
def visit_array_decl(self, node):
    var_name, size = node[1:]
    self.symbol_table[var_name] = [0] * size
```

* **Acesso e Atribuição**:

```python
# parser.py
def p_expression_array_access(p):
    'expression : ID LBRACKET expression RBRACKET'
    p[0] = ('array_access', p[1], p[3])

def p_assignment_array(p):
    'assignment : ID LBRACKET expression RBRACKET ASSIGN expression SEMI'
    p[0] = ('array_assign', p[1], p[3], p[6])
```

```python
# interpreter.py
def visit_array_access(self, node):
    var_name, index_node = node[1:]
    index = self.visit(index_node)
    return self.symbol_table[var_name][index]

def visit_array_assign(self, node):
    var_name, index_node, value_node = node[1:]
    index = self.visit(index_node)
    value = self.visit(value_node)
    self.symbol_table[var_name][index] = value
```

### Retorno de Função (`return`)

```python
# parser.py
def p_return_statement(p):
    'return_statement : RETURN expression SEMI'
    p[0] = ('return', p[2])
```

```python
# interpreter.py
class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value

def visit_return(self, node):
    value_node = node[1]
    raise ReturnValue(self.visit(value_node))

def interpret(self, ast):
    try:
        self.visit(ast)
    except ReturnValue as e:
        return e.value # Retorna o valor capturado
    return 0 # Código de saída padrão se não houver return
```

---

## Tabela de Versionamento

| Versão | Data       | Descrição                                | Autor(es)                                              | Revisor(es)                                  |
| ------ | ---------- | ---------------------------------------- | ------------------------------------------------------ | -------------------------------------------- |
| 1.0    | 26/06/2025 | Desenvolvimento do artefato para docuementação | [Felipe das Neves](https://github.com/FelipeFreire-gf) | [Lucas Soares](https://github.com/lucaaassb) |