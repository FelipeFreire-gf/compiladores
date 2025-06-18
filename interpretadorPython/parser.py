import ply.yacc as yacc
from lexer import tokens # Importa os tokens definidos no lexer


# Define a precedência dos operadores 
# Diz quem vem antes em expressões
# Cada linha tem mais prioridade que a de cima
precedence = (
    ('right', 'NOT', 'ADDRESS'),        # Operadores ! e & (ex: !a, &x)
    ('left', 'AND', 'OR'),              # && e ||
    ('left', 'LT', 'LE', 'GT', 'GE', 'EQ', 'NE'),  # <, <=, >, >=, ==, !=
    ('left', 'PLUS', 'MINUS'),          # + e -
    ('left', 'TIMES', 'DIVIDE', 'MOD'), # *, /, %
)

# Regras da linguagem começam aqui
# def p_nome_da_regra(p):
#    '''regra : alternativa1
#             | alternativa2'''
#    # ação semântica
#    p[0] = ...

# programa completo → lista de elementos (funções, declarações, etc.)
def p_program(p):
    '''program : element_list'''
    # Exemplo: int main() { return 0; }
    p[0] = ('program', p[1])

# lista de elementos: um ou vários
def p_element_list(p):
    '''element_list : element
                   | element_list element'''
    # Exemplo: várias funções ou declarações seguidas
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

# Um elemento pode ser uma função, declaração ou include
def p_element(p):
    '''element : function
              | declaration
              | include'''
    p[0] = p[1]

# Include (ex: #include <stdio.h>)
def p_include(p):
    '''include : INCLUDE'''
    p[0] = ('include', p[1])



# Função com ou sem parâmetros
def p_function(p):
    '''function : type ID LPAREN RPAREN compound_statement
               | type ID LPAREN parameter_list RPAREN compound_statement'''
    # Exemplo sem parâmetros: int main() { return 0; }
    # Exemplo com parâmetros: int soma(int a, int b) { return a + b; }
    if len(p) == 6:
        p[0] = ('function', p[1], p[2], [], p[5])
    else:
        p[0] = ('function', p[1], p[2], p[4], p[6])

# Lista de parâmetros da função
def p_parameter_list(p):
    '''parameter_list : parameter
                     | parameter_list COMMA parameter'''
    # Ex: int a, int b
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

# Parâmetro individual: pode ser variável ou array
def p_parameter(p):
    '''parameter : type ID
                | type ID LBRACKET RBRACKET'''
    # Ex: int x      → variável simples
    #     int vet[]  → array
    if len(p) == 3:
        p[0] = (p[1], p[2], False)
    else:
        p[0] = (p[1], p[2], True)

# Tipo base: int ou void
def p_base_type(p):
    '''base_type : INT
                | VOID'''
    p[0] = p[1]

# Tipo com ponteiro (ex: int*, int**, etc.)
def p_type(p):
    '''type : base_type
            | type TIMES'''
    # Ex: int        → ('type', 'int', 0)
    #     int*       → ('type', 'int', 1)
    #     int**      → ('type', 'int', 2)
    if len(p) == 2:
        p[0] = ('type', p[1], 0)
    else:
        p[0] = ('type', p[1][1], p[1][2] + 1)



# Operações com ponteiros: *p, &x
def p_pointer_expr(p):
    '''pointer_expr : ADDRESS id
                   | TIMES id
                   | TIMES pointer_expr'''
    # &x → endereço de x
    # *p → conteúdo do ponteiro p
    p[0] = ('pointer_op', p[1], p[2])


# Bloco de comandos: { ... }
def p_compound_statement(p):
    '''compound_statement : LBRACE statement_list RBRACE
                         | LBRACE RBRACE'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = []

# Lista de comandos
def p_statement_list(p):
    '''statement_list : statement
                     | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

# Tipos de comandos aceitos
def p_statement(p):
    '''statement : declaration
                | assignment
                | if_statement
                | while_statement
                | return_statement
                | expression SEMI
                | compound_statement'''
    # Expressão sozinha com ;
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('expression_stmt', p[1])

# Declaração de ponteiro com ou sem valor
def p_pointer_declaration(p):
    '''declaration : type TIMES ID SEMI
                   | type TIMES ID ASSIGN expression SEMI'''
    # int *p;
    # int *p = &x;
    if len(p) == 5:
        p[0] = ('pointer_decl', p[1], p[3], None)
    else:
        p[0] = ('pointer_decl', p[1], p[3], p[5])

# Atribuição usando ponteiro (ex: *p = 5;)
def p_pointer_assignment(p):
    '''statement : TIMES ID ASSIGN expression SEMI'''
    p[0] = ('pointer_assignment', p[2], p[4])

