# Interpreter
# 1. Executa o programa representado pela árvore sintática (AST) gerada pelo parser
# 2. Interpreta cada comando: variáveis, expressões, funções, if, while, ponteiros, etc.
# 3. Simula escopos (variáveis locais e globais), arrays e ponteiros
# 4. Controla a memória (endereços simulados) e o valor de retorno das funções
# 5. É chamado pelo main.py depois que o parser gera a AST

class Interpreter:
    def __init__(self):
        self.env_stack = [{}]
        self.functions = {}
        self.arrays = {}
        self.pointers = {}
        self.memory_counter = 1000
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

    def alloc_address(self):
        addr = self.memory_counter
        self.memory_counter += 1
        return addr

    def interpret(self, ast):
        if ast is None:
            # Mensagem melhorada: Informa que o erro vem do parser.
            print("Erro Crítico: A Árvore Sintática (AST) não foi gerada. Verifique os erros de sintaxe reportados pelo parser.")
            return None
            
        if ast[0] == 'program':
            for element in ast[1]:
                if element[0] == 'function':
                    self.functions[element[2]] = element
                elif element[0] == 'include':
                    self.eval(element)
                elif element[0] in ['declaration', 'array_declaration', 'array_declaration_init', 'pointer_decl']:
                    self.eval(element)
            
            if 'main' in self.functions:
                return self.interpret_function(self.functions['main'])
            else:
                # Mensagem melhorada
                print("Erro de Execução: A função 'main' não foi encontrada. Todo programa deve ter um ponto de entrada main().")
                return None
        return None

    def interpret_function(self, node):
        previous_function = self.current_function
        self.current_function = node[2]
        self.push_env()
        self.return_value = None

        
        for param_type, param_name, is_array in node[3]:
            if isinstance(param_type, tuple) and param_type[2] > 0:
                self.env[param_name] = None
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
        # Removendo prints de depuração intermediários para focar nas saídas de erro
        # print("Variáveis locais:", self.env) 
        self.pop_env()
        self.current_function = previous_function
        # print("\nVariáveis locais da função", node[2] + ":", self.env)
        return result

    def eval(self, node):
        if node is None:
            return None
            
        node_type = node[0] if isinstance(node, tuple) else None
        
        if node_type == 'include':
            if 'stdio.h' in node[1]:
                self.functions['print'] = ('function', 'void', 'print', [('type', 'int', 0)], [])
                self.functions['input'] = ('function', 'int', 'input', [], [])
            return None
            
        elif node_type == 'print':
            args = [str(self.eval(arg)) for arg in node[1]]
            output = ' '.join(args).replace(' :', ':').replace(': ', ':')
            print(output)
            return None
            
        elif node_type == 'input':
            try:
                user_input = input()
                return int(user_input) if user_input.isdigit() else 0
            except:
                return 0
                
        elif node_type == 'string':
            return node[1]
            
        elif node_type == 'expression_stmt':
            return self.eval(node[1])
            
        elif node_type == 'pointer_decl':
            var_type, var_name, init_value = node[1], node[2], node[3]
            
            if init_value is not None:
                if init_value[0] == 'pointer_op' and init_value[1] == '&':
                    target_var = init_value[2][1]
                    addr = self.alloc_address()
                    self.pointers[addr] = ('var', target_var)
                    self.env[var_name] = addr
                else:
                    self.env[var_name] = self.eval(init_value)
            else:
                self.env[var_name] = None
        
        elif node_type == 'pointer_assignment':
            ptr_name = node[1]
            value = self.eval(node[2])
            
            if ptr_name in self.env:
                ptr_addr = self.env[ptr_name]
                if ptr_addr in self.pointers:
                    _, target_var = self.pointers[ptr_addr]
                    for env in reversed(self.env_stack):
                        if target_var in env:
                            env[target_var] = value
                            return
                    # Mensagem melhorada
                    print(f"Erro em Tempo de Execução na função '{self.current_function}': A variável alvo '{target_var}' do ponteiro '{ptr_name}' não foi encontrada.")
                else:
                    # Mensagem melhorada
                    print(f"Erro de Atribuição na função '{self.current_function}': A variável '{ptr_name}' não aponta para um endereço de memória válido. Verifique se foi inicializada com '&'.")
            else:
                # Mensagem melhorada
                print(f"Erro em Tempo de Execução na função '{self.current_function}': O ponteiro '{ptr_name}' não foi declarado.")
        
        elif node_type == 'pointer_op':
            op, expr = node[1], node[2]
            
            if op == '&':
                var_name = expr[1]
                for env in reversed(self.env_stack):
                    if var_name in env:
                        addr = self.alloc_address()
                        self.pointers[addr] = ('var', var_name)
                        return addr
                # Mensagem melhorada
                print(f"Erro em Tempo de Execução na função '{self.current_function}': A variável '{var_name}' não foi encontrada para a operação de endereço '&'.")
                return 0
                
            elif op == '*':
                ptr_val = self.eval(expr)
                if ptr_val in self.pointers:
                    _, target_var = self.pointers[ptr_val]
                    for env in reversed(self.env_stack):
                        if target_var in env:
                            return env[target_var]
                    return 0
                # Mensagem melhorada
                print(f"Erro em Tempo de Execução na função '{self.current_function}': Tentativa de desreferenciar um ponteiro nulo ou inválido ('{expr[1]}').")
                return 0
            
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
                # Mensagem melhorada
                print(f"Aviso na declaração do array '{name}': O tamanho declarado é {size}, mas foram fornecidos {len(self.arrays[name])} valores de inicialização.")
            self.env[name] = {'type': 'array', 'size': size}
            
        elif node_type == 'assignment':
            var_name = node[1]
            value = self.eval(node[2])
            # Procura em todos os escopos
            for env in reversed(self.env_stack):
                if var_name in env:
                    env[var_name] = value
                    return
            # Mensagem melhorada: Informa sobre criação de variável implícita
            print(f"Aviso na função '{self.current_function}': Variável '{var_name}' não declarada foi encontrada. Criando no escopo atual. Considere declará-la explicitamente.")
            self.env[var_name] = value
            
        elif node_type == 'array_assignment':
            array_name, index_expr, value_expr = node[1], node[2], node[3]
            if array_name not in self.arrays:
                # Mensagem melhorada
                print(f"Erro em Tempo de Execução na função '{self.current_function}': Tentativa de atribuição a um array não declarado '{array_name}'.")
                return
            index = self.eval(index_expr)
            if not isinstance(index, int) or index < 0 or index >= len(self.arrays[array_name]):
                # Mensagem melhorada
                print(f"Erro de Acesso ao Array na função '{self.current_function}': O índice {index} está fora dos limites para o array '{array_name}' de tamanho {len(self.arrays[array_name])}. Índices válidos: 0 a {len(self.arrays[array_name]) - 1}.")
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
            if node[1] is not None:
                self.return_value = self.eval(node[1])
            else:
                self.return_value = None
            return self.return_value
            
        elif node_type == 'function_call':
            func_name = node[1]
            if func_name in self.functions:
                func = self.functions[func_name]
                args = [self.eval(arg) for arg in node[2]]
                
                if len(args) != len(func[3]):
                    # Mensagem melhorada
                    print(f"Erro na chamada da função '{func_name}': esperava {len(func[3])} argumentos, mas recebeu {len(args)}.")
                    return None
                    
                self.push_env()
                
                for (param_type, param_name, is_array), arg_value in zip(func[3], args):
                    if isinstance(param_type, tuple) and param_type[2] > 0:
                        self.env[param_name] = arg_value
                    elif is_array:
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
                # Mensagem melhorada
                print(f"Erro em Tempo de Execução na função '{self.current_function}': Tentativa de chamar uma função não definida '{func_name}'.")
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
                '%': lambda a, b: a % b,
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
            if var_name in self.arrays:
                return self.arrays[var_name]
                
            if self.current_function and var_name not in self.env and var_name in self.env_stack[0]:
                return self.env_stack[0][var_name]
                
            for env in reversed(self.env_stack):
                if var_name in env:
                    return env[var_name]
            # Mensagem melhorada
            print(f"Aviso na função '{self.current_function}': Variável '{var_name}' não foi encontrada, retornando valor padrão 0.")
            return 0
            
        elif node_type == 'array_access':
            array_name, index_expr = node[1], node[2]
            if array_name not in self.arrays:
                # Mensagem melhorada
                print(f"Erro em Tempo de Execução na função '{self.current_function}': Tentativa de acessar um array não declarado '{array_name}'.")
                return 0
            index = self.eval(index_expr)
            if not isinstance(index, int) or index < 0 or index >= len(self.arrays[array_name]):
                # Mensagem melhorada
                print(f"Erro de Acesso ao Array na função '{self.current_function}': O índice {index} está fora dos limites para o array '{array_name}' de tamanho {len(self.arrays[array_name])}. Índices válidos: 0 a {len(self.arrays[array_name]) - 1}.")
                return 0
            return self.arrays[array_name][index]

        return None