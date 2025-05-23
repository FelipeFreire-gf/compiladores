class Interpreter:
    def __init__(self):
        self.env_stack = [{}]  # Pilha de ambientes (escopos)
        self.functions = {}    # Dicionário de funções
        self.arrays = {}       # Dicionário de arrays
        self.return_value = None  # Valor de retorno
        self.current_function = None  # Função atual sendo executada

    @property
    def env(self):
        """Retorna o ambiente atual (último da pilha)"""
        return self.env_stack[-1]

    def push_env(self):
        """Adiciona um novo escopo/ambiente na pilha"""
        self.env_stack.append({})

    def pop_env(self):
        """Remove o escopo/ambiente atual da pilha"""
        if len(self.env_stack) > 1:
            self.env_stack.pop()

    def interpret(self, ast):
        """Interpreta a AST completa"""
        if ast is None:
            print("Erro: AST não foi gerada corretamente")
            return None
            
        if ast[0] == 'program':
            # Primeiro passada: registrar todas as funções
            for element in ast[1]:
                if element[0] == 'function':
                    self.functions[element[2]] = element
            
            # Segunda passada: processar declarações globais
            for element in ast[1]:
                if element[0] in ['declaration', 'array_declaration', 'array_declaration_init']:
                    self.eval(element)
            
            # Executar a função main
            if 'main' in self.functions:
                return self.interpret_function(self.functions['main'])
            else:
                print("Erro: função 'main' não encontrada")
                return None
        return None

    def interpret_function(self, node):
        """Interpreta uma função específica"""
        previous_function = self.current_function
        self.current_function = node[2]  # Nome da função
        self.push_env()  # Novo escopo para a função
        self.return_value = None
        
        # Processa parâmetros
        for param_type, param_name, is_array in node[3]:
            if is_array:
                self.arrays[param_name] = []
                self.env[param_name] = {'type': 'array', 'size': 0}
            else:
                self.env[param_name] = 0  # Valor padrão
                
        # Executa cada statement no corpo da função
        for stmt in node[4]:
            self.eval(stmt)
            if self.return_value is not None:  # Se encontrou um return
                break
                
        result = self.return_value
        self.pop_env()  # Remove o escopo da função
        self.current_function = previous_function
        return result if result is not None else 0  # Retorna 0 se não houver valor de retorno

    def eval(self, node):
        """Avalia um nó da AST"""
        if node is None:
            return None
            
        node_type = node[0] if isinstance(node, tuple) else None
        
        # Expressão statement (apenas avalia a expressão)
        if node_type == 'expression_stmt':
            return self.eval(node[1])
            
        # Declaração de variável
        elif node_type == 'declaration':
            var_name = node[2]
            initial_value = self.eval(node[3]) if len(node) > 3 else 0
            
            if len(self.env_stack) == 1:  # Escopo global
                self.env_stack[0][var_name] = initial_value
            else:  # Escopo local
                self.env[var_name] = initial_value
                
        # Declaração de array sem inicialização
        elif node_type == 'array_declaration':
            type_, name, size = node[1], node[2], node[3]
            self.arrays[name] = [0] * size
            self.env[name] = {'type': 'array', 'size': size}
            
        # Declaração de array com inicialização
        elif node_type == 'array_declaration_init':
            type_, name, size, values = node[1], node[2], node[3], node[4]
            self.arrays[name] = [self.eval(val) for val in values]
            if len(self.arrays[name]) != size:
                print(f"Aviso: Tamanho do array '{name}' não corresponde à inicialização")
            self.env[name] = {'type': 'array', 'size': size}
            
        # Atribuição simples
        elif node_type == 'assignment':
            var_name = node[1]
            value = self.eval(node[2])
            
            # Verifica se é uma variável global sendo acessada de dentro de uma função
            if self.current_function and var_name in self.env_stack[0] and var_name not in self.env:
                self.env_stack[0][var_name] = value
            else:
                # Procura a variável na pilha de escopos (do mais interno para o mais externo)
                for env in reversed(self.env_stack):
                    if var_name in env:
                        env[var_name] = value
                        return
                # Se não encontrou, cria no escopo atual
                self.env[var_name] = value
            
        # Atribuição de array
        elif node_type == 'array_assignment':
            array_name, index_expr, value_expr = node[1], node[2], node[3]
            if array_name not in self.arrays:
                print(f"Erro: Array '{array_name}' não declarado")
                return
            index = self.eval(index_expr)
            if not isinstance(index, int) or index < 0 or index >= len(self.arrays[array_name]):
                print(f"Erro: Índice {index} inválido para array '{array_name}'")
                return
            self.arrays[array_name][index] = self.eval(value_expr)
            
        # Condicional if
        elif node_type == 'if':
            if self.eval(node[1]):
                self.push_env()
                for stmt in node[2]:
                    self.eval(stmt)
                self.pop_env()
            elif node[3] is not None:  # Tem else
                self.push_env()
                if isinstance(node[3], list):
                    for stmt in node[3]:
                        self.eval(stmt)
                else:
                    self.eval(node[3])
                self.pop_env()
                    
        # Loop while
        elif node_type == 'while':
            while self.eval(node[1]):
                self.push_env()
                for stmt in node[2]:
                    self.eval(stmt)
                    if self.return_value is not None:  # Return encontrado
                        self.pop_env()
                        return
                self.pop_env()
                        
        # Return statement
        elif node_type == 'return':
            self.return_value = self.eval(node[1])
            
        # Chamada de função
        elif node_type == 'function_call':
            func_name = node[1]
            if func_name not in self.functions:
                print(f"Erro: função '{func_name}' não definida")
                return 0  # Retorna 0 para evitar problemas com operações
            
            func = self.functions[func_name]
            args = [self.eval(arg) for arg in node[2]]
            
            if len(args) != len(func[3]):
                print(f"Erro: número incorreto de argumentos para {func_name}")
                return 0
                
            self.push_env()  # Novo escopo para os parâmetros
            
            # Associa os argumentos aos parâmetros
            for (param_type, param_name, is_array), arg_value in zip(func[3], args):
                if is_array:
                    self.arrays[param_name] = arg_value.copy() if isinstance(arg_value, list) else arg_value
                    self.env[param_name] = {'type': 'array', 'size': len(self.arrays[param_name])}
                else:
                    self.env[param_name] = arg_value
                    
            result = 0  # Valor padrão
            for stmt in func[4]:
                self.eval(stmt)
                if self.return_value is not None:
                    result = self.return_value
                    break
                    
            self.pop_env()
            self.return_value = None  # Reseta para a função chamadora
            return result
            
        # Bloco de statements
        elif isinstance(node, list):
            self.push_env()
            for stmt in node:
                self.eval(stmt)
            self.pop_env()
            
        # Operador lógico NOT
        elif node_type == 'not':
            return not self.eval(node[1])
            
        # Operadores lógicos AND e OR
        elif node_type == 'logical':
            left = self.eval(node[2])
            right = self.eval(node[3])
            op = node[1]
            if op == '&&': return left and right
            elif op == '||': return left or right
            
        # Operadores binários
        elif node_type == 'binop':
            left = self.eval(node[2])
            right = self.eval(node[3])
            op = node[1]
            ops = {
                '+': lambda a, b: a + b,
                '-': lambda a, b: a - b,
                '*': lambda a, b: a * b,
                '/': lambda a, b: a // b,
                '%': lambda a, b: a % b,  # Adicionado operador módulo
                '<': lambda a, b: a < b,
                '<=': lambda a, b: a <= b,
                '>': lambda a, b: a > b,
                '>=': lambda a, b: a >= b,
                '==': lambda a, b: a == b,
                '!=': lambda a, b: a != b
            }
            return ops[op](left, right)
            
        # Literal numérico
        elif node_type == 'number':
            return node[1]
            
        # Literal booleano
        elif node_type == 'bool':
            return node[1]
            
        # Identificador (variável)
        elif node_type == 'id':
            var_name = node[1]
            if var_name in self.arrays:
                return self.arrays[var_name]
                
            # Verifica se é uma variável global sendo acessada de dentro de uma função
            if self.current_function and var_name not in self.env and var_name in self.env_stack[0]:
                return self.env_stack[0][var_name]
                
            # Procura a variável na pilha de escopos
            for env in reversed(self.env_stack):
                if var_name in env:
                    return env[var_name]
            return 0  # Retorna 0 se a variável não foi encontrada
            
        # Acesso a array
        elif node_type == 'array_access':
            array_name, index_expr = node[1], node[2]
            if array_name not in self.arrays:
                print(f"Erro: Array '{array_name}' não declarado")
                return 0
            index = self.eval(index_expr)
            if not isinstance(index, int) or index < 0 or index >= len(self.arrays[array_name]):
                print(f"Erro: Índice {index} inválido para array '{array_name}'")
                return 0
            return self.arrays[array_name][index]

        return None