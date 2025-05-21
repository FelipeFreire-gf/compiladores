import ply.yacc as yacc
from lexer import tokens

precedence = (
    ('right', 'NOT'),
    ('left', 'AND', 'OR'),
    ('left', 'LT', 'LE', 'GT', 'GE', 'EQ', 'NE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
    ('right', 'DEREFERENCE'),
    ('right', 'ADDRESS_OF')
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
              | declaration
              | pointer_declaration'''
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
                | type ID LBRACKET RBRACKET
                | type TIMES ID'''
    if len(p) == 3:
        p[0] = (p[1], p[2], False, False)
    elif len(p) == 5:
        p[0] = (p[1], p[2], True, False)
    else:
        p[0] = (p[1], p[3], False, True)

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
                | pointer_declaration
                | assignment
                | pointer_assignment
                | if_statement
                | while_statement
                | return_statement
                | expression_stmt
                | compound_statement'''
    p[0] = p[1]

def p_declaration(p):
    '''declaration : type ID SEMI
                  | type ID ASSIGN expression SEMI'''
    if len(p) == 4:
        p[0] = ('declaration', p[1], p[2], None)
    else:
        p[0] = ('declaration', p[1], p[2], p[4])

def p_pointer_declaration(p):
    '''pointer_declaration : type TIMES ID SEMI
                          | type TIMES ID ASSIGN expression SEMI'''
    if len(p) == 5:
        p[0] = ('pointer_declaration', p[1], p[3], None)
    else:
        p[0] = ('pointer_declaration', p[1], p[3], p[5])

def p_assignment(p):
    '''assignment : ID ASSIGN expression SEMI'''
    p[0] = ('assignment', p[1], p[3])

def p_pointer_assignment(p):
    '''pointer_assignment : TIMES ID ASSIGN expression SEMI'''
    p[0] = ('pointer_assignment', p[2], p[4])

def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN compound_statement
                   | IF LPAREN expression RPAREN compound_statement ELSE compound_statement
                   | IF LPAREN expression RPAREN compound_statement ELSE if_statement'''
    if len(p) == 6:
        p[0] = ('if', p[3], p[5], None)
    else:
        p[0] = ('if', p[3], p[5], p[7])

def p_while_statement(p):
    '''while_statement : WHILE LPAREN expression RPAREN compound_statement'''
    p[0] = ('while', p[3], p[5])

def p_return_statement(p):
    '''return_statement : RETURN SEMI
                       | RETURN expression SEMI'''
    if len(p) == 3:
        p[0] = ('return', None)
    else:
        p[0] = ('return', p[2])

def p_expression_stmt(p):
    '''expression_stmt : expression SEMI'''
    p[0] = ('expression_stmt', p[1])

def p_expression(p):
    '''expression : term
                 | expression PLUS term
                 | expression MINUS term
                 | expression LT term
                 | expression LE term
                 | expression GT term
                 | expression GE term
                 | expression EQ term
                 | expression NE term
                 | expression AND term
                 | expression OR term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('binop', p[2], p[1], p[3])

def p_term(p):
    '''term : factor
            | term TIMES factor
            | term DIVIDE factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('binop', p[2], p[1], p[3])

def p_factor(p):
    '''factor : NUMBER
              | ID
              | LPAREN expression RPAREN
              | NOT factor
              | TIMES factor %prec DEREFERENCE
              | AMPERSAND factor %prec ADDRESS_OF
              | function_call
              | array_access
              | TRUE
              | FALSE'''
    if len(p) == 2:
        if isinstance(p[1], int):
            p[0] = ('number', p[1])
        elif p[1] == 'true':
            p[0] = ('bool', True)
        elif p[1] == 'false':
            p[0] = ('bool', False)
        else:
            p[0] = ('id', p[1])
    elif len(p) == 3:
        if p[1] == '!':
            p[0] = ('not', p[2])
        elif p[1] == '*':
            p[0] = ('pointer_dereference', p[2][1])
        elif p[1] == '&':
            p[0] = ('address_of', p[2][1])
    else:
        p[0] = p[2]

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

def p_array_access(p):
    '''array_access : ID LBRACKET expression RBRACKET'''
    p[0] = ('array_access', p[1], p[3])

def p_error(p):
    if p:
        print(f"Erro de sintaxe em '{p.value}'")
    else:
        print("Erro de sintaxe no final do arquivo")

parser = yacc.yacc()