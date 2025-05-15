class Interpreter:
    def __init__(self):
        self.env_stack = [{}]  # Pilha de ambientes
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
            node = ast[1]
            if node[0] == 'function':
                return self.interpret_function(node)
            else:
                return self.eval(node)
        return None

    def interpret_function(self, node):
        self.push_env()  # Novo escopo para a função
        self.return_value = None
        for stmt in node[3]:  # node[3] agora é a lista de statements
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