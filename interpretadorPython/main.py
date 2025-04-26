import sys
from lexer import lexer
from parser import parser
from interpreter import Interpreter

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py arquivo.c")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        code = f.read()

    # Análise léxica
    lexer.input(code)
    print("\nTokens:")
    for token in lexer:
        print(token)

    # Análise sintática
    ast = parser.parse(code)
    print("\nAST:")
    print(ast)

    if ast is None:
        print("\nErro: Não foi possível gerar a AST")
        sys.exit(1)

    # Interpretação
    interpreter = Interpreter()
    result = interpreter.interpret(ast)
    
    print("\nResultado:", result)
    print("Variáveis finais:", interpreter.env)

if __name__ == "__main__":
    main()