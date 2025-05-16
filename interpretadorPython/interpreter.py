class Interpreter:
    def __init__(self):
        self.env_stack = [{}]  # Pilha de ambientes (env_stack[0] é o global)
        self.functions = {}    # Dicionário para armazenar funções
        self.return_value = None
        self.current_function = None  # Controla o contexto de execução

    @property
    def env(self):
        return self.env_stack[-1]

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
            # Primeiro processa todas as declarações globais e funções
            for element in ast[1]:
                if element[0] == 'function':
                    self.functions[element[2]] = element
                elif element[0] == 'declaration':
                    self.eval(element)
            
            # Depois executa a main
            if 'main' in self.functions:
                return self.interpret_function(self.functions['main'])
            else:
                print("Erro: função 'main' não encontrada")
                return None
        return None

    def interpret_function(self, node):
        """Executa uma função com novo escopo"""
        previous_function = self.current_function
        self.current_function = node[2]  # Armazena nome da função atual
        self.push_env()
        self.return_value = None
        
        # Inicializa parâmetros
        for param_type, param_name in node[3]:
            self.env[param_name] = 0
            
        # Executa o corpo
        for stmt in node[4]:
            self.eval(stmt)
            if self.return_value is not None:
                break
                
        result = self.return_value
        self.pop_env()
        self.current_function = previous_function  # Restaura contexto
        return result

    def eval(self, node):
        if node is None:
            return None
            
        node_type = node[0] if isinstance(node, tuple) else None
        
        if node_type == 'expression_stmt':
            return self.eval(node[1])
            
        elif node_type == 'declaration':
            var_name = node[2]
            # Declarações no escopo global vão para env_stack[0]
            if len(self.env_stack) == 1:  # Escopo global
                self.env_stack[0][var_name] = self.eval(node[3]) if node[3] is not None else 0
            else:  # Escopo local
                self.env[var_name] = self.eval(node[3]) if node[3] is not None else 0
                
        elif node_type == 'assignment':
            var_name = node[1]
            # Em funções, verifica se é uma variável global existente
            if self.current_function and var_name in self.env_stack[0] and var_name not in self.env:
                self.env_stack[0][var_name] = self.eval(node[2])
            else:
                # Atribuição normal (procura em todos os escopos)
                for env in reversed(self.env_stack):
                    if var_name in env:
                        env[var_name] = self.eval(node[2])
                        return
                # Se não encontrou, cria no escopo atual
                self.env[var_name] = self.eval(node[2])
            
        elif node_type == 'if':
            if self.eval(node[1]):
                self.push_env()
                for stmt in node[2]:
                    self.eval(stmt)
                self.pop_env()
            elif node[3] is not None:
                self.push_env()
                if isinstance(node[3], list):
                    for stmt in node[3]:
                        self.eval(stmt)
                else:
                    self.eval(node[3])
                self.pop_env()
                    
        elif node_type == 'while':
            while self.eval(node[1]):
                self.push_env()
                for stmt in node[2]:
                    self.eval(stmt)
                    if self.return_value is not None:
                        self.pop_env()
                        return
                self.pop_env()
                        
        elif node_type == 'return':
            self.return_value = self.eval(node[1])
            
        elif node_type == 'function_call':
            func_name = node[1]
            if func_name in self.functions:
                func = self.functions[func_name]
                
                # Avalia argumentos
                args = [self.eval(arg) for arg in node[2]]
                
                if len(args) != len(func[3]):
                    print(f"Erro: número incorreto de argumentos para {func_name}")
                    return None
                    
                self.push_env()
                
                # Associa parâmetros
                for (param_type, param_name), arg_value in zip(func[3], args):
                    self.env[param_name] = arg_value
                    
                # Executa função
                result = None
                for stmt in func[4]:
                    self.eval(stmt)
                    if self.return_value is not None:
                        result = self.return_value
                        break
                        
                self.pop_env()
                self.return_value = None
                return result
            else:
                print(f"Erro: função '{func_name}' não definida")
                return None
            
        elif isinstance(node, list):  # Bloco de código
            self.push_env()
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
            ops = {
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
            }
            return ops[op](left, right)
            
        elif node_type == 'number':
            return node[1]
            
        elif node_type == 'bool':
            return node[1]
            
        elif node_type == 'id':
            # Dentro de função, verifica se é global
            if self.current_function and node[1] in self.env_stack[0] and node[1] not in self.env:
                return self.env_stack[0][node[1]]
            # Busca normal na pilha
            for env in reversed(self.env_stack):
                if node[1] in env:
                    return env[node[1]]
            return 0  # Valor padrão para variáveis não declaradas

        return None