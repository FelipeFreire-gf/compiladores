import ply.yacc as yacc
from lexer import tokens

# Função
def p_function_definition(p):
    'function : type ID LPAREN param_list RPAREN compound_stmt'
    p[0] = ('function', p[1], p[2], p[4], p[6])

# Bloco de comandos
def p_compound_stmt(p):
    'compound_stmt : LBRACE stmt_list RBRACE'
    p[0] = ('block', p[2])

def p_stmt_list(p):
    '''stmt_list : stmt
                 | stmt_list stmt'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

# Comandos
def p_stmt(p):
    '''stmt : return_stmt
            | while_stmt
            | expr_stmt
            | compound_stmt
            | SEMI
            | IF LPAREN expression RPAREN stmt
            | IF LPAREN expression RPAREN stmt ELSE stmt'''
    if len(p) == 2 and p[1] == ';':
        p[0] = ('null_stmt',)
    elif len(p) == 6:
        p[0] = ('if', p[3], p[5])
    elif len(p) == 8:
        p[0] = ('if_else', p[3], p[5], p[7])
    else:
        p[0] = p[1]


def p_return_stmt(p):
    'return_stmt : RETURN expression SEMI'
    p[0] = ('return', p[2])

def p_while_stmt(p):
    'while_stmt : WHILE LPAREN expression RPAREN compound_stmt'
    p[0] = ('while', p[3], p[5])

def p_expr_stmt(p):
    'expr_stmt : expression SEMI'
    p[0] = ('expr', p[1])

# Expressões
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression GT expression
                  | expression LT expression
                  | expression GE expression
                  | expression LE expression
                  | expression EQ expression
                  | expression NE expression'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = ('num', p[1])

def p_expression_id(p):
    'expression : ID'
    p[0] = ('id', p[1])

def p_expression_assign(p):
    'expression : ID ASSIGN expression'
    p[0] = ('assign', p[1], p[3])

# Parâmetros
def p_param_list(p):
    '''param_list : param
                  | param_list COMMA param
                  | empty'''
    if len(p) == 2 and p[1] is not None:
        p[0] = [p[1]]
    elif len(p) == 2:
        p[0] = []
    else:
        p[0] = p[1] + [p[3]]

def p_param(p):
    '''param : type ID
             | type TIMES ID'''
    if len(p) == 3:
        p[0] = ('param', p[1], p[2])
    else:
        p[0] = ('param_ptr', p[1], p[3])

def p_type(p):
    '''type : INT
            | FLOAT
            | DOUBLE
            | CHAR
            | VOID'''
    p[0] = p[1]

def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    if p:
        print(f"Erro de sintaxe em '{p.value}'")
    else:
        print("Erro de sintaxe no final do input")

parser = yacc.yacc()
