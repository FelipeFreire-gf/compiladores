import sys
from lexer import lexer
from parser import parser
from interpreter import Interpreter

# Main
# 1. Lê o código-fonte (.c) de um arquivo passado como argumento
# 2. Envia o código para o lexer gerar tokens
# 3. Envia os tokens para o parser gerar a árvore sintática (AST)
# 4. Envia a AST para o interpretador executar o programa
# 5. Exibe a AST formatada, os tokens, o valor de retorno e o estado final da memória



def format_ast(node, indent=0):
    """Formata a AST para exibição hierárquica com indentação visual"""
    indent_str = "  " * indent
    
    if not isinstance(node, tuple):
        return f"{indent_str}└─ {node}\n"

    result = ""
    node_type = node[0]

    # Nó do programa principal
    if node_type == 'program':
        result += f"{indent_str}└─ Program\n"
        for element in node[1]:
            result += format_ast(element, indent + 1)
    
    # Funções
    elif node_type in ['function', 'function_definition']:
        func_name = node[2] if node_type == 'function' else node[1][1]
        return_type = node[1] if node_type == 'function' else node[0]
        result += f"{indent_str}└─ Function: {func_name} (returns {return_type})\n"
        
        # Parâmetros
        params = node[3] if node_type == 'function' else []
        if params:
            result += f"{indent_str}  └─ Parameters\n"
            for param in params:
                param_type = param[0][1] if isinstance(param[0], tuple) else param[0]
                result += f"{indent_str}    └─ {param[1]}: {param_type}{'[]' if len(param) > 2 and param[2] else ''}\n"
        
        # Corpo da função
        body = node[4] if node_type == 'function' else node[2]
        result += f"{indent_str}  └─ Body\n"
        for stmt in body:
            result += format_ast(stmt, indent + 2)
    
    # Declarações
    elif node_type == 'declaration':
        var_type = node[1][1] if isinstance(node[1], tuple) else node[1]
        result += f"{indent_str}└─ Declare: {node[2]} ({var_type})\n"
        if node[3] is not None:
            result += f"{indent_str}  └─ Initial value\n"
            result += format_ast(node[3], indent + 2)
    
    # Arrays
    elif node_type == 'array_declaration':
        var_type = node[1][1] if isinstance(node[1], tuple) else node[1]
        result += f"{indent_str}└─ Array Declare: {node[2]} ({var_type})[{node[3]}]\n"
    
    elif node_type == 'array_declaration_init':
        var_type = node[1][1] if isinstance(node[1], tuple) else node[1]
        result += f"{indent_str}└─ Array Declare Init: {node[2]} ({var_type})[{node[3]}]\n"
        result += f"{indent_str}  └─ Values\n"
        for val in node[4]:
            result += format_ast(val, indent + 2)
    
    # Atribuições
    elif node_type == 'assignment':
        result += f"{indent_str}└─ Assign: {node[1]}\n"
        result += f"{indent_str}  └─ Value\n"
        result += format_ast(node[2], indent + 2)
    
    elif node_type == 'array_assignment':
        array_name = node[1]
        index_node = node[2]
        value_node = node[3]
        
        index_str = str(index_node[1]) if index_node[0] == 'number' else format_ast(index_node, 0).strip()
        
        result += f"{indent_str}└─ Array Assign: {array_name}[{index_str}]\n"
        result += f"{indent_str}  └─ Value\n"
        result += format_ast(value_node, indent + 2)
    
    # Estruturas de controle
    elif node_type == 'if':
        result += f"{indent_str}└─ If\n"
        result += f"{indent_str}  └─ Condition\n"
        result += format_ast(node[1], indent + 2)
        result += f"{indent_str}  └─ Then\n"
        for stmt in node[2]:
            result += format_ast(stmt, indent + 2)
        if node[3] is not None:
            result += f"{indent_str}  └─ Else\n"
            if isinstance(node[3], list):
                for stmt in node[3]:
                    result += format_ast(stmt, indent + 2)
            else:
                result += format_ast(node[3], indent + 2)
    
    elif node_type == 'while':
        result += f"{indent_str}└─ While\n"
        result += f"{indent_str}  └─ Condition\n"
        result += format_ast(node[1], indent + 2)
        result += f"{indent_str}  └─ Body\n"
        for stmt in node[2]:
            result += format_ast(stmt, indent + 2)
    
    elif node_type == 'return':
        result += f"{indent_str}└─ Return\n"
        if node[1] is not None:
            result += f"{indent_str}  └─ Value\n"
            result += format_ast(node[1], indent + 2)
    
    # Expressões
    elif node_type == 'expression_stmt':
        result += f"{indent_str}└─ Expression\n"
        result += format_ast(node[1], indent + 2)
    
    elif node_type in ['logical', 'binop']:
        result += f"{indent_str}└─ {node_type.capitalize()}: {node[1]}\n"
        result += f"{indent_str}  └─ Left\n"
        result += format_ast(node[2], indent + 2)
        result += f"{indent_str}  └─ Right\n"
        result += format_ast(node[3], indent + 2)
    
    elif node_type == 'not':
        result += f"{indent_str}└─ Not\n"
        result += f"{indent_str}  └─ Expression\n"
        result += format_ast(node[1], indent + 2)
    
    # Literais e identificadores
    elif node_type == 'number':
        result += f"{indent_str}└─ Num: {node[1]}\n"
    
    elif node_type == 'bool':
        result += f"{indent_str}└─ Bool: {node[1]}\n"
    
    elif node_type == 'id':
        result += f"{indent_str}└─ Var: {node[1]}\n"
    
    elif node_type == 'string':
        result += f"{indent_str}└─ String: \"{node[1]}\"\n"
    
    # Chamadas de função
    elif node_type == 'function_call':
        result += f"{indent_str}└─ Call: {node[1]}\n"
        if node[2]:
            result += f"{indent_str}  └─ Arguments\n"
            for arg in node[2]:
                result += format_ast(arg, indent + 2)
    
    elif node_type == 'print':
        result += f"{indent_str}└─ Print\n"
        result += f"{indent_str}  └─ Arguments\n"
        for arg in node[1]:
            result += format_ast(arg, indent + 2)
    
    elif node_type == 'input':
        result += f"{indent_str}└─ Input\n"
    
    # Acesso a arrays
    elif node_type == 'array_access':
        array_name = node[1]
        index_node = node[2]
        
        index_str = str(index_node[1]) if index_node[0] == 'number' else format_ast(index_node, 0).strip()
        
        result += f"{indent_str}└─ Array Access: {array_name}[{index_str}]\n"
    
    # Includes
    elif node_type == 'include':
        result += f"{indent_str}└─ Include: {node[1]}\n"
    
    # Ponteiros
    elif node_type == 'pointer_decl':
        result += f"{indent_str}└─ Pointer Declare: {node[2]} ({node[1]})\n"
        if node[3] is not None:
            result += f"{indent_str}  └─ Initial value\n"
            result += format_ast(node[3], indent + 2)
    
    elif node_type == 'pointer_op':
        result += f"{indent_str}└─ Pointer Op: {node[1]}\n"
        result += f"{indent_str}  └─ Expression\n"
        result += format_ast(node[2], indent + 2)
    
    else:
        result += f"{indent_str}└─ Unknown node type: {node_type}\n"
        for item in node[1:]:
            result += format_ast(item, indent + 1)

    return result

