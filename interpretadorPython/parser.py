import ply.yacc as yacc
from lexer import tokens

precedence = (
    ('right', 'NOT'),
    ('left', 'AND', 'OR'),
    ('left', 'LT', 'LE', 'GT', 'GE', 'EQ', 'NE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

def p_program(p):
    '''program : element_list'''
    p[0] = ('program', p[1])

def p_element_list(p):
    '''element_list : element
                   | element_list element'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_element(p):
    '''element : function
              | declaration'''
    p[0] = p[1]

def p_function(p):
    '''function : type ID LPAREN RPAREN compound_statement
               | type ID LPAREN parameter_list RPAREN compound_statement'''
    if len(p) == 6:
        p[0] = ('function', p[1], p[2], [], p[5])
    else:
        p[0] = ('function', p[1], p[2], p[4], p[6])

def p_parameter_list(p):
    '''parameter_list : parameter
                     | parameter_list COMMA parameter'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_parameter(p):
    '''parameter : type ID
                | type ID LBRACKET RBRACKET'''
    if len(p) == 3:
        p[0] = (p[1], p[2], False)
    else:
        p[0] = (p[1], p[2], True)

def p_type(p):
    '''type : INT
            | VOID'''
    p[0] = p[1]

def p_compound_statement(p):
    '''compound_statement : LBRACE statement_list RBRACE
                         | LBRACE RBRACE'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = []

def p_statement_list(p):
    '''statement_list : statement
                     | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : declaration
                | assignment
                | if_statement
                | while_statement
                | return_statement
                | expression SEMI
                | compound_statement'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('expression_stmt', p[1])

def p_declaration(p):
    '''declaration : type ID SEMI
                  | type ID LBRACKET NUMBER RBRACKET SEMI
                  | type ID ASSIGN expression SEMI
                  | type ID LBRACKET NUMBER RBRACKET ASSIGN LBRACE array_init RBRACE SEMI'''
    if len(p) == 4:
        p[0] = ('declaration', p[1], p[2], None)
    elif len(p) == 7 and p[3] == '[':
        p[0] = ('array_declaration', p[1], p[2], p[4])
    elif len(p) == 6:
        p[0] = ('declaration', p[1], p[2], p[4])
    else:
        p[0] = ('array_declaration_init', p[1], p[2], p[4], p[8])

def p_array_init(p):
    '''array_init : expression
                 | array_init COMMA expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_assignment(p):
    '''assignment : ID ASSIGN expression SEMI
                 | ID LBRACKET expression RBRACKET ASSIGN expression SEMI'''
    if len(p) == 5:
        p[0] = ('assignment', p[1], p[3])
    else:
        p[0] = ('array_assignment', p[1], p[3], p[6])

def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN compound_statement
                   | IF LPAREN expression RPAREN compound_statement ELSE compound_statement
                   | IF LPAREN expression RPAREN compound_statement ELSE if_statement'''
    if len(p) == 6:
        p[0] = ('if', p[3], p[5], None)
    elif len(p) == 8:
        p[0] = ('if', p[3], p[5], p[7])
    else:
        p[0] = ('if', p[3], p[5], p[7])

def p_while_statement(p):
    'while_statement : WHILE LPAREN expression RPAREN compound_statement'
    p[0] = ('while', p[3], p[5])

def p_return_statement(p):
    'return_statement : RETURN expression SEMI'
    p[0] = ('return', p[2])

def p_expression(p):
    '''expression : number
                 | boolean
                 | id
                 | binop_expr
                 | logical_expr
                 | not_expr
                 | group_expr
                 | function_call
                 | array_access'''
    p[0] = p[1]

def p_array_access(p):
    'array_access : ID LBRACKET expression RBRACKET'
    p[0] = ('array_access', p[1], p[3])

def p_function_call(p):
    '''function_call : ID LPAREN RPAREN
                    | ID LPAREN argument_list RPAREN'''
    if len(p) == 4:
        p[0] = ('function_call', p[1], [])
    else:
        p[0] = ('function_call', p[1], p[3])

def p_argument_list(p):
    '''argument_list : expression
                    | argument_list COMMA expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_not_expr(p):
    'not_expr : NOT expression'
    p[0] = ('not', p[2])

def p_logical_expr(p):
    '''logical_expr : expression AND expression
                   | expression OR expression'''
    p[0] = ('logical', p[2], p[1], p[3])

def p_binop_expr(p):
    '''binop_expr : expression PLUS expression
                 | expression MINUS expression
                 | expression TIMES expression
                 | expression DIVIDE expression
                 | expression LT expression
                 | expression LE expression
                 | expression GT expression
                 | expression GE expression
                 | expression EQ expression
                 | expression NE expression'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_group_expr(p):
    'group_expr : LPAREN expression RPAREN'
    p[0] = p[2]

def p_boolean(p):
    '''boolean : TRUE
              | FALSE'''
    p[0] = ('bool', p[1].lower() == 'true')

def p_number(p):
    'number : NUMBER'
    p[0] = ('number', p[1])

def p_id(p):
    'id : ID'
    p[0] = ('id', p[1])

def p_error(p):
    if p:
        print(f"Erro de sintaxe em '{p.value}' na linha {p.lineno}")
    else:
        print("Erro de sintaxe no final do arquivo")

parser = yacc.yacc()