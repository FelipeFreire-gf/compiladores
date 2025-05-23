import sys
from lexer import lexer
from parser import parser
from interpreter import Interpreter

def format_ast(node, indent=0):
    indent_str = "  " * indent
    if not isinstance(node, tuple):
        return f"{indent_str}└─ {node}\n"

    result = ""
    node_type = node[0]

    if node_type == 'program':
        result += f"{indent_str}└─ Program\n"
        for element in node[1]:
            result += format_ast(element, indent + 1)

    elif node_type == 'function':
        result += f"{indent_str}└─ Function: {node[2]} ({node[1]})\n"
        if node[3]:
            result += f"{indent_str}  └─ Parameters\n"
            for param in node[3]:
                result += f"{indent_str}    └─ {param[1]}: {param[0]}{'[]' if param[2] else ''}\n"
        result += f"{indent_str}  └─ Body\n"
        for stmt in node[4]:
            result += format_ast(stmt, indent + 2)

    elif node_type == 'declaration':
        result += f"{indent_str}└─ Declare: {node[2]} ({node[1]})\n"
        if node[3] is not None:
            result += f"{indent_str}  └─ Value\n"
            result += format_ast(node[3], indent + 2)

    elif node_type == 'array_declaration':
        result += f"{indent_str}└─ Array Declare: {node[2]} ({node[1]})[{node[3]}]\n"

    elif node_type == 'array_declaration_init':
        result += f"{indent_str}└─ Array Declare Init: {node[2]} ({node[1]})[{node[3]}]\n"
        result += f"{indent_str}  └─ Values\n"
        for val in node[4]:
            result += format_ast(val, indent + 2)

    elif node_type == 'assignment':
        result += f"{indent_str}└─ Assign: {node[1]}\n"
        result += f"{indent_str}  └─ Value\n"
        result += format_ast(node[2], indent + 2)

    elif node_type == 'array_assignment':
        array_name = node[1]
        index_node = node[2]
        value_node = node[3]
        
        # Formata o índice de forma mais limpa
        if index_node[0] == 'number':
            index_str = str(index_node[1])
        else:
            index_str = format_ast(index_node, 0).strip()
        
        result += f"{indent_str}└─ Array Assign: {array_name}[{index_str}]\n"
        result += f"{indent_str}  └─ Value\n"
        result += format_ast(value_node, indent + 2)

    elif node_type == 'if':
        result += f"{indent_str}└─ If\n"
        result += f"{indent_str}  └─ Condition\n"
        result += format_ast(node[1], indent + 2)
        result += f"{indent_str}  └─ Body\n"
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

    elif node_type == 'expression_stmt':
        result += f"{indent_str}└─ Expression\n"
        result += format_ast(node[1], indent + 2)

    elif node_type == 'logical':
        result += f"{indent_str}└─ Logical: {node[1]}\n"
        result += f"{indent_str}  └─ Left\n"
        result += format_ast(node[2], indent + 2)
        result += f"{indent_str}  └─ Right\n"
        result += format_ast(node[3], indent + 2)

    elif node_type == 'binop':
        result += f"{indent_str}└─ Op: {node[1]}\n"
        result += f"{indent_str}  └─ Left\n"
        result += format_ast(node[2], indent + 2)
        result += f"{indent_str}  └─ Right\n"
        result += format_ast(node[3], indent + 2)

    elif node_type == 'not':
        result += f"{indent_str}└─ Not\n"
        result += f"{indent_str}  └─ Expression\n"
        result += format_ast(node[1], indent + 2)

    elif node_type == 'number':
        result += f"{indent_str}└─ Num: {node[1]}\n"

    elif node_type == 'bool':
        result += f"{indent_str}└─ Bool: {node[1]}\n"

    elif node_type == 'id':
        result += f"{indent_str}└─ Var: {node[1]}\n"

    elif node_type == 'function_call':
        result += f"{indent_str}└─ Call: {node[1]}\n"
        if node[2]:
            result += f"{indent_str}  └─ Arguments\n"
            for arg in node[2]:
                result += format_ast(arg, indent + 2)

    elif node_type == 'array_access':
        array_name = node[1]
        index_node = node[2]
        
        # Formata o índice de forma mais limpa
        if index_node[0] == 'number':
            index_str = str(index_node[1])
        else:
            index_str = format_ast(index_node, 0).strip()
        
        result += f"{indent_str}└─ Array Access: {array_name}[{index_str}]\n"

    return result

def analisar_parametros(codigo):
    # Tokenização
    print("Tokens:")
    lexer.input(codigo)
    for tok in lexer:
        print(f"  {tok.type}: {tok.value}")

    # Parsing
    print("\nAbstract Syntax Tree:")
    resultado = parser.parse(codigo)
    if resultado:
        print(format_ast(resultado))
    else:
        print("Error: No valid syntax tree generated.")
        return None

    # Interpretação
    interpreter = Interpreter()
    result = interpreter.interpret(resultado)

    print("\nResultado:", result)
    print("Variáveis finais:", interpreter.env_stack[0])
    print("Arrays finais:")
    for name, arr in interpreter.arrays.items():
        print(f"  {name}: {arr}")

    return resultado

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py file.c")
        sys.exit(1)

    arquivo = sys.argv[1]
    with open(arquivo, 'r') as f:
        conteudo = f.read()
        analisar_parametros(conteudo)
