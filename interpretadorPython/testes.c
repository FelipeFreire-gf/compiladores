a
3

/*

para executar:

instalar biblioteca ply --> pip install ply

python main.py testes.c

para o teste:

a
3

Explicacao da saida:

LexToken(ID, 'a', 1, 0):

    ID: O tipo do token, que é um identificador (geralmente usado para variáveis, funções ou outros nomes).

    'a': O valor do token, ou seja, o identificador detectado.

    1: A linha onde o token foi encontrado no arquivo de entrada.

    0: A posição dentro da linha onde o token foi encontrado (a primeira coluna).

Explicação: O lexer identificou que o símbolo 'a' é um identificador (ID). O 'a' não é uma palavra-chave ou um número, portanto, é classificado como ID.

LexToken(NUMBER, 3, 2, 2):

    NUMBER: O tipo do token, que é um número.

    3: O valor do token, ou seja, o número literal detectado.

    2: A linha onde o token foi encontrado no arquivo de entrada.

    2: A posição dentro da linha onde o token foi encontrado.

Explicação: O lexer identificou que o símbolo 3 é um número (NUMBER), e foi encontrado na linha 2, coluna 2.

*/
