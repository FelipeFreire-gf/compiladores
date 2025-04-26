import sys
from lexer import lexer
from parser import parser

def analisar_parametros(codigo):
    lexer.input(codigo)
    print("Tokens:")
    for tok in lexer:
        print(tok)

    print("\nParsing:")
    resultado = parser.parse(codigo)
    print(resultado)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python main.py arquivo.c")
        sys.exit(1)

    arquivo = sys.argv[1]
    with open(arquivo, 'r') as f:
        conteudo = f.read()
        analisar_parametros(conteudo)

