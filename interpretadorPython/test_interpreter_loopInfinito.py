from interpreter import Interpreter  # Importa a classe Interpreter

# Criar uma instância do interpretador
interpreter = Interpreter()

# Configurar o ambiente inicial
interpreter.env["counter"] = 0

# Definir a AST para o loop infinito
ast = ('while', ('bool', True), [  # Correção: Usar a representação de AST para booleano
    ('expression_stmt', ('assignment', 'counter', ('binop', '+', ('id', 'counter'), ('number', 1)))),
    ('if', ('binop', '>=', ('id', 'counter'), ('number', 5)), [  # Condição para sair do loop
        ('return', ('id', 'counter'))
    ], None)
])

# Executar o loop (interpreter.eval para um 'while' retorna None, mas define self.return_value)
interpreter.eval(ast)

# Verificar o valor final do contador
assert interpreter.return_value == 5, f"O loop infinito do while não funcionou corretamente. Valor retornado: {interpreter.return_value}"
print("Teste do loop infinito do while passou com sucesso!")