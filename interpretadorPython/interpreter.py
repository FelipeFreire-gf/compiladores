class Interpreter:
    def __init__(self):
        self.env_stack = [{}]
        self.functions = {}
        self.arrays = {}
        self.pointers = {}  # Armazena os ponteiros
        self.memory = {}    # Memória simulada
        self.next_address = 1000  # Endereço inicial para alocação
        self.return_value = None
        self.current_function = None

    @property
    def env(self):
        return self.env_stack[-1]

    def push_env(self):
        self.env_stack.append({})

    def pop_env(self):
        if len(self.env_stack) > 1:
            self.env_stack.pop()

    def allocate_memory(self, size=1):
        """Aloca memória e retorna o endereço base"""
        address = self.next_address
        self.next_address += size
        self.memory[address] = [0] * size
        return address

    def free_memory(self, address):
        """Libera a memória alocada"""
        if address in self.memory:
            del self.memory[address]

    def get_pointer_value(self, address, offset=0):
        """Obtém o valor apontado pelo ponteiro"""
        if address in self.memory:
            return self.memory[address][offset]
        return None

    def set_pointer_value(self, address, value, offset=0):
        """Define o valor apontado pelo ponteiro"""
        if address in self.memory:
            self.memory[address][offset] = value

    def interpret(self, ast):
        if ast is None:
            print("Erro: AST não foi gerada corretamente")
            return None
            
        if ast[0] == 'program':
            for element in ast[1]:
                if element[0] == 'function':
                    self.functions[element[2]] = element
                elif element[0] in ['declaration', 'array_declaration', 'array_declaration_init', 'pointer_declaration']:
                    self.eval(element)
            
            if 'main' in self.functions:
                return self.interpret_function(self.functions['main'])
            else:
                print("Erro: função 'main' não encontrada")
                return None
        return None

    def interpret_function(self, node):
        previous_function = self.current_function
        self.current_function = node[2]
        self.push_env()
        self.return_value = None
        
        for param_type, param_name, is_array, is_pointer in node[3]:
            if is_pointer:
                self.pointers[param_name] = self.allocate_memory()
                self.env[param_name] = {'type': 'pointer', 'address': self.pointers[param_name]}
            elif is_array:
                self.arrays[param_name] = []
                self.env[param_name] = {'type': 'array', 'size': 0}
            else:
                self.env[param_name] = 0
                
        for stmt in node[4]:
            self.eval(stmt)
            if self.return_value is not None:
                break
                
        result = self.return_value
        self.pop_env()
        self.current_function = previous_function
        return result

    def eval(self, node):
        if node is None:
            return None
            
        node_type = node[0] if isinstance(node, tuple) else None
        
        if node_type == 'expression_stmt':
            return self.eval(node[1])
            
        elif node_type == 'declaration':
            var_name = node[2]
            if len(self.env_stack) == 1:
                self.env_stack[0][var_name] = self.eval(node[3]) if node[3] is not None else 0
            else:
                self.env[var_name] = self.eval(node[3]) if node[3] is not None else 0
                
        elif node_type == 'array_declaration':
            type_, name, size = node[1], node[2], node[3]
            self.arrays[name] = [0] * size
            self.env[name] = {'type': 'array', 'size': size}
            
        elif node_type == 'array_declaration_init':
            type_, name, size, values = node[1], node[2], node[3], node[4]
            self.arrays[name] = [self.eval(val) for val in values]
            if len(self.arrays[name]) != size:
                print(f"Aviso: Tamanho do array '{name}' não corresponde à inicialização")
            self.env[name] = {'type': 'array', 'size': size}
            
        elif node_type == 'assignment':
            var_name = node[1]
            if self.current_function and var_name in self.env_stack[0] and var_name not in self.env:
                self.env_stack[0][var_name] = self.eval(node[2])
            else:
                for env in reversed(self.env_stack):
                    if var_name in env:
                        env[var_name] = self.eval(node[2])
                        return
                self.env[var_name] = self.eval(node[2])
            
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
                args = [self.eval(arg) for arg in node[2]]
                
                if len(args) != len(func[3]):
                    print(f"Erro: número incorreto de argumentos para {func_name}")
                    return None
                    
                self.push_env()
                
                for (param_type, param_name, is_array), arg_value in zip(func[3], args):
                    if is_array:
                        self.arrays[param_name] = arg_value.copy() if isinstance(arg_value, list) else arg_value
                        self.env[param_name] = {'type': 'array', 'size': len(self.arrays[param_name])}
                    else:
                        self.env[param_name] = arg_value
                        
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
            
        elif isinstance(node, list):
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
            var_name = node[1]
            if var_name in self.pointers:
                return self.pointers[var_name]
            elif var_name in self.arrays:
                return self.arrays[var_name]
            elif self.current_function and var_name not in self.env and var_name in self.env_stack[0]:
                return self.env_stack[0][var_name]
            for env in reversed(self.env_stack):
                if var_name in env:
                    return env[var_name]
            return 0
            
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

        elif node_type == 'pointer_declaration':
            var_name = node[2]
            if node[3] is not None:  # Inicialização
                value = self.eval(node[3])
                if isinstance(value, int):  # Endereço direto
                    self.pointers[var_name] = value
                else:  # Valor a ser armazenado
                    address = self.allocate_memory()
                    self.set_pointer_value(address, value)
                    self.pointers[var_name] = address
            else:
                self.pointers[var_name] = self.allocate_memory()
            self.env[var_name] = {'type': 'pointer', 'address': self.pointers[var_name]}

        elif node_type == 'pointer_assignment':
            ptr_name = node[1]
            if ptr_name in self.pointers:
                value = self.eval(node[2])
                self.set_pointer_value(self.pointers[ptr_name], value)
            else:
                print(f"Erro: Ponteiro '{ptr_name}' não declarado")

        elif node_type == 'pointer_dereference':
            ptr_name = node[1]
            if ptr_name in self.pointers:
                return self.get_pointer_value(self.pointers[ptr_name])
            else:
                print(f"Erro: Ponteiro '{ptr_name}' não declarado")
                return None

        elif node_type == 'address_of':
            var_name = node[1]
            if var_name in self.env:
                if isinstance(self.env[var_name], dict) and self.env[var_name]['type'] == 'pointer':
                    return self.env[var_name]['address']
                else:
                    address = self.allocate_memory()
                    self.set_pointer_value(address, self.env[var_name])
                    return address
            else:
                print(f"Erro: Variável '{var_name}' não declarada")
                return None

        return None