# Declaração de variáveis, arrays ou arrays com valores
def p_declaration(p):
    '''declaration : type ID SEMI
                  | type ID LBRACKET NUMBER RBRACKET SEMI
                  | type ID ASSIGN expression SEMI
                  | type ID LBRACKET NUMBER RBRACKET ASSIGN LBRACE array_init RBRACE SEMI'''
    # int x;
    # int x = 5;
    # int vet[3];
    # int vet[3] = {1, 2, 3};
    if len(p) == 4:
        p[0] = ('declaration', p[1], p[2], None)
    elif len(p) == 7 and p[3] == '[':
        p[0] = ('array_declaration', p[1], p[2], p[4])
    elif len(p) == 6:
        p[0] = ('declaration', p[1], p[2], p[4])
    else:
        p[0] = ('array_declaration_init', p[1], p[2], p[4], p[8])

# Lista de valores para arrays
def p_array_init(p):
    '''array_init : expression
                 | array_init COMMA expression'''
    # {1, 2, 3}
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


# Três tipos de atribuição:
# 1. x = 5;
# 2. vet[2] = 10;
# 3. (*p) = x;
def p_assignment(p):
    '''assignment : ID ASSIGN expression SEMI
                  | ID LBRACKET expression RBRACKET ASSIGN expression SEMI
                  | expression ASSIGN expression SEMI'''
    if len(p) == 5 and isinstance(p[1], tuple):
        p[0] = ('assignment_expr', p[1], p[3])
    elif len(p) == 5:
        p[0] = ('assignment', p[1], p[3])
    else:
        p[0] = ('array_assignment', p[1], p[3], p[6])

# if (condição) { ... } else { ... }
def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN compound_statement
                   | IF LPAREN expression RPAREN compound_statement ELSE compound_statement
                   | IF LPAREN expression RPAREN compound_statement ELSE if_statement'''
    if len(p) == 6:
        p[0] = ('if', p[3], p[5], None)
    elif len(p) == 8:
        p[0] = ('if', p[3], p[5], p[7])

# while (condição) { ... }
def p_while_statement(p):
    'while_statement : WHILE LPAREN expression RPAREN compound_statement'
    p[0] = ('while', p[3], p[5])

# return valor;
def p_return_statement(p):
    '''return_statement : RETURN expression SEMI
                       | RETURN SEMI'''
    if len(p) == 4:
        p[0] = ('return', p[2])
    else:
        p[0] = ('return', None)

# Expressão pode ser: número, string, chamada de função, operação, etc.
def p_expression(p):
    '''expression : number
                 | boolean
                 | string
                 | id
                 | binop_expr
                 | logical_expr
                 | not_expr
                 | group_expr
                 | function_call
                 | array_access
                 | pointer_expr'''
    p[0] = p[1]

# "texto"
def p_string(p):
    'string : STRING'
    p[0] = ('string', p[1])

# vet[2]
def p_array_access(p):
    'array_access : ID LBRACKET expression RBRACKET'
    p[0] = ('array_access', p[1], p[3])

# chamada de função ou input/print
def p_function_call(p):
    '''function_call : ID LPAREN RPAREN
                    | ID LPAREN argument_list RPAREN
                    | PRINT LPAREN argument_list RPAREN
                    | INPUT LPAREN RPAREN'''
    if len(p) == 4:
        if p[1] == 'input':
            p[0] = ('input',)
        else:
            p[0] = ('function_call', p[1], [])
    elif len(p) == 5:
        if p[1] == 'print':
            p[0] = ('print', p[3])
        else:
            p[0] = ('function_call', p[1], p[3])
    else:
        p[0] = ('input',)

# lista de argumentos (ex: print(a, b + 1))
def p_argument_list(p):
    '''argument_list : expression
                    | argument_list COMMA expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

# !x
def p_not_expr(p):
    'not_expr : NOT expression'
    p[0] = ('not', p[2])

# x && y, x || y
def p_logical_expr(p):
    '''logical_expr : expression AND expression
                   | expression OR expression'''
    p[0] = ('logical', p[2], p[1], p[3])

# x + y, x < y, etc.
def p_binop_expr(p):
    '''binop_expr : expression PLUS expression
                 | expression MINUS expression
                 | expression TIMES expression
                 | expression DIVIDE expression
                 | expression MOD expression
                 | expression LT expression
                 | expression LE expression
                 | expression GT expression
                 | expression GE expression
                 | expression EQ expression
                 | expression NE expression'''
    p[0] = ('binop', p[2], p[1], p[3])

# (x + y)
def p_group_expr(p):
    'group_expr : LPAREN expression RPAREN'
    p[0] = p[2]

# true ou false
def p_boolean(p):
    '''boolean : TRUE
              | FALSE'''
    p[0] = ('bool', p[1].lower() == 'true')

# Número literal
def p_number(p):
    'number : NUMBER'
    p[0] = ('number', p[1])

# Nome de variável, função, etc.
def p_id(p):
    'id : ID'
    p[0] = ('id', p[1])

# Caso de erro de sintaxe
def p_error(p):
    if p:
        print(f"Erro de sintaxe em '{p.value}' na linha {p.lineno}")
    else:
        print("Erro de sintaxe no final do arquivo")

# Cria o parser
parser = yacc.yacc()