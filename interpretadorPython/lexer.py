import ply.lex as lex

# Palavras-chave do C
reserved = {
    'auto': 'AUTO', 'break': 'BREAK', 'case': 'CASE', 'char': 'CHAR', 'const': 'CONST',
    'continue': 'CONTINUE', 'default': 'DEFAULT', 'do': 'DO', 'double': 'DOUBLE',
    'else': 'ELSE', 'enum': 'ENUM', 'extern': 'EXTERN', 'float': 'FLOAT', 'for': 'FOR',
    'goto': 'GOTO', 'if': 'IF', 'inline': 'INLINE', 'int': 'INT', 'long': 'LONG',
    'register': 'REGISTER', 'restrict': 'RESTRICT', 'return': 'RETURN', 'short': 'SHORT',
    'signed': 'SIGNED', 'sizeof': 'SIZEOF', 'static': 'STATIC', 'struct': 'STRUCT',
    'switch': 'SWITCH', 'typedef': 'TYPEDEF', 'union': 'UNION', 'unsigned': 'UNSIGNED',
    'void': 'VOID', 'volatile': 'VOLATILE', 'while': 'WHILE', '_Alignas': 'ALIGNAS',
    '_Alignof': 'ALIGNOF', '_Atomic': 'ATOMIC', '_Bool': 'BOOL', '_Complex': 'COMPLEX',
    '_Generic': 'GENERIC', '_Imaginary': 'IMAGINARY', '_Noreturn': 'NORETURN',
    '_Static_assert': 'STATIC_ASSERT', '_Thread_local': 'THREAD_LOCAL'
}

# Tokens
tokens = [
    'ID', 'NUMBER', 'STRING', 'CHARACTER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
    'AND', 'OR', 'NOT', 'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',
    'ASSIGN',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
    'COMMA', 'SEMI', 'DOT', 'ARROW', 'ELLIPSIS'
] + list(reserved.values())

# Regras de token simples
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_MOD       = r'%'
t_AND       = r'&&'
t_OR        = r'\|\|'
t_NOT       = r'!'
t_LT        = r'<'
t_LE        = r'<='
t_GT        = r'>'
t_GE        = r'>='
t_EQ        = r'=='
t_NE        = r'!='
t_ASSIGN    = r'='
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
t_LBRACKET  = r'\['
t_RBRACKET  = r'\]'
t_COMMA     = r','
t_SEMI      = r';'
t_DOT       = r'\.'
t_ARROW     = r'->'
t_ELLIPSIS  = r'\.\.\.'

def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Verifica se é palavra reservada
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

def t_CHARACTER(t):
    r'\'([^\\\n]|(\\.))*?\''
    return t

# Ignorar espaços e tabulações
t_ignore = ' \t'

# Nova linha
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Erro
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
