class Interpreter:
    def __init__(self):
        self.env = {}
        self.return_value = None

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
        self.env = {}
        self.return_value = None
        for stmt in node[3]:
            self.eval(stmt)
            if self.return_value is not None:
                return self.return_value
        return self.return_value

    def eval(self, node):
        if node is None:
            return None
            
        node_type = node[0]
        
        if node_type == 'expression_stmt':
            return self.eval(node[1])
            
        elif node_type == 'declaration':
            var_name = node[2]
            self.env[var_name] = self.eval(node[3]) if node[3] is not None else 0
                
        elif node_type == 'assignment':
            self.env[node[1]] = self.eval(node[2])
            
        elif node_type == 'if':
            if self.eval(node[1]):
                for stmt in node[2]:
                    self.eval(stmt)
            elif node[3] is not None:
                if isinstance(node[3], list):
                    for stmt in node[3]:
                        self.eval(stmt)
                else:
                    self.eval(node[3])
                    
        elif node_type == 'while':
            while self.eval(node[1]):
                for stmt in node[2]:
                    if self.eval(stmt) is not None:
                        return
                        
        elif node_type == 'return':
            self.return_value = self.eval(node[1])
            
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
            return self.env.get(node[1], 0)

        return None