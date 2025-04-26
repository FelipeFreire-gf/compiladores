class Interpreter:
    def __init__(self):
        self.env = {}
        self.return_value = None

    def interpret(self, ast):
        if ast is None:
            print("Erro: AST não foi gerada corretamente")
            return None
            
        if ast[0] == 'function':
            self.env = {}
            self.return_value = None
            for stmt in ast[3]:
                self.eval(stmt)
                if self.return_value is not None:
                    return self.return_value
            return self.return_value
        return None

    def eval(self, node):
        if node is None:
            return None
            
        if node[0] == 'declaration':
            var_name = node[2]
            if node[3] is not None:
                self.env[var_name] = self.eval(node[3])
            else:
                self.env[var_name] = 0
                
        elif node[0] == 'assignment':
            var_name = node[1]
            self.env[var_name] = self.eval(node[2])
            
        elif node[0] == 'if':
            condition = self.eval(node[1])
            if condition:
                for stmt in node[2]:
                    self.eval(stmt)
            elif node[3] is not None:  # else ou else if
                if isinstance(node[3], list):  # else normal
                    for stmt in node[3]:
                        self.eval(stmt)
                else:  # else if (outro nó if)
                    self.eval(node[3])
                    
        elif node[0] == 'while':
            while self.eval(node[1]):
                for stmt in node[2]:
                    if self.eval(stmt) is not None:  # Se encontrou um return
                        return
                        
        elif node[0] == 'return':
            self.return_value = self.eval(node[1])
            
        elif node[0] == 'binop':
            left = self.eval(node[2])
            right = self.eval(node[3])
            op = node[1]
            if op == '+': return left + right
            elif op == '-': return left - right
            elif op == '*': return left * right
            elif op == '/': return left // right
            elif op == '<': return left < right
            elif op == '<=': return left <= right
            elif op == '>': return left > right
            elif op == '>=': return left >= right
            elif op == '==': return left == right
            elif op == '!=': return left != right
            
        elif node[0] == 'number':
            return node[1]
            
        elif node[0] == 'id':
            return self.env.get(node[1], 0)

        return None