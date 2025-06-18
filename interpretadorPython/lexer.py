import ply.lex as lex

# Palavras chave (reservadas da linguagem) 
# É tipo uns tokens especiais
reserved = {
    'int': 'INT',
    'void': 'VOID',
    'return': 'RETURN',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'true': 'TRUE',
    'false': 'FALSE',
    'print': 'PRINT',
    'input': 'INPUT'
}

# Lista de todos os tokens que o analisador léxico pode reconhecer
tokens = [
    'ID', 'NUMBER', 'STRING', 'INCLUDE',      # identificadores, números, strings e includes
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',       # operadores aritméticos (+ - * /)
    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',       # operadores relacionais (< <= > >= == !=)
    'ASSIGN', 'AND', 'OR', 'NOT',             # operadores lógicos e de atribuição (= && || !)
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',   # parênteses e chaves (( ) { })
    'LBRACKET', 'RBRACKET',                   # colchetes ([ ])
    'SEMI', 'COMMA', 'MOD', 'ADDRESS'         # ponto e vírgula, vírgula, módulo, e operador de endereço
] + list(reserved.values())  # incluir os tokens das palavras reservadas acima

# Expressões regulares simples 
# Associam símbolos do código a seus respectivos tokens
# Diz como reconhecer cada token
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
t_ADDRESS = r'&'
t_ignore = ' \t'  # Ignora espaços em branco e tabulações

# Aqui são expressões mais complexas que precisam de funções
# Expressão para detectar diretivas de include (ex: #include <stdio.h>)
def t_INCLUDE(t):
    r'\#include\s*<\w+(\.\w+)*\s*>|\#\s*include\s*\"\w+(\.\w+)*\s*\"'
    return t

# Expressão para strings entre aspas (ex: "Olá mundo")
def t_STRING(t):
    r'\"([^\\\"]|\\.)*\"'
    t.value = t.value[1:-1]  # Remove as aspas da string
    return t

# Expressão para identificadores (ex: nomes de variáveis ou funções criadas pelo programador)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Verifica se é palavra reservada
    return t

# Expressão para números inteiros
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)  # Converte o valor para inteiro
    return t

# Comentários de linha (ex: // comentário) — são ignorados
def t_COMMENT(t):
    r'//.*'
    pass  # Não faz nada, apenas ignora

# Comentários de bloco (ex: /* ... */) — também são ignorados
def t_BLOCK_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')  # Atualiza número de linhas
    pass

# Detecção de novas linhas para controle de linha (útil para mensagens de erro)
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)  # Conta quantas linhas foram puladas

# Função de tratamento de erro — quando um caractere inválido aparece
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}'")
    t.lexer.skip(1)  # Pula o caractere inválido e continua

# Criação do analisador léxico (lexer) com base nas definições acima
lexer = lex.lex()