def analyze_code(code):
    """Analisa o código em três fases: tokenização, parsing e execução"""
    print("\n=== TOKENIZATION ===")
    lexer.input(code)
    token_count = 0
    for tok in lexer:
        print(f"Line {tok.lineno}: {tok.type:15} = {tok.value}")
        token_count += 1
    print(f"\nTotal tokens: {token_count}")

    print("\n=== SYNTAX TREE ===")
    ast = parser.parse(code)
    if ast:
        print(format_ast(ast))
        
        print("\n=== EXECUTION ===")
        interpreter = Interpreter()
        result = interpreter.interpret(ast)
        
        print("\n=== FINAL STATE ===")
        print(f"Return value: {result}")
        
        # Mostrar variáveis globais
        print("\nGlobal variables:")
        for var, value in interpreter.env_stack[0].items():
            print(f"  {var}: {value}")
        
        # Mostrar variáveis locais se houver
        if len(interpreter.env_stack) > 1:
            print("\nLocal variables:")
            for var, value in interpreter.env_stack[-1].items():
                print(f"  {var}: {value}")
        
        # Mostrar arrays
        if interpreter.arrays:
            print("\nArrays:")
            for name, array in interpreter.arrays.items():
                print(f"  {name}: {array}")
        
        # Mostrar ponteiros
        if interpreter.pointers:
            print("\nPointers:")
            for addr, (ptype, target) in interpreter.pointers.items():
                print(f"  {addr}: {ptype} -> {target}")
        
        # Estatísticas de memória
        print(f"\nMemory used: {interpreter.memory_counter - 0x1000} bytes")
    else:
        print("Failed to generate AST")

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <source_file.c>")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
            print(f"=== Analyzing {filename} ===")
            analyze_code(code)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()