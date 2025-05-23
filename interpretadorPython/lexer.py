import ply.lex as lex

reserved = {
    'int': 'INT',
    'void': 'VOID',
    'return': 'RETURN',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'true': 'TRUE',
    'false': 'FALSE'
}

tokens = [
    'ID', 'NUMBER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',
    'ASSIGN', 'AND', 'OR', 'NOT',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'LBRACKET', 'RBRACKET',
    'SEMI', 'COMMA', 'MOD'
] + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='
t_ASSIGN = r'='
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMI = r';'
t_COMMA = r','
t_MOD = r'\%'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_COMMENT(t):
    r'//.*'
    pass

def t_BLOCK_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
