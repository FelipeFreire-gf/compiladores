class Interpreter:
    def __init__(self):
        self.env_stack = [{}]  # Pilha de ambientes
        self.functions = {}    # Dicionário para armazenar funções
        self.return_value = None

    @property
    def env(self):
        return self.env_stack[-1]  # Ambiente atual

    def push_env(self):
        """Cria um novo escopo"""
        self.env_stack.append({})

    def pop_env(self):
        """Remove o escopo mais recente"""
        if len(self.env_stack) > 1:
            self.env_stack.pop()

    def interpret(self, ast):
        if ast is None:
            print("Erro: AST não foi gerada corretamente")
            return None
            
        if ast[0] == 'program':
            # Primeiro registra todas as funções
            for func in ast[1]:
                if func[0] == 'function':
                    self.functions[func[2]] = func
            
            # Depois executa a main
            if 'main' in self.functions:
                return self.interpret_function(self.functions['main'])
            else:
                print("Erro: função 'main' não encontrada")
                return None
        return None

    def interpret_function(self, node):
        self.push_env()  # Novo escopo para a função
        self.return_value = None
        
        # Inicializa parâmetros com valores padrão
        for param_type, param_name in node[3]:
            self.env[param_name] = 0
            
        # Executa o corpo da função
        for stmt in node[4]:
            self.eval(stmt)
            if self.return_value is not None:
                break
                
        result = self.return_value
        self.pop_env()  # Sai do escopo da função
        return result

    def eval(self, node):
        if node is None:
            return None
            
        node_type = node[0] if isinstance(node, tuple) else None
        
        if node_type == 'expression_stmt':
            return self.eval(node[1])
            
        elif node_type == 'declaration':
            var_name = node[2]
            self.env[var_name] = self.eval(node[3]) if node[3] is not None else 0
                
        elif node_type == 'assignment':
            # Procura a variável nos escopos aninhados
            for env in reversed(self.env_stack):
                if node[1] in env:
                    env[node[1]] = self.eval(node[2])
                    break
            else:
                # Variável não encontrada - cria no escopo atual
                self.env[node[1]] = self.eval(node[2])
            
        elif node_type == 'if':
            if self.eval(node[1]):
                self.push_env()  # Novo escopo para o bloco if
                for stmt in node[2]:
                    self.eval(stmt)
                self.pop_env()
            elif node[3] is not None:
                self.push_env()  # Novo escopo para o bloco else
                if isinstance(node[3], list):
                    for stmt in node[3]:
                        self.eval(stmt)
                else:
                    self.eval(node[3])
                self.pop_env()
                    
        elif node_type == 'while':
            while self.eval(node[1]):
                self.push_env()  # Novo escopo para cada iteração
                for stmt in node[2]:
                    if self.eval(stmt) is not None:
                        self.pop_env()
                        return
                self.pop_env()
                        
        elif node_type == 'return':
            self.return_value = self.eval(node[1])
            
        elif node_type == 'function_call':
            func_name = node[1]
            if func_name in self.functions:
                func = self.functions[func_name]
                
                # Avalia os argumentos
                args = [self.eval(arg) for arg in node[2]]
                
                # Verifica número de parâmetros
                if len(args) != len(func[3]):
                    print(f"Erro: número incorreto de argumentos para {func_name}")
                    return None
                    
                # Cria novo escopo para a chamada
                self.push_env()
                
                # Associa parâmetros aos argumentos
                for (param_type, param_name), arg_value in zip(func[3], args):
                    self.env[param_name] = arg_value
                    
                # Executa a função
                result = None
                for stmt in func[4]:
                    self.eval(stmt)
                    if self.return_value is not None:
                        result = self.return_value
                        break
                        
                self.pop_env()
                self.return_value = None  # Reseta para chamadas futuras
                return result
            else:
                print(f"Erro: função '{func_name}' não definida")
                return None
            
        elif isinstance(node, list):  # Bloco de código (compound_statement)
            self.push_env()  # Novo escopo
            for stmt in node:
                self.eval(stmt)
            self.pop_env()
            
        elif node_type == 'not':
            return not self.eval(node[1])
            
        elif node_type == 'logical':
            left = self.eval(node[2])
            right = self.eval(node[3])
            op = node[1]
            if op == '&&': return left and right
            elif op == '||': return left or right
            
        elif node_type == 'binop':
            left = self.eval(node[2])
            right = self.eval(node[3])
            op = node[1]
            return {
                '+': lambda a, b: a + b,
                '-': lambda a, b: a - b,
                '*': lambda a, b: a * b,
                '/': lambda a, b: a // b,
                '<': lambda a, b: a < b,
                '<=': lambda a, b: a <= b,
                '>': lambda a, b: a > b,
                '>=': lambda a, b: a >= b,
                '==': lambda a, b: a == b,
                '!=': lambda a, b: a != b
            }[op](left, right)
            
        elif node_type == 'number':
            return node[1]
            
        elif node_type == 'bool':
            return node[1]
            
        elif node_type == 'id':
            # Procura a variável nos escopos aninhados
            for env in reversed(self.env_stack):
                if node[1] in env:
                    return env[node[1]]
            return 0  # Valor padrão se variável não encontrada

        return None